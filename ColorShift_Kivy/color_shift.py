# color_shift.py
from PIL import Image, ImageFilter, ImageDraw

class ColorShift:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = self.load_image().convert("RGB")

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
    
    # Apply sharpen or blur
    def apply_sharpen_blur(self, effect):
        if effect == "sharpen":
            self.img = self.img.filter(ImageFilter.SHARPEN)
        elif effect == "blur":
            self.img = self.img.filter(ImageFilter.BLUR)
        print(f"Applied {effect} effect.")

    # Apply gradient
    def apply_gradient(self, color1, color2):
        width, height = self.img.size
        gradient = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(gradient)
        for i in range(height):
            r = int(color1[0] + (color2[0] - color1[0]) * i / height)
            g = int(color1[1] + (color2[1] - color1[1]) * i / height)
            b = int(color1[2] + (color2[2] - color1[2]) * i / height)
            draw.line([(0, i), (width, i)], fill=(r, g, b))
        self.img = Image.blend(self.img, gradient, alpha=0.5)
        print("Gradient applied.")
        print("Applied gradient effect.")



    # Save the modified image in a temporary file
    def save_image(self, output_path):
        if self.img:
            self.img.save(output_path)
            print(f"Temporary image saved at {output_path}")
        else:
            print("No image to save.")
