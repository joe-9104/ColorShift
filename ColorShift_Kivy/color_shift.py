# color_shift.py
from PIL import Image

class ColorShift:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = self.load_image()

    # Load the image
    def load_image(self):
        try:
            img = Image.open(self.image_path)
            return img
        except FileNotFoundError:
            print(f"Image not found at {self.image_path}")
            return None

    # Convert the image to black and white
    def convert_to_black_and_white(self):
        if self.img:
            self.img = self.img.convert("L").convert("RGB")  # Convert to grayscale and back to RGB
            return self.img
        else:
            print("No image loaded.")
            return None

    # Save the modified image in a temporary file
    def save_image(self, output_path):
        if self.img:
            self.img.save(output_path)
            print(f"Image saved at {output_path}")
        else:
            print("No image to save.")
