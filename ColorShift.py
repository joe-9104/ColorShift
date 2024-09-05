from PIL import Image
import re

class ColorShift:
    # Class constructor
    def __init__(self):
        # Ask the user for input and perform validation
        self.image_path = self.get_image_path()        
        # Load and convert the image
        self.img = self.load_image(self.image_path)
        self.user_option = self.get_user_option()
        # Call the transform_image() function to know which function to use
        self.transform_image()

    # Get and validate image path input
    def get_image_path(self):
        while True:
            path = input("Enter the image path: ").strip().replace("\\", "/")
            path = path.strip('"').strip("'")  # Remove surrounding quotes if any
            if re.match(r"^[a-zA-Z]:/.*\.(jpg|jpeg|png|bmp)$", path):
                print("\n\n")
                return path
            else:
                print("Invalid image path. Please enter a valid path (e.g., C:/path/to/image.jpg).")

    # Ask for the user choice; convert to bw, change bg or a specific color within the image?
    def get_user_option(self):
        while True:
            option = input("Choose a number: \n1. Convert the image in black and white \n2. Change the background color of the image \n3. Change a specific color within the image\n")
            if(option == "1" or option == "2" or option == "3"):
                return int(option)
            else:
                print("You must chooose between 1, 2 and 3. Try again!")

    # Get and validate target color input
    def get_target_color(self):
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

    # Get and validate color to change input
    def get_color_to_change(self): 
        while True:
            color = input("Which color to change (r (red), g (green), or b (blue)): ").strip().lower()
            if color in ('r', 'g', 'b'):
                print("\n\n")
                return color
            else:
                print("Invalid input. Please enter 'r', 'g', or 'b'.")

    # Open and convert the image
    def load_image(self, image_path):
        try:
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

    # Convert the image to black and white
    def convert_to_black_and_white(self):
        self.img = self.img.convert("L").convert("RGB")  # Convert to grayscale and back to RGB
    
    # Change the background color of the image
    def change_black_background(self, new_bg_color):
        data = self.img.getdata()
        new_image_data = []
        
        for item in data:
            # Detect black or near-black pixels
            if all(val < 30 for val in item):  # Threshold for black pixels
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
                
                # Check if the pixel is primarily the selected color
                if color_map[color_to_change] >= color_map['r'] and color_map[color_to_change] >= color_map['g'] and color_map[color_to_change] >= color_map['b']:
                    # Calculate the scaling factor based on the intensity of the selected channel
                    factor = color_map[color_to_change] / 255.0

                    # Blend the current pixel color with the target color
                    new_r = int((1 - factor) * r + factor * target_color[0])
                    new_g = int((1 - factor) * g + factor * target_color[1])
                    new_b = int((1 - factor) * b + factor * target_color[2])

                    new_image_data.append((new_r, new_g, new_b))
                else:
                    new_image_data.append(item)
            
            # Update image data
            self.img.putdata(new_image_data)
            print("Image changed successfully")
            
        except Exception as e:
            print(f"An error occurred while processing the image: {e}")

    # Function to handle the use of functions based on the user input
    def transform_image(self):
        if self.user_option == 1:
            return self.convert_to_black_and_white()
        elif self.user_option == 2:
            new_bg_color = self.get_target_color()
            return self.change_black_background(new_bg_color)
        else:
            target_color = self.get_target_color()
            color_to_change = self.get_color_to_change()
            return self.change_color(target_color, color_to_change)

    # Save the output image (same path, added the word 'modified' to the same image name)
    def save_image(self):
        try:
            output_path = self.image_path.replace(".jpg", "-Modified.jpg").replace(".jpeg", "-Modified.jpeg").replace(".png", "-Modified.png").replace(".bmp", "-Modified.bmp")
            self.img.save(output_path)
            print(f"Image saved successfully at {output_path}")
        except Exception as e:
            print(f"An error occurred while saving the image: {e}")

# Main program execution
if __name__ == "__main__":
    ColorShiftItem = ColorShift()
    ColorShiftItem.save_image()
