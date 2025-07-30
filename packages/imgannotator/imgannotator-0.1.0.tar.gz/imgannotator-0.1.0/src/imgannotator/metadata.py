# src/imgannotator/metadata.py
import os
import piexif
from PIL import Image

def embed_metadata(folder: str, label: str):
    for fname in os.listdir(folder):
        if fname.lower().endswith((".jpg",)):
            path = os.path.join(folder, fname)
            img = Image.open(path)
            exif_dict = piexif.load(img.info.get("exif", b""))
            user_comment = label.encode()
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = user_comment
            exif_bytes = piexif.dump(exif_dict)
            img.save(path, exif=exif_bytes)
            print(f"Metadata embedded in {fname}")