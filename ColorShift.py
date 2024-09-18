from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import re
import os

class ColorShift:
    # Class constructor
    def __init__(self):
        self.user_option = self.get_user_option()
        if(self.user_option != 5):
            self.image_path = self.get_image_path()        
            self.img = self.load_image(self.image_path)
        self.transform_image()

    # Get and validate image path input
    def get_image_path(self):
        while True:
            path = input("Enter the image path: ").strip().replace("\\", "/")
            path = path.strip('"').strip("'")  
            if re.match(r"^[a-zA-Z]:/.*\.(jpg|jpeg|png|bmp)$", path):
                return path
            else:
                print("Invalid image path. Please enter a valid path (e.g., C:/path/to/image.jpg).")

    # Get and validate user choice input
    def get_user_option(self):
        message = """Choose a number:
        1. Convert the image to black and white
        2. Change the background color of the image
        3. Change a specific color within the image
        4. Apply a color mask
        5. Batch process images (black and white)
        6. Adjust contrast and brightness
        7. Apply color preset
        8. Apply gradient effect
        9. Apply sharpen or blur effect
        10. Apply transparency
        """

        print(message)
        while True:
            option = input("Choice: ")
            if option in [str(i) for i in range(1, 11)]:
                return int(option)
            else:
                print("You must choose a valid option between 1 and 10.")

    # Get and validate target color input
    def get_target_color(self, input_message="Enter the target color in RGB format (e.g., (102, 147, 163)): "):
        while True:
            target_color = input(input_message).strip()
            if re.match(r"^\(\d{1,3},\s*\d{1,3},\s*\d{1,3}\)$", target_color):
                target_color_tuple = tuple(map(int, target_color.strip("()").split(",")))
                if all(0 <= val <= 255 for val in target_color_tuple):
                    print("\n\n")
                    return target_color_tuple
                else:
                    print("RGB values must be between 0 and 255.")
            else:
                print("Invalid RGB format. Please enter a valid color (e.g., (102, 147, 163)).")

    # Get and validate color to change input
    def get_color_to_change(self): 
        while True:
            color = input("Which color to change (r (red), g (green), or b (blue)): ").strip().lower()
            if color in ('r', 'g', 'b'):
                print("\n\n")
                return color
            else:
                print("Invalid input. Please enter 'r', 'g', or 'b'.")

    # Load and convert the image
    def load_image(self, image_path):
        try:
            img = Image.open(image_path).convert("RGB")
            print("Image loaded successfully.")
            return img
        except (FileNotFoundError, IOError):
            print(f"Error: Could not load the file at '{image_path}'. Skipping this image.")
            return None

    # Convert the image to black and white
    def convert_to_black_and_white(self):
        self.img = self.img.convert("L").convert("RGB")  # Convert to grayscale and back to RGB

    # Change the background color of the image
    def change_black_background(self, new_bg_color):
        data = self.img.getdata()
        new_image_data = []
        for item in data:
            if all(val < 30 for val in item):
                new_image_data.append(new_bg_color)
            else:
                new_image_data.append(item)
        self.img.putdata(new_image_data)
        print("Background color changed successfully.")
        return self.img

    # Change a specific color within the image
    def change_color(self, target_color, color_to_change):
        try:
            data = self.img.getdata()
            new_image_data = []
            for item in data:
                r, g, b = item
                color_map = {'r': r, 'g': g, 'b': b}
                if color_map[color_to_change] >= color_map['r'] and color_map[color_to_change] >= color_map['g'] and color_map[color_to_change] >= color_map['b']:
                    factor = color_map[color_to_change] / 255.0
                    new_r = int((1 - factor) * r + factor * target_color[0])
                    new_g = int((1 - factor) * g + factor * target_color[1])
                    new_b = int((1 - factor) * b + factor * target_color[2])
                    new_image_data.append((new_r, new_g, new_b))
                else:
                    new_image_data.append(item)
            self.img.putdata(new_image_data)
            print("Color changed successfully.")
        except Exception as e:
            print(f"Error occurred while processing the image: {e}")

    # Apply color mask
    def apply_color_mask(self):
        mask_color = self.get_target_color("Enter the color for the mask in RGB format: ")
        data = self.img.getdata()
        new_image_data = [(mask_color if (r < 100 and g < 100 and b < 100) else (r, g, b)) for (r, g, b) in data]
        self.img.putdata(new_image_data)
        print("Color mask applied successfully.")

    # Batch process images for black and white transformation
    def batch_process_images(self):
        while True:
            folder_path = input("Enter the folder path containing images for batch processing: ").strip().replace("\\", "/")
            folder_path = folder_path.strip('"').strip("'")
            # Check if the folder path exists and is a directory
            if not os.path.exists(folder_path):
                print("Error: The folder path does not exist. Please enter a valid path.")
                continue
            if not os.path.isdir(folder_path):
                print("Error: The provided path is not a directory. Please enter a valid folder path.")
                continue
            try:
                image_files = [f"{folder_path}/{f}" for f in os.listdir(folder_path) if re.match(r".*\.(jpg|jpeg|png|bmp)$", f)]
                for image_path in image_files:
                    try:
                        img = Image.open(image_path).convert("RGB")
                        img = img.convert("L").convert("RGB")
                        img.save(image_path.replace(".", "-Processed."))
                        print(f"Processed {image_path}.")
                    except Exception as e:
                        print(f"Skipping {image_path} due to error: {e}")
                break
            except FileNotFoundError:
                print("Invalid folder path. Please try again.")

    # Adjust contrast and brightness
    def adjust_contrast_brightness(self, contrast_factor, brightness_factor):
        enhancer_contrast = ImageEnhance.Contrast(self.img)
        self.img = enhancer_contrast.enhance(contrast_factor)
        enhancer_brightness = ImageEnhance.Brightness(self.img)
        self.img = enhancer_brightness.enhance(brightness_factor)

    # Apply color preset
    def apply_color_preset(self, preset):
        valid_presets = ["warm", "cool", "vintage", "sepia"]
        while preset not in valid_presets:
            preset = input(f"Invalid preset. Choose one from {valid_presets}: ")
        
        # Apply Sepia preset
        if preset == 'sepia':
            sepia_filter = [(int(r * 0.393 + g * 0.769 + b * 0.189),
                            int(r * 0.349 + g * 0.686 + b * 0.168),
                            int(r * 0.272 + g * 0.534 + b * 0.131))
                            for (r, g, b) in self.img.getdata()]
            self.img.putdata(sepia_filter)
            print("Sepia preset applied.")
        
        # Apply Cool preset
        elif preset == 'cool':
            cool_filter = [(int(r * 0.8), int(g * 0.9), int(b * 1.1)) for (r, g, b) in self.img.getdata()]
            self.img.putdata(cool_filter)
            print("Cool preset applied.")
        
        # Apply Warm preset
        elif preset == 'warm':
            warm_filter = [(int(r * 1.1), int(g * 0.9), int(b * 0.8)) for (r, g, b) in self.img.getdata()]
            self.img.putdata(warm_filter)
            print("Warm preset applied.")
        
        # Apply Vintage preset
        elif preset == 'vintage':
            vintage_filter = [(int(r * 0.9 + g * 0.7 + b * 0.4),
                            int(r * 0.6 + g * 0.5 + b * 0.3),
                            int(r * 0.3 + g * 0.2 + b * 0.1))
                            for (r, g, b) in self.img.getdata()]
            self.img.putdata(vintage_filter)
            print("Vintage preset applied.")
        
        print(f"Applied {preset} preset.")

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

    # Apply sharpen or blur
    def apply_sharpen_blur(self, effect):
        if effect == "sharpen":
            self.img = self.img.filter(ImageFilter.SHARPEN)
        elif effect == "blur":
            self.img = self.img.filter(ImageFilter.BLUR)
        print(f"Applied {effect} effect.")

    # Apply transparency
    def apply_transparency(self, transparency_level):
        while not (0 <= transparency_level <= 255):
            transparency_level = int(input("Enter a valid transparency level (0 to 255): "))
        self.img.putalpha(transparency_level)
        print("Transparency applied successfully.")

    # Function to handle user choices
    def transform_image(self):
        if self.user_option == 1:
            return self.convert_to_black_and_white()
        elif self.user_option == 2:
            new_bg_color = self.get_target_color("Enter new background color in RGB format: ")
            return self.change_black_background(new_bg_color)
        elif self.user_option == 3:
            target_color = self.get_target_color("Enter the color to change: ")
            color_to_change = self.get_color_to_change()
            return self.change_color(target_color, color_to_change)
        elif self.user_option == 4:
            return self.apply_color_mask()
        elif self.user_option == 5:
            return self.batch_process_images()
        elif self.user_option == 6:
            while True:
                contrast_factor = float(input("Enter contrast factor (0.0 - 2.0): "))
                if (0 <= contrast_factor <= 2):
                    break
                else:
                    print("contrast factor value must be between 0 and 2")
            while True:
                brightness_factor = float(input("Enter brightness factor (0.0 - 2.0): "))
                if (0 <= brightness_factor <= 2):
                    return self.adjust_contrast_brightness(contrast_factor, brightness_factor)
                else:
                    print("brightness factor value must be between 0 and 2")
        elif self.user_option == 7:
            preset = input("Choose a color preset (warm, cool, vintage, sepia): ")
            return self.apply_color_preset(preset)
        elif self.user_option == 8:
            color1 = self.get_target_color("Provide a color in RGB format: ")
            color2 = self.get_target_color("Provide a color in RGB format: ")
            return self.apply_gradient(color1, color2)
        elif self.user_option == 9:
            while True:
                effect = input("Choose effect (sharpen/blur): ").lower().strip()
                if effect in ["sharpen", "blur"]:
                    return self.apply_sharpen_blur(effect)
                else:
                    print("Choose a valid option: ['sharpen', 'blur']")
        elif self.user_option == 10:
            while True:
                transparency_level = input("Enter transparency level (0 to 255): ")
                if transparency_level in [str(i) for i in range(1, 256)]:
                    return self.apply_transparency(int(transparency_level))
                else:
                    print("You must choose a valid option between 0 and 255.")
            
        
     # Save the output image (same path, added the word 'modified' to the same image name)
    def save_image(self):
        try:
            output_path = self.image_path.replace(".jpg", "-Modified.jpg").replace(".jpeg", "-Modified.jpeg").replace(".png", "-Modified.png").replace(".bmp", "-Modified.bmp")
            self.img.save(output_path)
            print(f"Image saved successfully at {output_path}")
        except Exception as e:
            print(f"An error occurred while saving the image: {e}")

# Main function to run the program
def main():
    while True:
        color_shift_instance = ColorShift()
        if color_shift_instance.user_option != 5:
            color_shift_instance.save_image()
        repeat = input("Do you want to process another image? (yes/no): ").lower().strip()
        if repeat != "yes":
            break

if __name__ == "__main__":
    main()
