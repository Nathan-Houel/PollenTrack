import requests # type: ignore
import time
from datetime import datetime
import Send_folder
import os

def capture_image(api_url, save_path="captured_image.jpg"):
    image_endpoint = f"http://172.20.10.3:5000/api/v2/streams/snapshot"
    try:
        response = requests.get(image_endpoint, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        
        print(f"Image saved as {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error capturing image: {e}")

if __name__ == "__main__":
    API_URL = "http://172.20.10.3:5000/api/v2"

    date_str = datetime.now().strftime("%d_%m_%Y")
    folder_name = date_str
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Dossier créé : {folder_name}")
    else:
        print(f"Le dossier existe déjà : {folder_name}")
    
    IMAGE_PATH = folder_name + "/"
    for i in range(0,5):
        time.sleep(3)
        horodatage = datetime.now()
        timestamp = horodatage.strftime("%d-%m-%Y_%H-%M-%S")  # Format : DD-MM-YYYY_HH-MM-SS
        new_name = f"{timestamp}.jpg"
        name = os.path.join(IMAGE_PATH,new_name)
        capture_image(API_URL, name)

    Send_folder.envoyer_sur_huggingface(folder_name, "Images")
