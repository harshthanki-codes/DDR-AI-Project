import os
import shutil
import time
import logging

from src.extract_text import extract_text
from src.extract_images import extract_images
from src.preprocess import clean_text, extract_key_points
from src.ai import generate_ddr
from src.report_generator import save_report


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def clean_output():
    logging.info("Cleaning previous outputs...")

    output_dir = "output"
    images_dir = os.path.join(output_dir, "images")

    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)

    os.makedirs(images_dir, exist_ok=True)


def validate_inputs():
    if not os.path.exists("data/report.pdf"):
        raise FileNotFoundError("Missing file: data/report.pdf")

    if not os.path.exists("data/thermal.pdf"):
        raise FileNotFoundError("Missing file: data/thermal.pdf")


def run_pipeline():
    start_time = time.time()

    logging.info("Starting DDR pipeline...")

    try:
        validate_inputs()

        clean_output()

        inspection_path = "data/report.pdf"
        thermal_path = "data/thermal.pdf"

        logging.info("Extracting text...")
        inspection_text = extract_text(inspection_path)
        thermal_text = extract_text(thermal_path)

        if not inspection_text.strip():
            raise ValueError("Inspection data missing")

        logging.info("Cleaning data...")
        inspection_text = clean_text(inspection_text)
        thermal_text = clean_text(thermal_text)

        logging.info("Extracting key observations...")
        key_points = extract_key_points(inspection_text)

        logging.info("Extracting images...")
        inspection_images = extract_images(inspection_path)
        thermal_images = extract_images(thermal_path)

        all_images = inspection_images + thermal_images

        logging.info("Generating report...")
        report = generate_ddr(inspection_text, thermal_text, key_points)

        if not report or len(report) < 50:
            raise ValueError("Weak AI output")

        logging.info("Saving report...")
        save_report(report, all_images)

        logging.info("Pipeline completed successfully")
        logging.info(f"Execution time: {round(time.time() - start_time, 2)} sec")

    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")