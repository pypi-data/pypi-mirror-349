# src/imgannotator/filters.py
import os
from PIL import Image, ImageFilter
import cv2

def apply_filter(folder: str, filter_name: str):
    for fname in os.listdir(folder):
        if fname.lower().endswith((".jpg", ".png")):
            path = os.path.join(folder, fname)
            img = Image.open(path)
            # Pillow filter example
            img = img.filter(getattr(ImageFilter, filter_name))
            img.save(path)
            # OpenCV example: convert to grayscale
            cv_img = cv2.imread(path)
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(path, gray)
