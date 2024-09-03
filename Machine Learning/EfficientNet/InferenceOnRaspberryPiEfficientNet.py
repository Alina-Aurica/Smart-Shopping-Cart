import time
import torch
import torch.nn as nn
import cv2
from torchvision import models, transforms
import torch.quantization
from PIL import Image

# importare model fara ponderi
# modificare ultimul nivel
# importare modelul propriu
# setare pe mod evaluare
model = models.efficientnet_b7(pretrained=False)
model.classifier = nn.Sequential(
    nn.Dropout(p=0.5, inplace=True),
    nn.Linear(in_features=model.classifier[1].in_features, out_features=25, bias=True)
)
model_path = "efficientnet_model.pth"
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# aplicare quantizare dinamica
model = torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)

# set-up-ul camerei
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 36)

# pre-procesare
preprocess = transforms.Compose([
    transforms.Resize((260, 260)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

classes = (
    'CANDY', 'JUICE', 'VINEGAR', 'OIL', 'CHOCOLATE',
    'PASTA', 'RICE', 'MILK', 'SPICES', 'HONEY',
    'JAM', 'NUTS', 'CHIPS', 'SODA', 'COFFEE',
    'BEANS', 'TEA', 'CORN', 'CEREAL', 'CAKE',
    'SUGAR', 'WATER', 'FLOUR', 'TOMATO_SAUCE', 'FISH'
    )

# nu se mai propaga gradientii
with torch.no_grad():
    # citire si salvare imagine
    ret, image = cap.read()
    if not ret:
        raise RuntimeError("failed to read frame")
    cv2.imwrite("imageTest.png", image)

    # conversie din BGR in RGB si pre-procesare imaginie
    image = image[:, :, [2, 1, 0]]
    image = Image.fromarray(image)
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # calculare output si predictie
    output = model(input_batch)
    _, predicted = torch.max(output, 1)
    predicted_class_index = predicted.item()
    print(f'Predicted class: {classes[predicted_class_index]}')
