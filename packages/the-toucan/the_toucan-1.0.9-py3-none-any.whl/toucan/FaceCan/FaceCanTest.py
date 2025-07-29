import pytest
import torch
import torch.nn as nn
import numpy as np
from unittest.mock import patch
from PIL import Image
import albumentations as A
from DetectionModel import Detection, DWBlock
from utils import (
    create_anchors, generate_anchors, cxcywh_to_xyxy, compute_iou, compute_targets,
    detection_loss, DetectionDataset, detection_transforms, detection_training
)

# Fixtures
@pytest.fixture
def model():
    return Detection(img_size=(256, 256), num_classes=2)

@pytest.fixture
def sample_image():
    return torch.randn(1, 1, 256, 256)  # Batch, channels, height, width

@pytest.fixture
def sample_boxes():
    return torch.tensor([[20, 20, 60, 60], [100, 100, 140, 140]], dtype=torch.float32)  # [x_min, y_min, x_max, y_max]

@pytest.fixture
def sample_labels():
    return torch.tensor([1, 1], dtype=torch.long)

@pytest.fixture
def dataset():
    images = ["dummy.jpg"]
    bboxes = [[[20, 20, 60, 60], [100, 100, 140, 140]]]
    labels = [[1, 1]]
    transform = detection_transforms()
    return DetectionDataset(images, bboxes, labels, transform=transform, transform_type="albumentations")

# Tests for utils.py
def test_create_anchors():
    anchor_sizes = [16, 32]
    aspect_ratios = [0.5, 1.0]
    anchors = create_anchors(anchor_sizes, aspect_ratios)
    assert anchors.shape == (4, 2)  # 2 sizes * 2 ratios
    assert torch.allclose(anchors[0], torch.tensor([16 * (0.5 ** 0.5), 16 / (0.5 ** 0.5)]))

def test_generate_anchors():
    base_anchors = torch.tensor([[16, 16]], dtype=torch.float32)
    feature_size = (16, 16)
    anchors = generate_anchors(base_anchors, feature_size, image_size=256)
    assert anchors.shape == (256, 4)  # 16 * 16 * 1 anchor
    assert torch.allclose(anchors[0], torch.tensor([8, 8, 16, 16]))  # First anchor at (0.5, 0.5) * stride

def test_cxcywh_to_xyxy():
    box = torch.tensor([50, 50, 20, 30], dtype=torch.float32)
    xyxy = cxcywh_to_xyxy(box)
    expected = torch.tensor([40, 35, 60, 65], dtype=torch.float32)
    assert torch.allclose(xyxy, expected)

def test_compute_iou():
    boxes1 = torch.tensor([[0, 0, 10, 10]], dtype=torch.float32)
    boxes2 = torch.tensor([[5, 5, 15, 15]], dtype=torch.float32)
    iou = compute_iou(boxes1, boxes2)
    expected_iou = 25 / (100 + 100 - 25)  # Intersection: 5*5, Union: 10*10 + 10*10 - 5*5
    assert torch.allclose(iou, torch.tensor([[expected_iou]]))

def test_compute_targets(sample_boxes, sample_labels):
    anchors = torch.tensor([
        [50, 50, 20, 20],
        [120, 120, 20, 20],
        [200, 200, 20, 20]
    ], dtype=torch.float32)
    target_cls, target_reg, positive_mask = compute_targets(anchors, sample_boxes, sample_labels, iou_threshold=0.5)
    assert target_cls.shape == (3,)
    assert target_reg.shape == (3, 4)
    assert positive_mask.shape == (3,)
    assert positive_mask[:2].all() and not positive_mask[2]  # First two anchors match, third doesn't
    assert target_cls[:2].equal(torch.tensor([1, 1]))  # Labels for positive anchors

def test_compute_targets_empty_gt():
    anchors = torch.tensor([[50, 50, 20, 20]], dtype=torch.float32)
    gt_boxes = torch.empty((0, 4), dtype=torch.float32)
    gt_labels = torch.empty((0,), dtype=torch.long)
    target_cls, target_reg, positive_mask = compute_targets(anchors, gt_boxes, gt_labels)
    assert target_cls.shape == (1,)
    assert target_reg.shape == (1, 4)
    assert positive_mask.shape == (1,)
    assert not positive_mask.any()

