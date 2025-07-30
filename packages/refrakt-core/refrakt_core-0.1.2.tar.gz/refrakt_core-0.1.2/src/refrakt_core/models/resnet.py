import torch.nn as nn
from refrakt_core.registry.model_registry import register_model
from refrakt_core.models.templates.models import BaseClassifier
from refrakt_core.utils.classes.resnet import ResidualBlock, BottleneckBlock

class ResNet(BaseClassifier):
    def __init__(
        self, block, layers, in_channels=3, num_classes=10, model_name="resnet"
    ):
        super(ResNet, self).__init__(num_classes=num_classes, model_name=model_name)
        self.inplanes = 64
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(),
        )
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer0 = self._make_layer(block, 64, layers[0], stride=1)
        self.layer1 = self._make_layer(block, 128, layers[1], stride=2)
        self.layer2 = self._make_layer(block, 256, layers[2], stride=2)
        self.layer3 = self._make_layer(block, 512, layers[3], stride=2)
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, num_classes)

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes, kernel_size=1, stride=stride),
                nn.BatchNorm2d(planes),
            )
        layers = [block(self.inplanes, planes, stride, downsample)]
        self.inplanes = planes
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.maxpool(x)
        x = self.layer0(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)

        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)

        return x

@register_model("resnet18")
class ResNet18(ResNet):
    def __init__(self, in_channels=3, num_classes=10):
        super().__init__(
            block=ResidualBlock,
            layers=[2, 2, 2, 2],
            in_channels=in_channels,
            num_classes=num_classes
        )


@register_model("resnet50")
class ResNet50(ResNet):
    def __init__(self, in_channels=3, num_classes=10):
        super().__init__(
            block=BottleneckBlock, 
            layers=[3, 4, 6, 3],
            in_channels=in_channels,
            num_classes=num_classes
        )

@register_model("resnet101")
class ResNet101(ResNet):
    def __init__(self, in_channels=3, num_classes=10):
        super().__init__(
            block=BottleneckBlock,
            layers=[3, 4, 23, 3],
            in_channels=in_channels,
            num_classes=num_classes
        )

@register_model("resnet152")
class ResNet152(ResNet):
    def __init__(self, in_channels=3, num_classes=10):
        super().__init__(
            block=BottleneckBlock,
            layers=[3, 8, 36, 3],
            in_channels=in_channels,
            num_classes=num_classes
        )