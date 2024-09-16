# color_shift.py
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

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


    # Apply color preset
    def apply_color_preset(self, preset):
        valid_presets = ["warm", "cool", "vintage", "sepia"]
        while preset not in valid_presets:
            preset = input(f"Invalid preset. Choose one from {valid_presets}: ")
        if preset == 'sepia':
            sepia_filter = [(int(r * 0.393 + g * 0.769 + b * 0.189),
                            int(r * 0.349 + g * 0.686 + b * 0.168),
                            int(r * 0.272 + g * 0.534 + b * 0.131))
                            for (r, g, b) in self.img.getdata()]
            self.img.putdata(sepia_filter)
            print("Sepia preset applied.")
        elif preset == 'cool':
            cool_filter = [(int(r * 0.8), int(g * 0.9), int(b * 1.1)) for (r, g, b) in self.img.getdata()]
            self.img.putdata(cool_filter)
            print("Cool preset applied.")
        elif preset == 'warm':
            warm_filter = [(int(r * 1.1), int(g * 0.9), int(b * 0.8)) for (r, g, b) in self.img.getdata()]
            self.img.putdata(warm_filter)
            print("Warm preset applied.")
        elif preset == 'vintage':
            vintage_filter = [(int(r * 0.9 + g * 0.7 + b * 0.4),
                            int(r * 0.6 + g * 0.5 + b * 0.3),
                            int(r * 0.3 + g * 0.2 + b * 0.1))
                            for (r, g, b) in self.img.getdata()]
            self.img.putdata(vintage_filter)
            print("Vintage preset applied.")
        print(f"Applied {preset} preset.")

    # Adjust contrast and brightness
    def adjust_contrast_brightness(self, contrast_factor, brightness_factor):
        enhancer_contrast = ImageEnhance.Contrast(self.img)
        self.img = enhancer_contrast.enhance(contrast_factor)
        enhancer_brightness = ImageEnhance.Brightness(self.img)
        self.img = enhancer_brightness.enhance(brightness_factor)

    # Apply transparency
    def apply_transparency(self, transparency_level):
        while not (0 <= transparency_level <= 255):
            transparency_level = int(input("Enter a valid transparency level (0 to 255): "))
        self.img.putalpha(transparency_level)
        print("Transparency applied successfully.")


    # Save the modified image in a temporary file
    def save_image(self, output_path):
        if self.img:
            self.img.save(output_path)
            print(f"Temporary image saved at {output_path}")
        else:
            print("No image to save.")
