import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torchvision.transforms as T
import numpy as np

def create_anchors(anchor_sizes: list, aspect_ratios: list):
    """
    Creates base anchors with different sizes and aspect ratios.
    Args:
        anchor_sizes (list): List of anchor sizes (e.g., [16, 32, 64]).
        aspect_ratios (list): List of aspect ratios (e.g., [0.5, 1.0, 2.0]).
    Returns:
        torch.Tensor: Tensor of shape (num_anchors, 2) with [width, height] for each anchor.
    """
    anchors = []
    for size in anchor_sizes:
        for ratio in aspect_ratios:
            width = size * (ratio ** 0.5)
            height = size / (ratio ** 0.5)
            anchors.append([width, height])
    return torch.tensor(anchors, dtype=torch.float32)

def generate_anchors(base_anchors, feature_size, image_size=256):
    """
    Generates anchors across a feature map.
    Args:
        base_anchors (torch.Tensor): Base anchors of shape (num_anchors, 2) [width, height].
        feature_size (tuple): Feature map size (height, width).
        image_size (int): Input image size (assumes square image).
    Returns:
        torch.Tensor: Anchors of shape (num_anchors_total, 4) [center_x, center_y, width, height].
    """
    feature_map_height, feature_map_width = feature_size
    stride_h = image_size / feature_map_height
    stride_w = image_size / feature_map_width
    generated_anchors = []
    
    grid_y, grid_x = torch.meshgrid(
        torch.arange(feature_map_height, dtype=torch.float32),
        torch.arange(feature_map_width, dtype=torch.float32),
        indexing='ij'
    )
    grid_x = (grid_x + 0.5) * stride_w
    grid_y = (grid_y + 0.5) * stride_h
    
    for anchor in base_anchors:
        width, height = anchor
        cx = grid_x.flatten().unsqueeze(1)
        cy = grid_y.flatten().unsqueeze(1)
        w = torch.full_like(cx, width)
        h = torch.full_like(cy, height)
        anchors = torch.cat([cx, cy, w, h], dim=1)
        generated_anchors.append(anchors)
    
    return torch.cat(generated_anchors, dim=0)

def cxcywh_to_xyxy(box):
    """
    Converts boxes from [center_x, center_y, width, height] to [x_min, y_min, x_max, y_max].
    Args:
        box (torch.Tensor): Box tensor of shape (..., 4).
    Returns:
        torch.Tensor: Converted box tensor of shape (..., 4).
    """
    cx, cy, w, h = box[..., 0], box[..., 1], box[..., 2], box[..., 3]
    x_min = cx - w / 2
    y_min = cy - h / 2
    x_max = cx + w / 2
    y_max = cy + h / 2
    return torch.stack([x_min, y_min, x_max, y_max], dim=-1)

def compute_iou(boxes1, boxes2):
    """
    Computes IoU between two sets of boxes in [x_min, y_min, x_max, y_max] format.
    Args:
        boxes1 (torch.Tensor): Boxes of shape (N, 4).
        boxes2 (torch.Tensor): Boxes of shape (M, 4).
    Returns:
        torch.Tensor: IoU matrix of shape (N, M).
    """
    area1 = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    area2 = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])
    
    x1 = torch.max(boxes1[:, None, 0], boxes2[:, 0])
    y1 = torch.max(boxes1[:, None, 1], boxes2[:, 1])
    x2 = torch.min(boxes1[:, None, 2], boxes2[:, 2])
    y2 = torch.min(boxes1[:, None, 3], boxes2[:, 3])
    
    intersection = torch.clamp(x2 - x1, min=0) * torch.clamp(y2 - y1, min=0)
    union = area1[:, None] + area2 - intersection
    iou = intersection / (union + 1e-6)
    return iou

