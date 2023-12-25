from PIL import Image
import pytesseract

# Open an image file
img = Image.open('example.png')

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(img)

# Print the recognized text
print(text)

