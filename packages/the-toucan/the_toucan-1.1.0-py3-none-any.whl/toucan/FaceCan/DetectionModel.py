import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.ops import nms
from .utils import create_anchors, generate_anchors, cxcywh_to_xyxy

class DWBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(DWBlock, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, in_channels, kernel_size=3, stride=stride, padding=1, groups=in_channels, bias=False),
            nn.BatchNorm2d(in_channels),
            nn.ReLU6(inplace=True),
            nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU6(inplace=True)
        )
        self.shortcut = nn.Sequential()
        if stride == 1 and in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = self.conv(x)
        out += self.shortcut(x)
        return out

class Detection(nn.Module):
    def __init__(self, img_size=(256, 256), num_classes=2, in_channels=1):
        super(Detection, self).__init__()
        self.img_size = img_size
        self.num_classes = num_classes
        self.in_channels = in_channels 
        
        self.anchor_sizes = [[32, 64], [128]]  
        self.aspect_ratios = [1.0, 1.5]  
        self.feature_sizes = [(16, 16), (8, 8)]
        
        anchors_list = []
        for sizes, feat_size in zip(self.anchor_sizes, self.feature_sizes):
            base_anchors = create_anchors(sizes, self.aspect_ratios)
            anchors = generate_anchors(base_anchors, feat_size, image_size=self.img_size[0])
            anchors_list.append(anchors.clone().detach())  
        self.register_buffer('anchors', torch.cat(anchors_list, dim=0))
        self.num_anchors = self.anchors.shape[0]  
        
        self.backbone = nn.Sequential(
            DWBlock(self.in_channels, 16, stride=2), 
            DWBlock(16, 32, stride=2),              
            DWBlock(32, 64, stride=2),              
            DWBlock(64, 128, stride=2)             
        )
        self.cls_head = nn.Conv2d(128, len(self.aspect_ratios) * num_classes, kernel_size=1)
        self.reg_head = nn.Conv2d(128, len(self.aspect_ratios) * 4, kernel_size=1)
    
    def forward(self, x, conf_threshold=0.5, nms_threshold=0.5, max_detections=100):
        """
        Forward pass that directly outputs bounding boxes.
        Args:
            x (torch.Tensor): Input image, shape [1, in_channels, 256, 256]
            conf_threshold (float): Confidence threshold for detections
            nms_threshold (float): IoU threshold for NMS
            max_detections (int): Max detections per image
        Returns:
            torch.Tensor: Bounding boxes, shape [num_detections, 5] (x_min, y_min, x_max, y_max, score)
        """
        if x.dim() != 4 or x.shape[2:4] != self.img_size:
            raise ValueError(f"Expected input shape [1, {self.in_channels}, 256, 256], got {x.shape}")
        if x.shape[0] != 1:
            raise ValueError("Batch size must be 1 for single-image inference")
        
       
        x = self.backbone(x) 
        
        cls = self.cls_head(x).permute(0, 2, 3, 1).contiguous()  
        reg = self.reg_head(x).permute(0, 2, 3, 1).contiguous() 
        
        cls = cls.view(1, -1, self.num_classes) 
        reg = reg.view(1, -1, 4)              
        
        probs = F.softmax(cls, dim=-1)[0, :, 1]  
        offsets = reg[0]                         
        boxes = self.decode_boxes(offsets)      
        
        mask = probs > conf_threshold
        selected_boxes = boxes[mask]
        selected_scores = probs[mask]
        
        if selected_boxes.size(0) > 0:
            keep = nms(selected_boxes, selected_scores, nms_threshold)
            if len(keep) > max_detections:
                keep = keep[:max_detections]
            detections = torch.cat([selected_boxes[keep], selected_scores[keep].unsqueeze(1)], dim=1)
        else:
            detections = torch.empty((0, 5), device=x.device)
        
        return detections
    
    def decode_boxes(self, offsets):
        """Convert predicted offsets to xyxy boxes."""
        boxes_cxcywh = torch.zeros_like(self.anchors)
        boxes_cxcywh[:, 0] = offsets[:, 0] * self.anchors[:, 2] + self.anchors[:, 0] 
        boxes_cxcywh[:, 1] = offsets[:, 1] * self.anchors[:, 3] + self.anchors[:, 1]  
        boxes_cxcywh[:, 2] = torch.exp(offsets[:, 2]) * self.anchors[:, 2]  
        boxes_cxcywh[:, 3] = torch.exp(offsets[:, 3]) * self.anchors[:, 3]  
        return cxcywh_to_xyxy(boxes_cxcywh)