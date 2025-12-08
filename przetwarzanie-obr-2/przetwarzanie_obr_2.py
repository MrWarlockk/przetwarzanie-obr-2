import io
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def downloadImg():
    imgUrl = "https://upload.wikimedia.org/wikipedia/commons/2/2a/STS069-302-010_-_STS-069_-_Underexposed_-_DPLA_-_d4a340457c33446bd344a121dde4e385.jpg"
    header = {"User-Agent": "download-img"}
    response = requests.get(imgUrl, headers=header, timeout=15)
    response.raise_for_status()
    return response.content

def showHistogram(img):
    imgArr = np.array(img)

    imgLumin = (0.2126 * imgArr[:,:,0] + 0.7152 * imgArr[:,:,1] + 0.0722 * imgArr[:,:,2] ).astype(np.uint8)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    axeAll = axes[0]
    axeRed   = axes[1]
    axeGreen   = axes[2]
    axeBlue   = axes[3]

    # Wszystkie kolory razem
    axeAll.hist(imgLumin.flatten(), bins=256, range=(0, 255))
    axeAll.set_title("Jasnosc")
    axeAll.set_xlim(0, 255)

    #Czerwony histogram
    axeRed.hist(imgArr[:, :, 0].flatten(), bins=256, range=(0, 255), color='red')
    axeRed.set_title("Kanal czerwony")
    axeRed.set_xlim(0, 255)

    #Zielony histogram
    axeGreen.hist(imgArr[:, :, 1].flatten(), bins=256, range=(0, 255), color='green')
    axeGreen.set_title("Kanal zielony")
    axeGreen.set_xlim(0, 255)

    #Niebieski histogram
    axeBlue.hist(imgArr[:, :, 2].flatten(), bins=256, range=(0, 255), color='blue')
    axeBlue.set_title("Kanal niebieski")
    axeBlue.set_xlim(0, 255)

    plt.show()



def main():
    try:
        imgRet = downloadImg()
    except Exception as e:
        print(f"Error downloading image: {e}")
        return
    print("Image downloaded successfully.")
    try:
        img = Image.open(io.BytesIO(imgRet)).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    print("Image loaded successfully.")
    img.show()

    showHistogram(img)

if __name__ == "__main__":
    main()