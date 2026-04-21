def clean_text(text):
    return text.replace("\n", " ").strip()

def extract_key_points(text):
    keywords = ["dampness", "leakage", "crack", "tile", "seepage"]
    points = []

    for line in text.split("."):
        for word in keywords:
            if word in line.lower():
                points.append(line.strip())

    return list(set(points))  # remove duplicates