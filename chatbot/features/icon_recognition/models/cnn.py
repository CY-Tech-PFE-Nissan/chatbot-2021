import torch.nn as nn


class CNN(nn.Module):
    def __init__(self, n_classes=4):
        super(CNN, self).__init__()
        self.features = nn.Sequential(
            # 1x64x64
            nn.Conv2d(1, 16, 5, padding=2),
            nn.Dropout(0.5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # 16x32x32
            nn.Conv2d(16, 32, 3, padding=1),
            nn.Dropout(0.5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # 32x16x16
            nn.Conv2d(32, 64, 3, padding=1),
            nn.Dropout(0.5),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # 64x8x8
        )
        self.dropout = nn.Dropout(0.5)
        self.classifier = nn.Sequential(
            nn.Linear(64 * 8 * 8, 512),
            nn.Dropout(0.5),
            nn.ReLU(inplace=True),
            nn.Linear(512, n_classes),
        )

    def forward(self, inputs):
        x = self.features(inputs)
        x = x.view(-1, 4096)
        x = self.dropout(x)
        x = self.classifier(x)
        return x
