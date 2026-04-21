from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os


def _images_for_section(section_name, images):
    section = section_name.lower()
    matched = []

    for img in images:
        name = os.path.basename(img).lower()
        if any(k in name for k in section.split()):
            matched.append(img)

    return matched


def save_report(report_text, images):
    path = "output/final_ddr.pdf"
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    elements = []
    current_section = ""

    for line in report_text.split("\n"):
        if not line.strip():
            continue

        # detect section headings
        if ":" in line and len(line.split()) < 6:
            current_section = line.strip()
            elements.append(Paragraph(f"<b>{line}</b>", styles["Heading2"]))
        else:
            elements.append(Paragraph(line, styles["Normal"]))

        elements.append(Spacer(1, 8))

        # attach relevant images immediately after section lines
        matched = _images_for_section(current_section, images)
        if matched:
            for img in matched[:2]:
                try:
                    elements.append(Image(img, width=400, height=250))
                    elements.append(Spacer(1, 10))
                except:
                    elements.append(Paragraph("Image Not Available", styles["Normal"]))

    doc.build(elements)
    print(f"PDF saved at {path}")