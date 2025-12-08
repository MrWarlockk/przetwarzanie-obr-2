import io
import requests
from PIL import Image


def downloadImg():
    imgUrl = "https://upload.wikimedia.org/wikipedia/commons/2/2a/STS069-302-010_-_STS-069_-_Underexposed_-_DPLA_-_d4a340457c33446bd344a121dde4e385.jpg"
    header = {"User-Agent": "download-img"}
    response = requests.get(imgUrl, headers=header, timeout=15)
    response.raise_for_status()
    return response.content


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

if __name__ == "__main__":
    main()