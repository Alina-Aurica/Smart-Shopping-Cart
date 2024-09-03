import torch
import torch.nn as nn
import torchvision.models as models
import torchmetrics
from torch.utils.tensorboard import SummaryWriter
from torchvision.models import *
from tqdm import tqdm
from LoadImagesResNet import *

# importare model ResNet18, impreuna cu weight-urile potrivite
# modificarea ultimului layer
model = models.resnet18(ResNet18_Weights.DEFAULT)
model.fc = nn.Linear(model.fc.in_features, 25)

# activare antrenare pe GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)

# stabilire criterion, optimizer si LR
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
# optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

# augmentarea imaginilor
augmentation = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
])

num_epochs = 20

# -- TRAINING PART --
def train_function():
    # initializare acuratete
    accuracy_metric = torchmetrics.Accuracy(task="multiclass", num_classes=25).to(device)
    for epoch in range(num_epochs):
        # afiseaza procesul de invatare ca pe o bara de incarcare
        pbar = tqdm(enumerate(train_loader, 0),
                    unit='image',
                    total=len(train_loader),
                    smoothing=0)

        # activam antrenarea
        model.train()
        for i, data in pbar:
            # pentru fiecare imagine se ia separat eticheta si imaginea
            inputs, labels = data
            # se augmenteaza imaginea
            inputs = augmentation(inputs)

            inputs = inputs.to(device)
            labels = labels.to(device)

            # Forward pass
            # se calculeaza output-ul si loss-ul
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Backward pass si optimizarea gradientilor
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # se realizeaza predictia
            # se calculeaza acuratetea
            _, predicted = torch.max(outputs, 1)
            accuracy_metric.update(predicted, labels)
            pbar.set_description(
                'Train [ E {}, L {:.4f}]'.format(epoch + 1, float(loss) / (i + 1)))

        # se calculeaza acuratetea finala
        accuracy = accuracy_metric.compute() * 100
        print('Train [E {}, Accuracy: {:.2f}%]'.format(epoch + 1, accuracy))
        accuracy_metric.reset()

        val_function()


def val_function():
    # se seteaza modelul pe mod de evaluare
    model.eval()

    # se initiaza metricile de evaluare
    accuracy_metric = torchmetrics.Accuracy(task="multiclass", num_classes=25).to(device)
    precision_metric = torchmetrics.Precision(task="multiclass", num_classes=25, average='macro').to(device)
    recall_metric = torchmetrics.Recall(task="multiclass", num_classes=25, average='macro').to(device)
    f1_score_metric = torchmetrics.F1Score(task="multiclass", num_classes=25, average='macro').to(device)
    total_loss = 0.0

    pbar = tqdm(enumerate(val_loader, 0),
                unit='image',
                total=len(val_loader),
                smoothing=0)

    # nu se mai propaga gradientii
    with torch.no_grad():
        for i, data in pbar:
            # pentru fiecare imagine se ia separat eticheta si imaginea
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)

            # se calculeaza output-ul
            # se actualizeaza loss-ul
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item()

            # se realizeaza predictia
            # se calculeaza acuratetea, precizia, recall-ul si f1_score
            _, predicted = torch.max(outputs.data, 1)

            accuracy_metric.update(predicted, labels)
            precision_metric.update(predicted, labels)
            recall_metric.update(predicted, labels)
            f1_score_metric.update(predicted, labels)

    # se calculeaza metricile totale
    total_loss = total_loss / len(val_loader)
    accuracy = accuracy_metric.compute() * 100
    precision = precision_metric.compute() * 100
    recall = recall_metric.compute() * 100
    f1_score = f1_score_metric.compute() * 100

    print('Validation [Loss: {:.4f}, Accuracy: {:.2f}%, Precision: {:.2f}%, Recall: {:.2f}%, F1_score: {:.2f}%]'.format(
        total_loss, accuracy, precision, recall, f1_score))
    # resetare pe mod de training
    model.train()


# apelare functie de training
train_function()
# salvare model
torch.save(model.state_dict(), 'resnet_model.pth')
