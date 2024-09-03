import random
from sklearn.model_selection import train_test_split

# --- SPLIT DATASETS ---
images_with_labels_path = "D:/Facultate/ANUL 4/Licenta/Licenta/Proiect/splits/train"
images_folder_path = "D:/Facultate/ANUL 4/Licenta/Licenta/Proiect/images/"

# impartirea setului de date de train in train si validation - 80%-20% raportul
# raportul se respecta pentru fiecare clasa
def split_each_class(images_set):
    dataset_list = list(images_set)
    paths = []
    labels = []
    # fiecare linie din fisierul train.txt se imparte in path si label
    for item in dataset_list:
        if len(item) == 2:
            path, label = item
            paths.append(path)
            labels.append(label)
        else:
            print(f"Skipping invalid item with {len(item)} elements: {item}")

    # realizarea split-ului
    paths_train, paths_val, labels_train, labels_val = train_test_split(
        paths,
        labels,
        test_size=0.2,
        stratify=labels,
        random_state=42
    )

    # se formeaza seturile pentru train si split
    train_set = list(zip(paths_train, labels_train))
    val_set = list(zip(paths_val, labels_val))

    return train_set, val_set


# se primeste path-ul catre fisierul de train si numarul fisierului
def split_train_validation_file_function(path, n):
    # initializare images_set
    # folosim set ca sa eliminam duplicatele
    images_set = set()
    n_str = str(n)

    # se citeste fisierul
    with open(path + n_str + ".txt", 'r') as file:
        file_content = file.read()

    # se formeaza setul de tuple [path, label]
    content_tuple = tuple(item.strip() for item in file_content.split('\n'))
    for item in content_tuple:
        item_tuple = tuple(item.split(' '))
        images_set.add(item_tuple)

    # se realizeaza split-ul pe fiecare clasa
    images_train_set, images_validation_set = split_each_class(images_set)

    # se formeaza fisierele pentru train si validation
    with open('D:/Facultate/ANUL 4/Licenta/Licenta/Proiect/splits/train' + '0' + n_str + '.txt', 'w') as file:
        for item in images_train_set:
            if item[0] != '':
                file.write(str(item[0]) + ' ' + str(item[1]))
                file.write('\n')

    with open('D:/Facultate/ANUL 4/Licenta/Licenta/Proiect/splits/validation' + n_str + '.txt', 'w') as file:
        for item in images_validation_set:
            if item[0] != '':
                file.write(str(item[0]) + ' ' + str(item[1]))
                file.write('\n')

# realizarea split-urilor
split_train_validation_file_function(images_with_labels_path, 0)
split_train_validation_file_function(images_with_labels_path, 1)
split_train_validation_file_function(images_with_labels_path, 2)
split_train_validation_file_function(images_with_labels_path, 3)
split_train_validation_file_function(images_with_labels_path, 4)

# --- RETURN TUPLE OF DATASET ---

# crearea unei tuple de tuple de forma [path, label]
def return_tuple_of_dataset(path, n):
    images_tuple = tuple()
    n_str = str(n)
    with open(path + n_str + ".txt", 'r') as file:
        file_content = file.read()

    content_tuple = tuple(item.strip() for item in file_content.split('\n'))
    for item in content_tuple:
        item_tuple = tuple(item.split(' '))
        images_tuple = images_tuple + (item_tuple,)

    images_tuple = images_tuple[:-1]
    return images_tuple