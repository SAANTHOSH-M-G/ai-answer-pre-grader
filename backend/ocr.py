import easyocr

# CPU mode for now.
# We can enable GPU later if CUDA is fixed.
reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):
    results = reader.readtext(image_path)

    text_parts = []
    confidences = []

    for detection in results:
        detected_text = detection[1]
        confidence = detection[2]

        text_parts.append(detected_text)
        confidences.append(confidence)

    extracted_text = "\n".join(text_parts)

    if confidences:
        average_confidence = sum(confidences) / len(confidences)
    else:
        average_confidence = 0.0

    return extracted_text, average_confidence
