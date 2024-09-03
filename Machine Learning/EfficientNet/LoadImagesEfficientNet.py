from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from SplitDatasets import *


# --- COSTUM IMAGES ---
class CustomImageDataset(Dataset):
    # data - lista de tuple de forma [path, label]
    # transform - preprocesarile aplicate
    def __init__(self, data, transform=None):
        self.data = data
        self.transform = transform

    # returneaza lungimea setului de date
    def __len__(self):
        return len(self.data)

    # metoda care returneaza imaginea pre-procesata si eticheta pentru un index dat
    def __getitem__(self, idx):
        (img_path, class_id) = self.data[idx]
        class_id_number = int(class_id)
        image = Image.open(images_folder_path + img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, class_id_number


# --- PRE-PROCESS IMAGES ---
transform = transforms.Compose([
    transforms.Resize((260, 260)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# --- DATASETS ---
train_data = return_tuple_of_dataset("D:/Facultate/ANUL 4/Licenta/Proiect/splits/train", '00')
val_data = return_tuple_of_dataset("D:/Facultate/ANUL 4/Licenta/Proiect/splits/validation", 0)
test_data = return_tuple_of_dataset("D:/Facultate/ANUL 4/Licenta/Proiect/splits/test", 0)

train_dataset = CustomImageDataset(train_data, transform=transform)
val_dataset = CustomImageDataset(val_data, transform=transform)
test_dataset = CustomImageDataset(test_data, transform=transform)

# --- BATCH_SIZE ---
batch_size = 16

# --- DATALOADERS ---
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# --- CLASSES ---
classes = ('CANDY', 'JUICE', 'VINEGAR', 'OIL', 'CHOCOLATE',
           'PASTA', 'RICE', 'MILK', 'SPICES', 'HONEY',
           'JAM', 'NUTS', 'CHIPS', 'SODA', 'COFFEE',
           'BEANS', 'TEA', 'CORN', 'CEREAL', 'CAKE',
           'SUGAR', 'WATER', 'FLOUR', 'TOMATO_SAUCE', 'FISH'
           )
