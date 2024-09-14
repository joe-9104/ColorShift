from PIL import Image as PILImage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.spinner import Spinner
from color_shift import ColorShift
import os

class ColorShiftApp(App):
    def build(self):
        # Main layout: Divide into two vertical sections
        self.main_layout = BoxLayout(orientation='horizontal', spacing=10)
        
        # Left section (1/3 screen): Divide into static and dynamic parts
        self.left_layout = BoxLayout(orientation='vertical', size_hint=(1/3, 1))
        
        # Static part: Contains the logo and effect selection dropdown
        self.static_left_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.4))
        # Dynamic part: Updates based on effect selection
        self.dynamic_left_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        
        # Add logo to static part
        logo = Image(source='assets/logo.png', size_hint=(1, 0.3))  # Logo takes 30% of the static layout
        self.static_left_layout.add_widget(logo)
        
        # Add dropdown for effect selection
        self.effect_spinner = Spinner(
            text="Select effect",
            values=("black and white", "sharpen or blur"),
            size_hint=(1, 0.1)
        )
        self.effect_spinner.bind(text=self.on_effect_selected)
        self.static_left_layout.add_widget(self.effect_spinner)
        
        # Add static and dynamic layouts to the main left layout
        self.left_layout.add_widget(self.static_left_layout)
        self.left_layout.add_widget(self.dynamic_left_layout)
        
        # Right section: Initially file chooser, then image display
        self.right_layout = BoxLayout(orientation='vertical', size_hint=(2/3, 1))
        self.file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        self.file_chooser.bind(selection=self.initial_image_selection)  # Initially bind for first image
        self.right_layout.add_widget(self.file_chooser)
        
        # Add left and right layouts to main layout
        self.main_layout.add_widget(self.left_layout)
        self.main_layout.add_widget(self.right_layout)
        
        # Variable to store the current image path
        self.current_image = None
        self.stored_original_image = None
        self.stored_modified_image = None
        
        return self.main_layout

    # Handle the first time a user selects an image
    def initial_image_selection(self, instance, value):
        if value and os.path.isfile(value[0]):
            self.current_image = value[0]  # Store the selected image
            self.stored_original_image = self.current_image

            if self.current_image.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Display the selected image
                self.right_layout.clear_widgets()
                self.img_widget = Image(source=self.current_image)
                self.right_layout.add_widget(self.img_widget)
                
                # Remove file chooser
                self.right_layout.remove_widget(self.file_chooser)

                # Add "Choose Another Photo" button in the static layout
                self.choose_another_btn = Button(text="Choose Another Photo", size_hint=(1, 0.1))
                self.choose_another_btn.bind(on_press=self.choose_another_photo)
                self.static_left_layout.add_widget(self.choose_another_btn)

                # Clear dynamic layout and add the effect-specific UI
                self.dynamic_left_layout.clear_widgets()
                self.on_effect_selected(self.effect_spinner, self.effect_spinner.text)
            else:
                print("Please select a valid image file!")

    # Handle effect selection and update the dynamic part
    def on_effect_selected(self, spinner, text):
        # Clear dynamic layout for new content
        self.dynamic_left_layout.clear_widgets()

        if text == "black and white":
            bw_btn = Button(text="Apply black and white", size_hint=(1, 0.1), on_press=self.start_black_and_white_transformation)
            self.dynamic_left_layout.add_widget(bw_btn)
        elif text == "sharpen or blur":
            # Add dropdown for sharpen/blur selection
            self.sharpen_blur_spinner = Spinner(
                text="Select effect",
                values=("sharpen", "blur"),
                size_hint=(1, 0.1)
            )
            self.dynamic_left_layout.add_widget(self.sharpen_blur_spinner)
            
            # Add button to apply sharpen or blur effect
            sharpen_blur_btn = Button(text="Apply sharpen or blur", size_hint=(1, 0.1), on_press=self.start_sharpen_blur_transformation)
            self.dynamic_left_layout.add_widget(sharpen_blur_btn)


    # Add save and cancel buttons after applying effect
    def add_save_cancel_buttons(self, modification_type="bw"):

        # Check if "Save" and "Cancel" buttons are already added to avoid duplication
        if hasattr(self, 'save_btn') and hasattr(self, 'cancel_mod_btn'):
            if self.save_btn in self.right_layout.children and self.cancel_mod_btn in self.right_layout.children:
                # Buttons are already displayed, so do nothing
                return
            
        self.save_btn = Button(text="Save", size_hint=(1, 0.1))
        self.save_btn.bind(on_press=lambda x: self.save_image(x, modification_type))
        self.right_layout.add_widget(self.save_btn)

        self.cancel_mod_btn = Button(text="Cancel", size_hint=(1, 0.1))
        self.cancel_mod_btn.bind(on_press=self.cancel_image_modification)
        self.right_layout.add_widget(self.cancel_mod_btn)


    def choose_another_photo(self, instance):
        # Store the current image before the user selects a new one
        if hasattr(self, 'current_image') and self.current_image:
            self.stored_original_image = self.current_image  # Save the currently displayed image

        # Remove "Choose Another Photo" button and show the file chooser
        self.static_left_layout.remove_widget(self.choose_another_btn)
        
        # Add "Cancel" button in the same place
        self.cancel_btn = Button(text="Cancel", size_hint=(1, 0.1))
        self.cancel_btn.bind(on_press=self.cancel_selection)
        self.static_left_layout.add_widget(self.cancel_btn)

        # Reopen the FileChooser to let the user choose a new image
        self.right_layout.clear_widgets()
        self.file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        self.file_chooser.bind(selection=self.show_image)
        self.right_layout.add_widget(self.file_chooser)

    def show_image(self, instance, value):
        # Check if any file is selected and if it's an image
        if value and os.path.isfile(value[0]):
            self.current_image = value[0]  # Update the current image with the newly selected one
            # Clear paths of stored images
            self.stored_modified_image = None
            self.stored_original_image = None

            # Ensure the selected file is an image
            if self.current_image.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Display the new selected image
                self.right_layout.clear_widgets()
                self.img_widget = Image(source=self.current_image)
                self.right_layout.add_widget(self.img_widget)
                
                # Once image is shown, remove the "Cancel" button and re-add the "Choose Another Photo" button
                self.static_left_layout.remove_widget(self.cancel_btn)
                self.static_left_layout.add_widget(self.choose_another_btn)
            else:
                # Optional: Display error if the file is not an image
                print("Please select a valid image file!")

    def cancel_selection(self, instance):
        # Re-display the stored image (initial image) when the user clicks on "Cancel"
        if hasattr(self, 'stored_modified_image') and self.stored_modified_image:
            self.img_widget = Image(source=self.stored_modified_image)
            self.right_layout.add_widget(self.img_widget)

            # Add Save and Cancel buttons
            self.add_save_cancel_buttons(self.modification_type)

        elif hasattr(self, 'stored_original_image') and self.stored_original_image and not self.stored_modified_image:
            self.right_layout.clear_widgets()
            self.img_widget = Image(source=self.stored_original_image)
            self.right_layout.add_widget(self.img_widget)

        # Remove "Cancel" button and re-add "Choose Another Photo" button
        self.static_left_layout.remove_widget(self.cancel_btn)
        self.static_left_layout.add_widget(self.choose_another_btn)
    
    # Save the modified image over the original and remove the temporary file
    def save_image(self, instance, modification_type="bw"):
        if self.stored_modified_image and self.current_image:
            # Save the black-and-white image with a new name (append "_bw" to the original file name)
            original_dir, original_filename = os.path.split(self.current_image)
            filename_wo_ext, ext = os.path.splitext(original_filename)
            bw_img_filename = f"{filename_wo_ext}_{modification_type}{ext}"  # E.g., "image_bw.png"
            bw_img_path = os.path.join(original_dir, bw_img_filename)
            img_to_save = PILImage.open(self.stored_modified_image)
            img_to_save.save(bw_img_path)
            os.remove(self.stored_modified_image)  # Remove the temporary file
            self.stored_modified_image = None

            # Remove Save and Cancel buttons
            self.right_layout.remove_widget(self.save_btn)
            self.right_layout.remove_widget(self.cancel_mod_btn)

    # Cancel the modification and revert to the original image
    def cancel_image_modification(self, instance):
        if self.stored_modified_image:

            # Restore the original image
            self.img_widget.source = self.stored_original_image
            self.img_widget.reload()

            # Remove Save and Cancel buttons
            self.right_layout.remove_widget(self.save_btn)
            self.right_layout.remove_widget(self.cancel_mod_btn)

            os.remove(self.stored_modified_image)  # Delete the temporary black-and-white image
            self.stored_modified_image = None

    # Main functions
    def start_black_and_white_transformation(self, instance):
        if self.current_image:
            ColorShiftInstance = ColorShift(self.current_image)
            bw_img = ColorShiftInstance.convert_to_black_and_white()
            if bw_img:
                # Path for temporary black and white image
                bw_img_path = os.path.join(os.getcwd(), "ColorShift_Kivy/images", "bw_image.png")
                ColorShiftInstance.save_image(bw_img_path)
                self.stored_modified_image = bw_img_path

                # Update the Kivy UI with the black-and-white image
                self.img_widget.source = bw_img_path
                self.img_widget.reload()  # Reload the image to reflect changes

                # Add Save and Cancel buttons
                self.modification_type = "bw"
                self.add_save_cancel_buttons()

    def start_sharpen_blur_transformation(self, instance):
        selected_effect = self.sharpen_blur_spinner.text  # Get the selected effect from the dropdown
        if self.current_image and selected_effect in ("sharpen", "blur"):
            self.stored_original_image = self.current_image
            ColorShiftInstance = ColorShift(self.current_image)
            ColorShiftInstance.apply_sharpen_blur(selected_effect)

            # Save the modified image temporarily and display it
            modified_img_path = os.path.join(os.getcwd(), "ColorShift_Kivy/images", f"{selected_effect}_image.png")
            ColorShiftInstance.save_image(modified_img_path)
            self.stored_modified_image = modified_img_path

            # Update the Kivy UI with the sharpened or blurred image
            self.img_widget.source = modified_img_path
            self.img_widget.reload()  # Reload the image to reflect changes

            # Add Save and Cancel buttons
            self.modification_type = selected_effect
            self.add_save_cancel_buttons(selected_effect)

        else:
            print("Please select an effect and an image.")


# Run the app
if __name__ == '__main__':
    ColorShiftApp().run()
