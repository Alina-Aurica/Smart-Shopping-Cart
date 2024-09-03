import numpy as np
from PIL import Image
import os

images_folder_path = "D:/Facultate/ANUL 4/Licenta/Licenta/Proiect/images/"

classes = ('CANDY', 'JUICE', 'VINEGAR', 'OIL', 'CHOCOLATE',
           'PASTA', 'RICE', 'MILK', 'SPICES', 'HONEY',
           'JAM', 'NUTS', 'CHIPS', 'SODA', 'COFFEE',
           'BEANS', 'TEA', 'CORN', 'CEREAL', 'CAKE',
           'SUGAR', 'WATER', 'FLOUR', 'TOMATO_SAUCE', 'FISH'
           )


# calcularea totalului de poze dintr-un folder
def count_photos_in_folder(folder_path):
    photo_extension = '.png'
    number_of_photos = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(photo_extension):
                number_of_photos += 1

    return number_of_photos


# calcularea mean and std pentru fiecare canal RGB
def mean_and_standard_deviation():
    total_pixels_photos = 0
    sum_red = 0
    sum_green = 0
    sum_blue = 0
    sum_square_diff_red = 0
    sum_square_diff_green = 0
    sum_square_diff_blue = 0
    image_array = None

    # calcularea mediei pe fiecare canal
    for class_name in classes:
        class_path = os.path.join(images_folder_path, class_name)

        # calcularea numarului de poze fiecare folder
        number_of_photos = count_photos_in_folder(class_path)
        for i in range(number_of_photos):
            class_path_photo = os.path.join(class_path, f"{class_name}{i:04d}.png")
            image = Image.open(class_path_photo)

            # formatul de la image_array HxWxC
            image_array = np.array(image)
            # verifica daca sunt 3 canale
            if image_array.ndim == 3 and image_array.shape[2] == 3:
                red_channel = image_array[:, :, 0]
                green_channel = image_array[:, :, 1]
                blue_channel = image_array[:, :, 2]

                # calculeaza numarul de pixeli pentru fiecare canal
                sum_red += np.sum(red_channel)
                sum_green += np.sum(green_channel)
                sum_blue += np.sum(blue_channel)

        # calculeaza numarul total de pixeli
        total_pixels_photos += number_of_photos * image_array.shape[0] * image_array.shape[1]

    # media pentru fiecare canal - pentru tot setul de date
    mean_red = sum_red / total_pixels_photos
    mean_green = sum_green / total_pixels_photos
    mean_blue = sum_blue / total_pixels_photos

    # calcularea deviatiei standard pe fiecare canal
    for class_name in classes:
        class_path = os.path.join(images_folder_path, class_name)

        # calcularea numarului de poze fiecare folder
        number_of_photos = count_photos_in_folder(class_path)
        for i in range(number_of_photos):
            class_path_photo = os.path.join(class_path, f"{class_name}{i:04d}.png")
            image = Image.open(class_path_photo)

            image_array = np.array(image)
            if image_array.ndim == 3 and image_array.shape[2] == 3:
                red_channel = image_array[:, :, 0]
                green_channel = image_array[:, :, 1]
                blue_channel = image_array[:, :, 2]

                # calculeaza suma patratelor diferentelorpentru fiecare canal
                sum_square_diff_red += np.sum((red_channel - mean_red) ** 2)
                sum_square_diff_green += np.sum((green_channel - mean_green) ** 2)
                sum_square_diff_blue += np.sum((blue_channel - mean_blue) ** 2)

    # deviatia standard pentru fiecare canal - pentru tot setul de date
    std_dev_red = np.sqrt(sum_square_diff_red / total_pixels_photos)
    std_dev_green = np.sqrt(sum_square_diff_green / total_pixels_photos)
    std_dev_blue = np.sqrt(sum_square_diff_blue / total_pixels_photos)

    # normalizarea si returnarea valorilor
    return (mean_red / 255.0, mean_green / 255.0, mean_blue / 255.0,
            std_dev_red / 255.0, std_dev_green / 255.0, std_dev_blue / 255.0)


mean_red, mean_green, mean_blue, std_dev_red, std_dev_green, std_dev_blue = mean_and_standard_deviation()
print("Mean red: " + str(mean_red))
print("Mean green: " + str(mean_green))
print("Mean blue: " + str(mean_blue))
print("Std_dev red: " + str(std_dev_red))
print("Std_dev green: " + str(std_dev_green))
print("Std_dev blue: " + str(std_dev_blue))
