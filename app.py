import os
import shutil
import time

from src.extract_text import extract_text
from src.extract_images import extract_images
from src.preprocess import clean_text, extract_key_points
from src.ai import generate_ddr
from src.report_generator import save_report


def clean_output():
    print("Cleaning previous outputs...")

    images_dir = os.path.join("output", "images")

    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)

    os.makedirs(images_dir, exist_ok=True)


def validate_inputs():
    if not os.path.exists("data/report.pdf"):
        raise FileNotFoundError("Missing file: data/report.pdf")

    if not os.path.exists("data/thermal.pdf"):
        raise FileNotFoundError("Missing file: data/thermal.pdf")


def main():
    start_time = time.time()

    print("Starting DDR pipeline...\n")

    try:
        validate_inputs()

        clean_output()

        inspection_path = "data/report.pdf"
        thermal_path = "data/thermal.pdf"

        print("Extracting text...")
        inspection_text = extract_text(inspection_path)
        thermal_text = extract_text(thermal_path)

        if not inspection_text.strip():
            raise ValueError("Inspection text extraction failed")

        print("Cleaning data...")
        inspection_text = clean_text(inspection_text)
        thermal_text = clean_text(thermal_text)

    
        print("Extracting key observations...")
        key_points = extract_key_points(inspection_text)

        
        print("Extracting images...")
        inspection_images = extract_images(inspection_path)
        thermal_images = extract_images(thermal_path)

        all_images = (inspection_images or []) + (thermal_images or [])

        if not all_images:
            print("Warning: No images extracted")

        print("Generating report...")
        report = generate_ddr(inspection_text, thermal_text, key_points)

        if not report or len(report.strip()) < 50:
            print("Warning: Weak report output, using fallback")
            report = "Report generation incomplete. Please verify input data."

        print("Saving report...")
        save_report(report, all_images)

        end_time = time.time()

        print("\nPipeline completed successfully.")
        print(f"Execution time: {round(end_time - start_time, 2)} seconds")

    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()