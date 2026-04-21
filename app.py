import os
import shutil
import time

from src.extract_text import extract_text
from src.extract_images import extract_images
from src.preprocess import clean_text, extract_key_points
from src.ai import generate_ddr
from src.report_generator import save_report


# Cleaned output directory
def clean_output():
    print("Cleaning previous outputs...")

    images_dir = os.path.join("output", "images")

    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)

    os.makedirs(images_dir, exist_ok=True)


# Validates required input files
def validate_inputs():
    if not os.path.exists("data/report.pdf"):
        raise FileNotFoundError("Missing file: data/report.pdf")

    if not os.path.exists("data/thermal.pdf"):
        raise FileNotFoundError("Missing file: data/thermal.pdf")


def main():
    start_time = time.time()

    print("Starting DDR pipeline...\n")

    try:
        # Step 0: Validate inputs
        validate_inputs()

        # Step 1: Clean output
        clean_output()

        inspection_path = "data/report.pdf"
        thermal_path = "data/thermal.pdf"

        # Step 2: Extract text
        print("Extracting text...")
        inspection_text = extract_text(inspection_path)
        thermal_text = extract_text(thermal_path)

        if not inspection_text.strip():
            raise ValueError("Inspection text extraction failed")

        # Step 3: Clean data
        print("Cleaning data...")
        inspection_text = clean_text(inspection_text)
        thermal_text = clean_text(thermal_text)

        # Step 4: Extract key points
        print("Extracting key observations...")
        key_points = extract_key_points(inspection_text)

        # Step 5: Extract images
        print("Extracting images...")
        inspection_images = extract_images(inspection_path)
        thermal_images = extract_images(thermal_path)

        # Merge image lists safely
        all_images = (inspection_images or []) + (thermal_images or [])

        if not all_images:
            print("Warning: No images extracted")

        # Step 6: Generating report
        print("Generating report...")
        report = generate_ddr(inspection_text, thermal_text, key_points)

        # Reliability checking
        if not report or len(report.strip()) < 50:
            print("Warning: Weak report output, using fallback")
            report = "Report generation incomplete. Please verify input data."

        # Step 7: Saving report
        print("Saving report...")
        save_report(report, all_images)

        end_time = time.time()

        print("\nPipeline completed successfully.")
        print(f"Execution time: {round(end_time - start_time, 2)} seconds")

    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()