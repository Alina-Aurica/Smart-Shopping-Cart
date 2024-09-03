import torch
import torch.nn as nn
from tqdm import tqdm
import torchmetrics
import torchvision.models as models

from LoadImagesResNet import *

# importare baza modelului, fara ponderi
# modificare ultimului nivel
# importarea modelului re-antrenat
model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, 25)
model_path = 'resnet_model.pth'
model.load_state_dict(torch.load(model_path))

# activare testare pe GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


def test_function():
    # se seteaza modelul pe mod de evaluare
    model.eval()

    accuracy_metric = torchmetrics.Accuracy(task="multiclass", num_classes=25).to(device)
    precision_metric = torchmetrics.Precision(task="multiclass", num_classes=25, average='macro').to(device)
    recall_metric = torchmetrics.Recall(task="multiclass", num_classes=25, average='macro').to(device)
    f1_score_metric = torchmetrics.F1Score(task="multiclass", num_classes=25, average='macro').to(device)
    # se calculeaza pentru fiecare clasa acuratetea
    # initializarea valorilor
    correct_pred = {classname: 0 for classname in classes}
    total_pred = {classname: 0 for classname in classes}

    pbar = tqdm(enumerate(test_loader, 0),
                unit='image',
                total=len(test_loader),
                smoothing=0)

    # nu se mai propaga gradientii
    with torch.no_grad():
        for i, data in pbar:
            images, labels = data

            images = images.to(device)
            labels = labels.to(device)

            # se calculeaza output-ul si predictia
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)

            # se calculeaza metricile
            accuracy_metric.update(predicted, labels)
            precision_metric.update(predicted, labels)
            recall_metric.update(predicted, labels)
            f1_score_metric.update(predicted, labels)

            # se calculeaza acuratetea pentru fiecare clasa
            for label, prediction in zip(labels, predicted):
                if label == prediction:
                    correct_pred[classes[label]] += 1
                total_pred[classes[label]] += 1

    # se calculeaza predictia
    accuracy = accuracy_metric.compute() * 100
    precision = precision_metric.compute() * 100
    recall = recall_metric.compute() * 100
    f1_score = f1_score_metric.compute() * 100

    accuracy_metric.reset()
    precision_metric.reset()
    recall_metric.reset()
    f1_score_metric.reset()

    print(f'Accuracy: {accuracy:.2f}')
    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1 Score: {f1_score:.2f}')

    for classname, correct_count in correct_pred.items():
        accuracy = 100 * float(correct_count) / total_pred[classname]
        print(f'Accuracy for class: {classname:5s} is {accuracy:.1f} %')


# apelare functie de test
test_function()
