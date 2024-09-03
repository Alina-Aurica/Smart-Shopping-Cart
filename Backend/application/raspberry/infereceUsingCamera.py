import torch
import torch.nn as nn
import cv2
from torchvision import models, transforms
import torch.quantization
from PIL import Image

# se importa un schemete de model de EfficientNet_b7
# se modifica ultimul layer sa corespunda cu numarul de clase pe care il avem
# se incarca modelul re-antrenat pe setul nou de date
# se seteaza cu o executie pe CPU
# se seteaza pe mod de evaluare
model = models.efficientnet_b7(pretrained=False)
model.classifier = nn.Sequential(nn.Dropout(p=0.5, inplace=True),
                                 nn.Linear(in_features=2560, out_features=25, bias=True))
model_path = "efficientnet_model_4LR_Adam_aug_v5.pth"
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# se aplica optimizarea prin cuantizare
model = torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)

# pre-procesarile folosite la formarea dataloaderelor de train
preprocess = transforms.Compose([
    transforms.Resize((260, 260)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# clasele
classes = (
    'CANDY', 'JUICE', 'VINEGAR', 'OIL', 'CHOCOLATE',
    'PASTA', 'RICE', 'MILK', 'SPICES', 'HONEY',
    'JAM', 'NUTS', 'CHIPS', 'SODA', 'COFFEE',
    'BEANS', 'TEA', 'CORN', 'CEREAL', 'CAKE',
    'SUGAR', 'WATER', 'FLOUR', 'TOMATO_SAUCE', 'FISH'
)

# metoda de rulare de inferente - returneaza clasa produsului
def run_inference():
    # setup-ul camerei - pentru capturi video
    # se conecteaza la camera de pe portul 1
    # se seteaza dimensiunile imaginii
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)

    with torch.no_grad():
        # citim imaginea si dupa o salvam
        # ret - indica daca cadrul a fost citit cu succes (True sau False)
        ret, image = cap.read()
        if not ret:
            raise RuntimeError("failed to read frame")
        cv2.imwrite("imageTest.png", image)

        # conversie din BGR in RGB
        # conversie din array in imafine
        # si preprocesarea imaginii
        image = image[:, :, [2, 1, 0]]
        image = Image.fromarray(image)
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)

        # optinerea output-ului retelei
        # si realizarea predictiei
        output = model(input_batch)
        _, predicted = torch.max(output, 1)
        predicted_class_index = predicted.item()
        print(f'Predicted class: {classes[predicted_class_index]}')
        return classes[predicted_class_index]
