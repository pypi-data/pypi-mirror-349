import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torchvision.transforms as T

def create_anchors(anchor_sizes: list, aspect_ratios: list):
    anchors = []
    for size in anchor_sizes:
        for ratio in aspect_ratios:
            width = size * np.sqrt(ratio)
            height = size / np.sqrt(ratio)
            anchors.append([width, height])
    return anchors

def generate_anchors(base_anchors, feature_size, image_size=256):
    generated_anchors = []
    feature_map_height, feature_map_width = feature_size
    stride_h = image_size / feature_map_height
    stride_w = image_size / feature_map_width
    for y in range(feature_map_height):
        for x in range(feature_map_width):
            for anchor in base_anchors:
                width, height = anchor
                center_x = (x + 0.5) * stride_w
                center_y = (y + 0.5) * stride_h
                generated_anchors.append([center_x, center_y, width, height])
    return np.array(generated_anchors)

def compute_iou(box1, box2):
    x1 = np.maximum(box1[0], box2[0])
    y1 = np.maximum(box1[1], box2[1])
    x2 = np.minimum(box1[2], box2[2])
    y2 = np.minimum(box1[3], box2[3])
    intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union = box1_area + box2_area - intersection
    return intersection / union if union > 0 else 0

def compute_targets(anchors, gt_boxes, gt_labels, iou_threshold=0.5):
    if len(gt_boxes) == 0:
        num_anchors = anchors.shape[0]
        target_cls = np.zeros(num_anchors, dtype=int)
        target_reg = np.zeros((num_anchors, 4))
        positive_mask = np.zeros(num_anchors, dtype=bool)
        return target_cls, target_reg, positive_mask

    anchors_xyxy = np.array([cxcywh_to_xyxy(a) for a in anchors])
    gt_boxes_xyxy = np.array(gt_boxes)
    ious = np.array([[compute_iou(a, g) for g in gt_boxes_xyxy] for a in anchors_xyxy])
    max_ious = ious.max(axis=1)
    max_idx = ious.argmax(axis=1)
    positive_mask = max_ious > iou_threshold
    for i in range(len(gt_boxes)):
        if ious.shape[0] > 0:
            best_anchor_idx = ious[:, i].argmax()
            positive_mask[best_anchor_idx] = True
            max_idx[best_anchor_idx] = i
    target_cls = np.zeros(len(anchors), dtype=int)
    target_cls[positive_mask] = gt_labels[max_idx[positive_mask]]
    target_reg = np.zeros((len(anchors), 4))
    for i in range(len(anchors)):
        if positive_mask[i]:
            anchor = anchors[i]
            gt = gt_boxes[max_idx[i]]
            gt_cx = (gt[0] + gt[2]) / 2
            gt_cy = (gt[1] + gt[3]) / 2
            gt_w = gt[2] - gt[0]
            gt_h = gt[3] - gt[1]
            dx = (gt_cx - anchor[0]) / anchor[2]
            dy = (gt_cy - anchor[1]) / anchor[3]
            dw = np.log(gt_w / anchor[2])
            dh = np.log(gt_h / anchor[3])
            target_reg[i] = [dx, dy, dw, dh]
    return target_cls, target_reg, positive_mask

def cxcywh_to_xyxy(box):
    cx, cy, w, h = box
    x_min = cx - w / 2
    y_min = cy - h / 2
    x_max = cx + w / 2
    y_max = cy + h / 2
    return [x_min, y_min, x_max, y_max]

def detection_loss(pred_cls, pred_reg, target_cls, target_reg, positive_mask):
    B = pred_cls.size(0)
    A = pred_cls.size(1)
    cls_loss = F.cross_entropy(pred_cls.view(-1, pred_cls.size(-1)), target_cls.view(-1), reduction='mean')
    if positive_mask.sum() > 0:
        pred_reg_positive = pred_reg[positive_mask]
        target_reg_positive = target_reg[positive_mask]
        reg_loss = F.smooth_l1_loss(pred_reg_positive, target_reg_positive, reduction='mean')
    else:
        reg_loss = torch.tensor(0.0, device=pred_reg.device)
    return cls_loss + reg_loss

class DetectionDataset(Dataset):
    def __init__(self, images, bboxes, labels, transform, transform_type="albumentations"):
        self.images = images
        self.bboxes = bboxes
        self.labels = labels 
        self.transform = transform
        self.transform_type = transform_type

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
                raise ValueError("Invalid Transform Type")
        else:
            img = T.ToTensor()(img)  
        return (
            img,
            torch.tensor(bboxes, dtype=torch.float32),
            torch.tensor(labels, dtype=torch.long)
        )

    def __len__(self):
        return len(self.images)

def detection_transforms():
    transforms = A.Compose([
        A.Resize(256, 256),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.CLAHE(p=0.1),
        A.Blur(blur_limit=3, p=0.1),
        A.Normalize(mean=[0.5], std=[0.5]),
        ToTensorV2(),
    ], bbox_params=A.BboxParams(
        format='pascal_voc',
        min_visibility=0.3,
        label_fields=['labels']
    ))
    return transforms

def detection_training(epochs, model, train_dl, val_dl, optimizer=None, lr=3e-3, device=None):
    optimizer = optimizer or torch.optim.Adam(model.parameters(), lr=lr)
    device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    def compute_batch_targets(imgs, lbls, clss):
        target_cls_batch, target_reg_batch, positive_mask_batch = [], [], []
        for gt_boxes, gt_labels in zip(lbls, clss):
            target_cls, target_reg, positive_mask = compute_targets(model.anchors.cpu().numpy(), gt_boxes, gt_labels)
            target_cls_batch.append(torch.tensor(target_cls, dtype=torch.long))
            target_reg_batch.append(torch.tensor(target_reg, dtype=torch.float32))
            positive_mask_batch.append(torch.tensor(positive_mask, dtype=torch.bool))
        return (torch.stack(target_cls_batch).to(device),
                torch.stack(target_reg_batch).to(device),
                torch.stack(positive_mask_batch).to(device))

    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for i, (imgs, lbls, clss) in enumerate(train_dl):
            imgs = imgs.to(device)
            target_cls, target_reg, positive_mask = compute_batch_targets(imgs, lbls, clss)
            cls_scores, box_offsets = model(imgs)
            loss = detection_loss(cls_scores, box_offsets, target_cls, target_reg, positive_mask)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        train_loss /= len(train_dl)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for imgs, lbls, clss in val_dl:
                imgs = imgs.to(device)
                target_cls, target_reg, positive_mask = compute_batch_targets(imgs, lbls, clss)
                cls_scores, box_offsets = model(imgs)
                val_loss += detection_loss(cls_scores, box_offsets, target_cls, target_reg, positive_mask).item()
        val_loss /= len(val_dl)

        print(f'Epoch {epoch+1}/{epochs} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}')
    
    return model