def compute_targets(anchors, gt_boxes, gt_labels, iou_threshold=0.5, device='cpu'):
    """
    Computes classification and regression targets for anchors.
    Args:
        anchors (torch.Tensor): Anchors of shape (num_anchors, 4) [center_x, center_y, width, height].
        gt_boxes (torch.Tensor): Ground truth boxes of shape (num_gt, 4) [x_min, y_min, x_max, y_max].
        gt_labels (torch.Tensor): Ground truth labels of shape (num_gt,).
        iou_threshold (float): IoU threshold for positive anchors.
        device (str): Device to place tensors on.
    Returns:
        tuple: (target_cls, target_reg, positive_mask)
            - target_cls (torch.Tensor): Classification targets of shape (num_anchors,).
            - target_reg (torch.Tensor): Regression targets of shape (num_anchors, 4).
            - positive_mask (torch.Tensor): Boolean mask for positive anchors.
    """
    anchors = anchors.to(device)
    gt_boxes = gt_boxes.to(device)
    gt_labels = gt_labels.to(device)
    
    num_anchors = anchors.size(0)
    if gt_boxes.size(0) == 0:
        target_cls = torch.zeros(num_anchors, dtype=torch.long, device=device)
        target_reg = torch.zeros((num_anchors, 4), dtype=torch.float32, device=device)
        positive_mask = torch.zeros(num_anchors, dtype=torch.bool, device=device)
        return target_cls, target_reg, positive_mask
    
    anchors_xyxy = cxcywh_to_xyxy(anchors)
    ious = compute_iou(anchors_xyxy, gt_boxes)
    max_ious, max_idx = ious.max(dim=1)
    positive_mask = max_ious > iou_threshold
    
    for i in range(gt_boxes.size(0)):
        if ious.size(0) > 0:
            best_anchor_idx = ious[:, i].argmax()
            positive_mask[best_anchor_idx] = True
            max_idx[best_anchor_idx] = i
    
    target_cls = torch.zeros(num_anchors, dtype=torch.long, device=device)
    target_cls[positive_mask] = gt_labels[max_idx[positive_mask]]
    
    target_reg = torch.zeros((num_anchors, 4), dtype=torch.float32, device=device)
    if positive_mask.any():
        anchors_pos = anchors[positive_mask]
        gt_idx = max_idx[positive_mask]
        gt_boxes_pos = gt_boxes[gt_idx]
        gt_cx = (gt_boxes_pos[:, 0] + gt_boxes_pos[:, 2]) / 2
        gt_cy = (gt_boxes_pos[:, 1] + gt_boxes_pos[:, 3]) / 2
        gt_w = gt_boxes_pos[:, 2] - gt_boxes_pos[:, 0]
        gt_h = gt_boxes_pos[:, 3] - gt_boxes_pos[:, 1]
        dx = (gt_cx - anchors_pos[:, 0]) / anchors_pos[:, 2]
        dy = (gt_cy - anchors_pos[:, 1]) / anchors_pos[:, 3]
        dw = torch.log(gt_w / anchors_pos[:, 2] + 1e-6)
        dh = torch.log(gt_h / anchors_pos[:, 3] + 1e-6)
        target_reg[positive_mask] = torch.stack([dx, dy, dw, dh], dim=1)
    
    return target_cls, target_reg, positive_mask

def detection_loss(pred_cls, pred_reg, target_cls, target_reg, positive_mask, cls_weight=1.0, reg_weight=1.0):
    """
    Computes detection loss combining classification and regression losses.
    Args:
        pred_cls (torch.Tensor): Predicted class scores of shape (batch, num_anchors, num_classes).
        pred_reg (torch.Tensor): Predicted regression offsets of shape (batch, num_anchors, 4).
        target_cls (torch.Tensor): Target class labels of shape (batch, num_anchors).
        target_reg (torch.Tensor): Target regression offsets of shape (batch, num_anchors, 4).
        positive_mask (torch.Tensor): Boolean mask for positive anchors of shape (batch, num_anchors).
        cls_weight (float): Weight for classification loss.
        reg_weight (float): Weight for regression loss.
    Returns:
        torch.Tensor: Combined loss (classification + regression).
    """
    cls_loss = F.cross_entropy(pred_cls.view(-1, pred_cls.size(-1)), target_cls.view(-1), reduction='mean')
    reg_loss = torch.tensor(0.0, device=pred_cls.device)
    if positive_mask.sum() > 0:
        pred_reg_positive = pred_reg[positive_mask]
        target_reg_positive = target_reg[positive_mask]
        reg_loss = F.smooth_l1_loss(pred_reg_positive, target_reg_positive, reduction='mean')
    return cls_weight * cls_loss + reg_weight * reg_loss

class DetectionDataset(Dataset):
    def __init__(self, images, bboxes, labels, transform=None, transform_type="albumentations"):
        """
        Dataset for object detection.
        Args:
            images (list): List of image file paths.
            bboxes (list): List of bounding boxes per image in [x_min, y_min, x_max, y_max] format.
            labels (list): List of labels per image.
            transform: Transform pipeline (Albumentations or PyTorch).
            transform_type (str): Type of transform ('albumentations' or 'torch').
        """
        self.images = images
        self.bboxes = bboxes
        self.labels = labels
        self.transform = transform
        self.transform_type = transform_type
        if transform_type not in ["albumentations", "torch"]:
            raise ValueError("transform_type must be 'albumentations' or 'torch'")

    def __getitem__(self, idx):
        img = Image.open(self.images[idx]).convert("L")  
        bboxes = self.bboxes[idx]
        labels = self.labels[idx]
        
        if self.transform:
            if self.transform_type == "albumentations":
                img = np.array(img)
                transformed = self.transform(image=img, bboxes=bboxes, labels=labels)
                img = transformed["image"]
                bboxes = transformed["bboxes"]
                labels = transformed["labels"]
            elif self.transform_type == "torch":
                img = self.transform(img)
        else:
            img = T.ToTensor()(img)
        
        return (
            img,
            torch.tensor(bboxes, dtype=torch.float32) if bboxes else torch.empty((0, 4), dtype=torch.float32),
            torch.tensor(labels, dtype=torch.long) if labels else torch.empty((0,), dtype=torch.long)
        )

    def __len__(self):
        return len(self.images)

