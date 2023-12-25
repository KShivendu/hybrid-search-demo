from PIL import Image
import pytesseract

# Open an image file
img = Image.open('data/20231219_190133.jpg')

# Use pytesseract to do OCR on the image
custom_config = r'--oem 3 --psm 6'  # Page segmentation mode
text = pytesseract.image_to_string(img) # , config=custom_config)

# Print the recognized text
print(text)

