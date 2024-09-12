from PIL import Image as PILImage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from color_shift import ColorShift
import os

class ColorShiftApp(App):
    def build(self):
        # Main layout: Divide into two vertical sections
        self.main_layout = BoxLayout(orientation='horizontal', spacing=10)
        
        # Left section (1/3 screen): Logo and buttons
        self.left_layout = BoxLayout(orientation='vertical', size_hint=(1/3, 1))
        
        # Placeholder for Logo (use your image logo path)
        logo = Image(source='assets/logo.png', size_hint=(1, 0.3))  # Logo takes 30% of the left layout
        
        # Add logo to the left layout
        self.left_layout.add_widget(logo)

        #Button to apply black and white
        bw_btn = Button(text=f"Apply black and white", size_hint=(1,0.1), on_press=self.start_black_and_white_transformation)
        self.left_layout.add_widget(bw_btn)

        # Buttons for "Apply Color Shift" options
        for i in range(1, 4):
            btn = Button(text=f"Apply Color Shift {i}", size_hint=(1, 0.1))
            self.left_layout.add_widget(btn)

        # Right section (2/3 screen): Initially file chooser, then image display
        self.right_layout = BoxLayout(orientation='vertical', size_hint=(2/3, 1))
        
        # Create FileChooser to let user pick an image
        self.file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        self.file_chooser.bind(selection=self.initial_image_selection)  # Initially bind it for the first image
        self.right_layout.add_widget(self.file_chooser)
        
        # Add left and right layouts to main layout
        self.main_layout.add_widget(self.left_layout)
        self.main_layout.add_widget(self.right_layout)

        # Variable to store the current image path
        self.current_image = None
        self.stored_original_image = None
        self.stored_modified_image = None
        
        return self.main_layout

    # Handle the first time a user selects an image.
    def initial_image_selection(self, instance, value):
        # Ensure a file is selected and it's an image
        if value and os.path.isfile(value[0]):
            self.current_image = value[0]  # Store the currently selected image

            if self.current_image.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Display the selected image
                self.right_layout.clear_widgets()
                self.img_widget = Image(source=self.current_image)
                self.right_layout.add_widget(self.img_widget)

                # Remove file chooser and show the "Choose Another Photo" button
                self.right_layout.remove_widget(self.file_chooser)

                # Add "Choose Another Photo" button
                self.choose_another_btn = Button(text="Choose Another Photo", size_hint=(1, 0.1))
                self.choose_another_btn.bind(on_press=self.choose_another_photo)
                self.left_layout.add_widget(self.choose_another_btn)
            else:
                # Optional: Display error if the file is not an image
                print("Please select a valid image file!")

    def choose_another_photo(self, instance):
        # Store the current image before the user selects a new one
        if hasattr(self, 'current_image') and self.current_image:
            self.stored_original_image = self.current_image  # Save the currently displayed image

        # Remove "Choose Another Photo" button and show the file chooser
        self.left_layout.remove_widget(self.choose_another_btn)
        
        # Add "Cancel" button in the same place
        self.cancel_btn = Button(text="Cancel", size_hint=(1, 0.1))
        self.cancel_btn.bind(on_press=self.cancel_selection)
        self.left_layout.add_widget(self.cancel_btn)

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
                self.left_layout.remove_widget(self.cancel_btn)
                self.left_layout.add_widget(self.choose_another_btn)
            else:
                # Optional: Display error if the file is not an image
                print("Please select a valid image file!")

    def cancel_selection(self, instance):
        # Re-display the stored image (initial image) when the user clicks on "Cancel"
        if hasattr(self, 'stored_modified_image') and self.stored_modified_image:
            self.right_layout.clear_widgets()
            self.img_widget = Image(source=self.stored_modified_image)
            self.right_layout.add_widget(self.img_widget)
        elif hasattr(self, 'stored_original_image') and self.stored_original_image and not self.stored_modified_image:
            self.right_layout.clear_widgets()
            self.img_widget = Image(source=self.stored_original_image)
            self.right_layout.add_widget(self.img_widget)

        # Remove "Cancel" button and re-add "Choose Another Photo" button
        self.left_layout.remove_widget(self.cancel_btn)
        self.left_layout.add_widget(self.choose_another_btn)
    
    # Save the modified image over the original and remove the temporary file
    def save_image(self, instance):
        if self.stored_modified_image and self.current_image:
            # Save the black-and-white image with a new name (append "_bw" to the original file name)
            original_dir, original_filename = os.path.split(self.current_image)
            filename_wo_ext, ext = os.path.splitext(original_filename)
            bw_img_filename = f"{filename_wo_ext}_bw{ext}"  # E.g., "image_bw.png"
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
            os.remove(self.stored_modified_image)  # Delete the temporary black-and-white image
            self.stored_modified_image = None

            # Restore the original image
            self.right_layout.clear_widgets()
            self.img_widget = Image(source=self.stored_original_image)
            self.right_layout.add_widget(self.img_widget)

            # Remove Save and Cancel buttons
            self.right_layout.remove_widget(self.save_btn)
            self.right_layout.remove_widget(self.cancel_mod_btn)

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
                self.save_btn = Button(text="Save", size_hint=(1, 0.1))
                self.save_btn.bind(on_press=self.save_image)
                self.right_layout.add_widget(self.save_btn)

                self.cancel_mod_btn = Button(text="Cancel", size_hint=(1, 0.1))
                self.cancel_mod_btn.bind(on_press=self.cancel_image_modification)
                self.right_layout.add_widget(self.cancel_mod_btn)



# Run the app
if __name__ == '__main__':
    ColorShiftApp().run()
