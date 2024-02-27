from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import pytesseract

EXTRACTED_WORDS = []


def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    lines = text.splitlines()
    for line in lines:
        words = line.split()
        if words:
            sentence = ' '.join(words)
            EXTRACTED_WORDS.append(sentence)


def extract_text_from_images(file_paths, progress_callback=None):
    with ThreadPoolExecutor() as executor:
        for i, _ in enumerate(tqdm(executor.map(extract_text_from_image, file_paths), total=len(file_paths))):
            if progress_callback:
                progress = (i + 1) / len(file_paths) * 100
                progress_callback(progress)
