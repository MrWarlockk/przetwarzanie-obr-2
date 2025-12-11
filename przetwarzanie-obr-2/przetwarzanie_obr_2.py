import io
from re import S
import requests
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def downloadImg():
    imgUrl = "https://upload.wikimedia.org/wikipedia/commons/7/77/Magic_lilies_lycoris_squamigera-_underexposed_fill_flash-_indianapolis_in_usa_%2811%29.JPG"
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

def calculateScore(img):
    imgArr = np.array(img)
    imgLumin = (0.2126 * imgArr[:,:,0] + 0.7152 * imgArr[:,:,1] + 0.0722 * imgArr[:,:,2] ).astype(np.uint8)
    pixelCount = imgLumin.size

    nearZero = np.sum(imgLumin < 10)
    near255 = np.sum(imgLumin > 245)

    if(nearZero | near255) < (0.05 * pixelCount):
        return 0
    else:
        if(nearZero | near255) < (0.1 * pixelCount):
            return 1
        else:
            return 2

def fixExposure(img, score):
    if score == 0:
        return img

    if score == 1:
        gamma = 0.8

    if score == 2:
        gamma = 0.6

    imgArr = np.array(img).astype(np.float32) / 255.0
    imgArr = np.power(imgArr, gamma)
    imgArr = (imgArr * 255).astype(np.uint8)
    return Image.fromarray(imgArr)




def main():
    try:
        imgRet = downloadImg()
    except Exception as e:
        print(f"Blad podczas pobierania obrazu: {e}")
        return
    print("Obraz pobrany poprawnie.")
    try:
        img = Image.open(io.BytesIO(imgRet)).convert("RGB")
    except Exception as e:
        print(f"Blad podczas wczytywania obrazu: {e}")
        return

    print("Obraz wczytany pomyslnie.")
    img.show()

    print("Ocena jakosci obrazu (ekspozycja):")
    score = calculateScore(img)

    print("Poprawa ekspozycji obrazu (jezeli jest taka potrzeba)...")
    img = fixExposure(img, score)
    img.show()

    print(f"Wynik oceny: {score} (0 - Dobra jakosc obrazu, 1 - Srednia jakosc obrazu, 2 - Zla jakosc obrazu)")
    calculateScore(img)
    showHistogram(img)

if __name__ == "__main__":
    main()