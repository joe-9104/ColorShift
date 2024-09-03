from PIL import Image
import re

class ColorChanger:
    def __init__(self):
        # Ask the user for input and perform validation
        self.image_path = self.get_image_path()
        self.target_color = self.get_target_color()
        self.color_to_change = self.get_color_to_change()
        
        # Load and convert the image
        self.img = self.load_image(self.image_path)

    def get_image_path(self):
        # Get and validate image path input
        while True:
            path = input("Enter the image path: ").strip().replace("\\", "/")
            path = path.strip('"').strip("'")  # Remove surrounding quotes if any
            if re.match(r"^[a-zA-Z]:/.*\.(jpg|jpeg|png|bmp)$", path):
                print("\n\n")
                return path
            else:
                print("Invalid image path. Please enter a valid path (e.g., C:/path/to/image.jpg).")

    def get_target_color(self):
        # Get and validate target color input
        while True:
            target_color = input("Enter the target color in RGB format (e.g., (102, 147, 163)): ").strip()
            if re.match(r"^\(\d{1,3},\s*\d{1,3},\s*\d{1,3}\)$", target_color):
                # Convert to tuple of integers
                target_color_tuple = tuple(map(int, target_color.strip("()").split(",")))
                
                # Check if all values are within the range 0-255
                if all(0 <= val <= 255 for val in target_color_tuple):
                    print("\n\n")
                    return target_color_tuple
                else:
                    print("RGB values must be between 0 and 255.")
            else:
                print("Invalid RGB format. Please enter a valid color (e.g., (102, 147, 163)).")

    def get_color_to_change(self):
        # Get and validate color to change input
        while True:
            color = input("Which color to change (r (red), g (green), or b (blue)): ").strip().lower()
            if color in ('r', 'g', 'b'):
                print("\n\n")
                return color
            else:
                print("Invalid input. Please enter 'r', 'g', or 'b'.")

    def load_image(self, image_path):
        try:
            # Attempt to open and convert the image
            img = Image.open(image_path).convert("RGB")
            print("Image loaded successfully.")
            return img
        except FileNotFoundError:
            print(f"Error: The file at '{image_path}' does not exist.")
            # Re-prompt the user for the correct path
            self.image_path = self.get_image_path()
            return self.load_image(self.image_path)
        except IOError:
            print("Error: The image could not be opened. Please check the file and try again.")
            # Re-prompt the user for the correct path
            self.image_path = self.get_image_path()
            return self.load_image(self.image_path)

    def change_color(self):
        try:
            data = self.img.getdata()
            new_image_data = []
            
            for item in data:
                r, g, b = item
                color_map = {'r': r, 'g': g, 'b': b}
                
                # Check if the pixel is primarily the selected color
                if color_map[self.color_to_change] >= color_map['r'] and color_map[self.color_to_change] >= color_map['g'] and color_map[self.color_to_change] >= color_map['b']:
                    # Calculate the scaling factor based on the intensity of the selected channel
                    factor = color_map[self.color_to_change] / 255.0

                    # Blend the current pixel color with the target color
                    new_r = int((1 - factor) * r + factor * self.target_color[0])
                    new_g = int((1 - factor) * g + factor * self.target_color[1])
                    new_b = int((1 - factor) * b + factor * self.target_color[2])

                    new_image_data.append((new_r, new_g, new_b))
                else:
                    new_image_data.append(item)
            
            # Update image data
            self.img.putdata(new_image_data)
            print("Image changed successfully")
            
        except Exception as e:
            print(f"An error occurred while processing the image: {e}")

    def save_image(self):
        try:
            output_path = self.image_path.replace(".jpg", "-Modified.jpg").replace(".jpeg", "-Modified.jpeg").replace(".png", "-Modified.png").replace(".bmp", "-Modified.bmp")
            self.img.save(output_path)
            print(f"Image saved successfully at {output_path}")
        except Exception as e:
            print(f"An error occurred while saving the image: {e}")

# Main program execution
if __name__ == "__main__":
    changer = ColorChanger()
    changer.change_color()
    changer.save_image()
