# The new config inherits a base config to highlight the necessary modification
_base_ = 'detectors/htc_r50_rfp_1x_coco.py'

# We also need to change the num_classes in head to match the dataset's annotation
model = dict(
        type = 'MaskRCNN',
        backbone = dict(
            type = 'ResNet',
            depth = 50,
            num_stages = 4,
            out_indices = (0, 1, 2, 3),
            in_channels = 3,
            frozen_stages = 1,
            norm_cfg = dict(
                type = 'BN',
                requires_grad = True
            ),
            norm_eval = True,
            style = 'pytorch',
            init_cfg = dict(
                type = 'Pretrained',
                checkpoint = 'torchivision://resnet50'
            )
        ),
        neck = dict(
            type = 'FPN',
            in_channels = [256, 512, 1024, 2048],
            out_channels = 256,
            num_outs = 5
        ),
        rpn_head = dict(
            type = 'RPNHead',
            in_channels = 256,
            feat_channels = 256,
            anchor_generator = dict
        ),
        train_cfg=dict(),
        test_cfg=dict()
    )
)

# Modify dataset related settings
dataset_type = 'CocoDataset'
classes = ('HolePairLeft', 'HolePairRight', 'ACHole')
data = dict(
    train=dict(
        img_prefix='data/train/',
        classes=classes,
        ann_file='data/train/train.json'),
    val=dict(
        img_prefix='data/val/',
        classes=classes,
        ann_file='data/val/val.json'),
    test=dict(
        img_prefix='data/test/',
        classes=classes,
        ann_file='data/test/test.json'))

# We can use the pre-trained Mask RCNN model to obtain higher performance
load_from = 'http://download.openmmlab.com/mmdetection/v2.0/detectors/detectors_htc_r50_1x_coco/detectors_htc_r50_1x_coco-329b1453.pth'