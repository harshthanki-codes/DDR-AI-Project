import fitz  # PyMuPDF
import os
import re


def detect_area(page_text):
    text = page_text.lower()

    if "hall" in text:
        return "hall"
    elif "bedroom" in text:
        return "bedroom"
    elif "kitchen" in text:
        return "kitchen"
    elif "bathroom" in text or "toilet" in text:
        return "bathroom"
    elif "balcony" in text:
        return "balcony"
    else:
        return "general"



def clean_filename(name):
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name.lower()


# Main Funtion
def extract_images(pdf_path, output_folder="output/images"):
    os.makedirs(output_folder, exist_ok=True)

    doc = fitz.open(pdf_path)
    image_paths = []

    image_counter = {}

    for page_index in range(len(doc)):
        page = doc[page_index]

        # Extract page text for context
        page_text = page.get_text()
        area = detect_area(page_text)
        area = clean_filename(area)

        # Initializing counter for each area
        if area not in image_counter:
            image_counter[area] = 1

        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            try:
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                # SMART NAMING
                image_name = f"{area}_img_{image_counter[area]}.png"
                image_path = os.path.join(output_folder, image_name)

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                image_paths.append(image_path)
                image_counter[area] += 1

            except Exception as e:
                print(f"Skipping image (page {page_index+1}): {e}")

    return image_paths