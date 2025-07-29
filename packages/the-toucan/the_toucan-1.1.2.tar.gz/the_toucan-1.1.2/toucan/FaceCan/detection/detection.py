import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import numpy as np
import torchvision.transforms as T
import torch.nn.functional as F
from tqdm import tqdm
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class DWBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, in_channels, 3, stride, 1, groups=in_channels, bias=False),
            nn.BatchNorm2d(in_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels, out_channels, 1, 1, 0, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
        self.shortcut = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 1, stride, bias=False),
            nn.BatchNorm2d(out_channels)
        ) if stride != 1 or in_channels != out_channels else nn.Identity()

    def forward(self, x):
        return self.conv(x) + self.shortcut(x)

class Detection(nn.Module):
    def __init__(self, num_classes=2, hidden_units=256, in_channels=1, max_faces=10):
        super().__init__()
        self.max_faces = max_faces
        self.num_classes = num_classes
        
        self.backbone = nn.Sequential(
            nn.Conv2d(in_channels, 64, 3, padding=1),
            nn.ReLU(),
            DWBlock(64, hidden_units),
            DWBlock(hidden_units, hidden_units),
            DWBlock(hidden_units, hidden_units),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        
        self.cls_head = nn.Linear(hidden_units, max_faces * num_classes)
        self.reg_head = nn.Linear(hidden_units, max_faces * 4)

    def forward(self, x):
        batch_size = x.size(0)
        features = self.backbone(x).view(batch_size, -1)
        
        cls_logits = self.cls_head(features).view(batch_size, self.max_faces, self.num_classes)
        bbox_deltas = self.reg_head(features).view(batch_size, self.max_faces, 4)
        return cls_logits, bbox_deltas

class ToucanDetectionLoss(nn.Module):
    def __init__(self, num_classes=2, bbox_weight=1.0, cls_weight=1.0):
        super().__init__()
        self.num_classes = num_classes
        self.bbox_weight = bbox_weight
        self.cls_weight = cls_weight
    
    def smooth_l1(self, pred, target):
        diff = torch.abs(pred - target)
        loss = torch.where(diff < 1.0, 0.5 * diff**2, diff - 0.5)
        return loss.sum(dim=1).mean()

    def forward(self, cls_logits, bbox_preds, targets):
        target_bboxes, target_labels = targets
        
        cls_loss = F.cross_entropy(
            cls_logits.view(-1, self.num_classes), 
            target_labels.view(-1),
            ignore_index=-1
        )
        
        mask = target_labels != -1
        valid_bbox_preds = bbox_preds[mask]
        valid_bbox_targets = target_bboxes[mask]
        
        if valid_bbox_preds.numel() > 0:
            bbox_loss = self.smooth_l1(valid_bbox_preds, valid_bbox_targets)
        else:
            bbox_loss = torch.tensor(0.0, device=cls_logits.device)
        
        return self.cls_weight * cls_loss + self.bbox_weight * bbox_loss

def get_transform():
    return T.Compose([
        T.Resize((256, 256)),
        T.RandomHorizontalFlip(p=0.5),
        T.ColorJitter(brightness=0.2, contrast=0.2),
        T.RandomGrayscale(p=0.1),
        T.GaussianBlur(kernel_size=3, sigma=(0.1, 2.0)),
        T.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
        T.ToTensor()
    ])

def get_eval_transform():
    return T.Compose([
        T.Resize((256, 256)),
        T.ToTensor()
    ])

class FaceDataset(Dataset):
    def __init__(self, image_paths, label_data, transform=None):
        self.image_paths = image_paths
        self.label_data = label_data
        self.transform = transform

    def __getitem__(self, idx):
        img = Image.open(self.image_paths[idx]).convert("L")
        bboxes, labels = self.label_data[idx]
        
        if self.transform:
            seed = np.random.randint(2147483647)
            torch.manual_seed(seed)
            img = self.transform(img)
            
            if isinstance(self.transform, T.Compose):
                new_bboxes = bboxes.copy()
                for t in self.transform.transforms:
                    if isinstance(t, T.RandomHorizontalFlip) and torch.rand(1) < 0.5:
                        new_bboxes = [[1.0 - box[2], box[1], 1.0 - box[0], box[3]] for box in new_bboxes]
                    elif isinstance(t, T.RandomAffine):
                        translate = t.translate if hasattr(t, 'translate') else (0, 0)
                        scale = t.scale if hasattr(t, 'scale') else (1, 1)
                        tx, ty = translate
                        scale_factor = np.random.uniform(scale[0], scale[1]) if isinstance(scale, tuple) else scale
                        new_bboxes = [[
                            (box[0] * scale_factor + tx) / scale_factor,
                            (box[1] * scale_factor + ty) / scale_factor,
                            (box[2] * scale_factor + tx) / scale_factor,
                            (box[3] * scale_factor + ty) / scale_factor
                        ] for box in new_bboxes]
                bboxes = new_bboxes
        
        bboxes = torch.tensor(bboxes, dtype=torch.float32) if bboxes else torch.zeros((0, 4))
        labels = torch.tensor(labels, dtype=torch.long) if labels else torch.full((0,), -1)
        return img, bboxes, labels

    def __len__(self):
        return len(self.image_paths)

def collate_fn(batch, max_faces=10):
    images, bboxes, labels = zip(*batch)
    images = torch.stack(images)
    
    padded_bboxes = []
    padded_labels = []
    for b, l in zip(bboxes, labels):
        if len(b) > max_faces:
            b = b[:max_faces]
            l = l[:max_faces]
        elif len(b) < max_faces:
            pad_size = max_faces - len(b)
            b = torch.cat([b, torch.zeros(pad_size, 4)])
            l = torch.cat([l, -torch.ones(pad_size, dtype=torch.long)])
        padded_bboxes.append(b)
        padded_labels.append(l)
        
    return images, (torch.stack(padded_bboxes), torch.stack(padded_labels))

def yolo_to_pascal_voc(yolo_bbox, img_size=256):
    cls_id, x_center, y_center, width, height = map(float, yolo_bbox)
    x_center *= img_size
    y_center *= img_size
    width *= img_size
    height *= img_size
    x_min = x_center - width / 2
    y_min = y_center - height / 2
    x_max = x_center + width / 2
    y_max = y_center + height / 2
    return [
        max(0.0, min(x_min / img_size, 1.0)),
        max(0.0, min(y_min / img_size, 1.0)),
        max(0.0, min(x_max / img_size, 1.0)),
        max(0.0, min(y_max / img_size, 1.0))
    ]

def process_labels(label_dir, img_size=256):
    labels = []
    for lbl_file in tqdm(sorted(os.listdir(label_dir))):
        with open(os.path.join(label_dir, lbl_file)) as f:
            bboxes = []
            classes = []
            for line in f:
                parts = line.strip().split()
                if len(parts) != 5:
                    continue
                bbox = yolo_to_pascal_voc(parts, img_size)
                bboxes.append(bbox)
                classes.append(int(parts[0]))
            labels.append((bboxes, classes))
    return labels

def train_one_epoch(model, optimizer, criterion, train_loader, device, epoch, num_epochs, accum_steps=2):
    model.train()
    total_loss = 0.0
    num_batches = len(train_loader)
    optimizer.zero_grad()
    
    progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{num_epochs}")
    for i, (images, (target_bboxes, target_labels)) in enumerate(progress_bar):
        images = images.to(device)
        target_bboxes = target_bboxes.to(device)
        target_labels = target_labels.to(device)
        
        cls_logits, bbox_preds = model(images)
        loss = criterion(cls_logits, bbox_preds, (target_bboxes, target_labels))
        loss = loss / accum_steps
        loss.backward()
        
        if (i + 1) % accum_steps == 0 or (i + 1) == num_batches:
            optimizer.step()
            optimizer.zero_grad()
        
        total_loss += loss.item() * accum_steps
        progress_bar.set_postfix({'loss': f"{loss.item() * accum_steps:.4f}"})
    
    avg_loss = total_loss / num_batches
    return avg_loss

def evaluate(model, criterion, val_loader, device):
    model.eval()
    total_loss = 0.0
    total_correct = 0
    total_valid = 0
    num_batches = len(val_loader)
    
    progress_bar = tqdm(val_loader, desc="Evaluating")
    with torch.no_grad():
        for images, (target_bboxes, target_labels) in progress_bar:
            images = images.to(device)
            target_bboxes = target_bboxes.to(device)
            target_labels = target_labels.to(device)
            
            cls_logits, bbox_preds = model(images)
            loss = criterion(cls_logits, bbox_preds, (target_bboxes, target_labels))
            
            preds = torch.argmax(cls_logits, dim=-1)
            mask = target_labels != -1
            total_correct += (preds[mask] == target_labels[mask]).sum().item()
            total_valid += mask.sum().item()
            
            total_loss += loss.item()
            progress_bar.set_postfix({'val_loss': f"{loss.item():.4f}"})
    
    avg_loss = total_loss / num_batches
    accuracy = total_correct / total_valid if total_valid > 0 else 0.0
    return avg_loss, accuracy

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    train_img_dir = "/kaggle/input/face-detection-dataset/images/train"
    val_img_dir = "/kaggle/input/face-detection-dataset/images/val"
    train_labels = process_labels("/kaggle/input/face-detection-dataset/labels/train")
    val_labels = process_labels("/kaggle/input/face-detection-dataset/labels/val")
    
    train_dataset = FaceDataset(
        [os.path.join(train_img_dir, f) for f in sorted(os.listdir(train_img_dir))],
        train_labels,
        transform=get_transform()
    )
    val_dataset = FaceDataset(
        [os.path.join(val_img_dir, f) for f in sorted(os.listdir(val_img_dir))],
        val_labels,
        transform=get_eval_transform()
    )
    
    train_loader = DataLoader(
        train_dataset, batch_size=8, shuffle=True,
        collate_fn=lambda b: collate_fn(b, max_faces=10)
    )
    val_loader = DataLoader(
        val_dataset, batch_size=8, shuffle=False,
        collate_fn=lambda b: collate_fn(b, max_faces=10)
    )
    
    model = Detection().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=1e-2)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)
    criterion = ToucanDetectionLoss(num_classes=2)
    num_epochs = 20
    best_val_loss = float('inf')
    
    for epoch in range(num_epochs):
        train_loss = train_one_epoch(model, optimizer, criterion, train_loader, device, epoch, num_epochs)
        val_loss, val_accuracy = evaluate(model, criterion, val_loader, device)
        scheduler.step()
        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Accuracy: {val_accuracy:.4f}")
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': train_loss,
                'val_loss': val_loss,
                'val_accuracy': val_accuracy,
            }, "/kaggle/working/best_checkpoint.pth")
        print(f"{epoch+1} | {train_loss:.2f} | {val_loss:.2f}")

def inference(model, image_path, transform, device):
    model.eval()
    img = Image.open(image_path).convert("L")
    img = transform(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        cls_logits, bbox_preds = model(img)
    
    cls_probs = torch.nn.functional.softmax(cls_logits, dim=-1)
    bbox_preds = bbox_preds.squeeze(0)
    
    results = []
    for i in range(cls_logits.size(1)):
        if cls_probs[0, i] > 0.5:
            results.append({
                "class_id": i,
                "score": cls_probs[0, i].item(),
                "bbox": bbox_preds[i].cpu().numpy().tolist()
            })
    
    return results