def detection_transforms(mean=0.5, std=0.5):
    """
    Creates Albumentations transform pipeline for detection.
    Args:
        mean (float): Mean for normalization.
        std (float): Standard deviation for normalization.
    Returns:
        A.Compose: Transform pipeline.
    """
    transforms = A.Compose([
        A.Resize(256, 256),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.CLAHE(p=0.1),
        A.Blur(blur_limit=3, p=0.1),
        A.Normalize(mean=[mean], std=[std]),
        ToTensorV2(),
    ], bbox_params=A.BboxParams(
        format='pascal_voc',
        min_visibility=0.3,
        label_fields=['labels']
    ))
    return transforms

def detection_training(epochs, model, train_dl, optimizer=None, lr=3e-3, device=None, iou_threshold=0.5):
    """
    Simplified training loop for detection model, comparing predicted bounding boxes to ground truth.
    Args:
        epochs (int): Number of training epochs.
        model (nn.Module): Detection model outputting [num_detections, 5] tensors.
        train_dl (DataLoader): Training data loader with images, bboxes, and labels.
        optimizer: Optimizer (default: Adam).
        lr (float): Learning rate.
        device (str): Device to train on (default: cuda if available, else cpu).
        iou_threshold (float): IoU threshold for matching predicted and ground truth boxes.
    Returns:
        nn.Module: Trained model.
    """
    optimizer = optimizer or torch.optim.Adam(model.parameters(), lr=lr)
    device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        num_batches = 0
        
        for img, gt_boxes, gt_labels in train_dl:
            img = img[0:1].to(device)  
            gt_boxes = gt_boxes[0].to(device)  
            gt_labels = gt_labels[0].to(device) 
            
            
            pred_boxes = model(img)  
            
            loss = compute_bbox_loss(pred_boxes, gt_boxes, gt_labels, iou_threshold, device)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            num_batches += 1
        
        train_loss /= num_batches
        print(f'Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f}')
    
    return model

def compute_bbox_loss(pred_boxes, gt_boxes, gt_labels, iou_threshold, device):
    """
    Computes loss between predicted and ground truth bounding boxes.
    Args:
        pred_boxes (torch.Tensor): Predicted boxes [num_detections, 5] (x_min, y_min, x_max, y_max, score).
        gt_boxes (torch.Tensor): Ground truth boxes [num_gt, 4] (x_min, y_min, x_max, y_max).
        gt_labels (torch.Tensor): Ground truth labels [num_gt].
        iou_threshold (float): IoU threshold for matching.
        device (str): Device for tensors.
    Returns:
        torch.Tensor: Combined box and score loss.
    """
    if pred_boxes.size(0) == 0 or gt_boxes.size(0) == 0:
        if gt_boxes.size(0) > 0:
            return F.binary_cross_entropy(
                torch.zeros(1, device=device), torch.ones(1, device=device)
            )
        return torch.tensor(0.0, device=device)
    
    ious = compute_iou(pred_boxes[:, :4], gt_boxes) 
    max_ious, max_idx = ious.max(dim=1) 
    
    positive_mask = max_ious > iou_threshold
    if not positive_mask.any():
        return F.binary_cross_entropy(
            pred_boxes[:, 4], torch.zeros_like(pred_boxes[:, 4])
        )
    
    pred_boxes_pos = pred_boxes[positive_mask, :4]
    gt_boxes_pos = gt_boxes[max_idx[positive_mask]]
    box_loss = F.smooth_l1_loss(pred_boxes_pos, gt_boxes_pos, reduction='mean')
    
    pred_scores_pos = pred_boxes[positive_mask, 4]
    gt_scores_pos = (gt_labels[max_idx[positive_mask]] == 1).float()
    score_loss = F.binary_cross_entropy(pred_scores_pos, gt_scores_pos, reduction='mean')
    
    return box_loss + score_loss