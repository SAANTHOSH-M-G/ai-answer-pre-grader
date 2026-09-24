from ocr import extract_text

image_path = "sample_answer.jpg"

text, confidence = extract_text(image_path)

print("\n========== OCR RESULT ==========\n")

print("Extracted Text:")
print(text)

print("\nOCR Confidence:")
print(f"{confidence * 100:.1f}%")