def test_detection_loss():
    pred_cls = torch.randn(2, 3, 2)  # Batch, anchors, classes
    pred_reg = torch.randn(2, 3, 4)
    target_cls = torch.tensor([[1, 0, 1], [0, 1, 0]], dtype=torch.long)
    target_reg = torch.randn(2, 3, 4)
    positive_mask = torch.tensor([[True, False, True], [False, True, False]], dtype=torch.bool)
    loss = detection_loss(pred_cls, pred_reg, target_cls, target_reg, positive_mask)
    assert loss.item() > 0  # Loss should be positive
    # Test with no positive anchors
    positive_mask = torch.zeros_like(positive_mask)
    loss = detection_loss(pred_cls, pred_reg, target_cls, target_reg, positive_mask)
    assert loss.item() > 0  # Only classification loss

@patch('PIL.Image.open')
def test_detection_dataset(mock_open, dataset):
    mock_img = Image.fromarray(np.random.randint(0, 255, (256, 256), dtype=np.uint8))
    mock_open.return_value = mock_img
    img, bboxes, labels = dataset[0]
    assert img.shape == (1, 256, 256)
    assert bboxes.shape == (2, 4)
    assert labels.shape == (2,)
    assert labels.dtype == torch.long

def test_detection_transforms():
    transform = detection_transforms(mean=0.5, std=0.5)
    img = np.random.randint(0, 255, (300, 300), dtype=np.uint8)
    bboxes = [[20, 20, 60, 60]]
    labels = [1]
    transformed = transform(image=img, bboxes=bboxes, labels=labels)
    assert transformed['image'].shape == (1, 256, 256)
    assert len(transformed['bboxes']) == len(bboxes)
    assert len(transformed['labels']) == len(labels)

# Tests for DetectionModel.py
def test_model_init(model):
    assert model.img_size == (256, 256)
    assert model.num_classes == 2
    assert len(model.cls_heads) == 2
    assert len(model.reg_heads) == 2
    assert model.anchors.shape[1] == 4  # [center_x, center_y, width, height]

def test_dwblock():
    block = DWBlock(in_channels=1, out_channels=32, stride=2)
    x = torch.randn(1, 1, 256, 256)
    out = block(x)
    assert out.shape == (1, 32, 128, 128)  # Stride 2 halves dimensions

def test_model_forward(model, sample_image):
    cls_scores, box_offsets = model(sample_image)
    num_anchors = 16 * 16 * 3 + 8 * 8 * 3  # Feature sizes (16,16) and (8,8) with 3 aspect ratios
    assert cls_scores.shape == (1, num_anchors, 2)  # Batch, anchors, classes
    assert box_offsets.shape == (1, num_anchors, 4)  # Batch, anchors, [dx, dy, dw, dh]

def test_decode_boxes(model):
    offsets = torch.tensor([[0.1, 0.1, 0.0, 0.0]], dtype=torch.float32)
    boxes = model.decode_boxes(offsets)
    assert boxes.shape == (1, 4)  # [x_min, y_min, x_max, y_max]
    anchor = model.anchors[0]
    expected_cx = anchor[0] + 0.1 * anchor[2]
    expected_cy = anchor[1] + 0.1 * anchor[3]
    expected_w = anchor[2]
    expected_h = anchor[3]
    expected = torch.tensor([
        expected_cx - expected_w / 2,
        expected_cy - expected_h / 2,
        expected_cx + expected_w / 2,
        expected_cy + expected_h / 2
    ])
    assert torch.allclose(boxes[0], expected)

def test_detect(model, sample_image):
    detections = model.detect(sample_image, conf_threshold=0.5, nms_threshold=0.5, max_detections=10)
    assert len(detections) == 1  # One image in batch
    assert detections[0].shape[1] == 5  # [x_min, y_min, x_max, y_max, score]
    assert detections[0].shape[0] <= 10  # Respect max_detections

def test_detection_training(model, dataset):
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=1)
    initial_params = [p.clone() for p in model.parameters()]
    model = detection_training(
        epochs=1,
        model=model,
        train_dl=dataloader,
        val_dl=dataloader,
        lr=1e-3,
        cls_weight=1.0,
        reg_weight=1.0
    )
    # Check that parameters have been updated
    for p1, p2 in zip(initial_params, model.parameters()):
        assert not torch.allclose(p1, p2)

if __name__ == '__main__':
    pytest.main()