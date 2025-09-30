import cv2
from os import listdir

def measure_blurriness(image):
    """determine the blurriness of an image using Laplacian filter

    Args:
        image_path (_string_): path of the image

    Returns:
        _float_: Laplacian variance
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

    return laplacian

if __name__ == "__main__" :

    sample_directory = "samples"
    directory_list = listdir(sample_directory)

    with open("blurriness/data.txt", "w") as text_file:
        text_file.write("Blurriness rate of image samples\n")
        text_file.write("--------------------------\n\n")

        for dir in directory_list :
            directory = sample_directory + "/" + dir + "/cropped_image"
            text_file.write("Directory : " + directory + "\n\n")
            for file in listdir(directory) :
                blurriness = measure_blurriness(directory + "/" + file)
                text_file.write(file + " : " + str(blurriness) + "\n")
            text_file.write("--------------------------\n")
            text_file.write("\n")