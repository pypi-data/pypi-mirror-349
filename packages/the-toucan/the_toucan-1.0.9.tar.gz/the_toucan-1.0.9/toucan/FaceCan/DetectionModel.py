import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.ops import nms
from .utils import create_anchors, generate_anchors

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

    def forward(self, x):
        return self.conv(x)

class Detection(nn.Module):
    def __init__(self, img_size=(256, 256), num_classes=2):
        super(Detection, self).__init__()
        self.img_size = img_size
        self.num_classes = num_classes
        
        self.anchor_sizes = [[16, 32, 64], [64, 128, 256]]
        self.aspect_ratios = [0.5, 1.0, 2.0]
        self.feature_sizes = [(16, 16), (8, 8)]
        
        anchors_list = []
        for sizes, feat_size in zip(self.anchor_sizes, self.feature_sizes):
            base_anchors = create_anchors(sizes, self.aspect_ratios)
            anchors = generate_anchors(base_anchors, feat_size, image_size=self.img_size[0])
            anchors_list.append(torch.tensor(anchors, dtype=torch.float32))
        self.register_buffer('anchors', torch.cat(anchors_list, dim=0))
        
        self.backbone = nn.Sequential(
            DWBlock(1, 32, stride=2),
            DWBlock(32, 64, stride=1),
            DWBlock(64, 128, stride=2),
            DWBlock(128, 256, stride=2),
            DWBlock(256, 512, stride=2),
            DWBlock(512, 1024, stride=2)
        )
        
        self.cls_heads = nn.ModuleList([
            nn.Conv2d(512, len(self.aspect_ratios) * num_classes, kernel_size=1),
            nn.Conv2d(1024, len(self.aspect_ratios) * num_classes, kernel_size=1)
        ])
        self.reg_heads = nn.ModuleList([
            nn.Conv2d(512, len(self.aspect_ratios) * 4, kernel_size=1),
            nn.Conv2d(1024, len(self.aspect_ratios) * 4, kernel_size=1)
        ])
    
    def forward(self, x):
        features = []
        for i, layer in enumerate(self.backbone):
            x = layer(x)
            if i == 4:  # After fifth block
                features.append(x)
            elif i == 5:  # After sixth block
                features.append(x)
        
        cls_scores = []
        box_offsets = []
        batch_size = x.size(0)
        for feat, cls_head, reg_head, feat_size in zip(
            features, self.cls_heads, self.reg_heads, self.feature_sizes
        ):
            cls = cls_head(feat).permute(0, 2, 3, 1).contiguous()
            h, w = feat.shape[2], feat.shape[3]
            num_anchors = len(self.aspect_ratios)
            cls = cls.view(batch_size, h * w * num_anchors, self.num_classes)
            cls_scores.append(cls)
            
            reg = reg_head(feat).permute(0, 2, 3, 1).contiguous()
            reg = reg.view(batch_size, h * w * num_anchors, 4)
            box_offsets.append(reg)
        
        cls_scores = torch.cat(cls_scores, dim=1)
        box_offsets = torch.cat(box_offsets, dim=1)
        return cls_scores, box_offsets
    
    def decode_boxes(self, offsets):
        boxes_cxcywh = torch.zeros_like(self.anchors)
        boxes_cxcywh[:, 0] = offsets[:, 0] * self.anchors[:, 2] + self.anchors[:, 0]  # cx
        boxes_cxcywh[:, 1] = offsets[:, 1] * self.anchors[:, 3] + self.anchors[:, 1]  # cy
        boxes_cxcywh[:, 2] = torch.exp(offsets[:, 2]) * self.anchors[:, 2]  # w
        boxes_cxcywh[:, 3] = torch.exp(offsets[:, 3]) * self.anchors[:, 3]  # h
        
        x_min = boxes_cxcywh[:, 0] - boxes_cxcywh[:, 2] / 2
        y_min = boxes_cxcywh[:, 1] - boxes_cxcywh[:, 3] / 2
        x_max = boxes_cxcywh[:, 0] + boxes_cxcywh[:, 2] / 2
        y_max = boxes_cxcywh[:, 1] + boxes_cxcywh[:, 3] / 2
        boxes = torch.stack([x_min, y_min, x_max, y_max], dim=1)
        return boxes
    
    def detect(self, x, conf_threshold=0.5, nms_threshold=0.5, max_detections=100):
        """
        Performs inference and directly outputs bounding boxes with probabilities.
        Args:
            x (torch.Tensor): Input image tensor of shape (batch_size, channels, height, width).
            conf_threshold (float): Confidence score threshold for detections (default: 0.5).
            nms_threshold (float): IoU threshold for Non-Maximum Suppression (default: 0.5).
            max_detections (int): Maximum number of detections to keep per image (default: 100).
        Returns:
            List[torch.Tensor]: List of detections per image, each tensor of shape (num_detections, 5)
                               with [x_min, y_min, x_max, y_max, score].
        """
        cls_scores, box_offsets = self.forward(x)
        batch_size = x.size(0)
        probs = F.softmax(cls_scores, dim=-1)[:, :, 1]  # Probability of foreground class
        final_detections = []
        
        for i in range(batch_size):
            offsets = box_offsets[i]
            boxes = self.decode_boxes(offsets)
            scores = probs[i]
            mask = scores > conf_threshold
            selected_boxes = boxes[mask]
            selected_scores = scores[mask]
            
            if selected_boxes.size(0) > 0:
                keep = nms(selected_boxes, selected_scores, nms_threshold)
                if len(keep) > max_detections:
                    keep = keep[:max_detections]  # Keep top-scoring detections
                final_boxes = selected_boxes[keep]
                final_scores = selected_scores[keep]
                detections = torch.cat([final_boxes, final_scores.unsqueeze(1)], dim=1)
            else:
                detections = torch.empty((0, 5), device=x.device)
            final_detections.append(detections)
        
        return final_detections