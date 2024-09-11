from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
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
        
        return self.main_layout

    def initial_image_selection(self, instance, value):
        """This function handles the first time a user selects an image."""
        # Ensure a file is selected and it's an image
        if value and os.path.isfile(value[0]):
            self.current_image = value[0]  # Store the currently selected image

            if self.current_image.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Display the selected image
                self.right_layout.clear_widgets()
                img_widget = Image(source=self.current_image)
                self.right_layout.add_widget(img_widget)

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
            self.stored_image = self.current_image  # Save the currently displayed image

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

            # Ensure the selected file is an image
            if self.current_image.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Display the new selected image
                self.right_layout.clear_widgets()
                img_widget = Image(source=self.current_image)
                self.right_layout.add_widget(img_widget)
                
                # Once image is shown, remove the "Cancel" button and re-add the "Choose Another Photo" button
                self.left_layout.remove_widget(self.cancel_btn)
                self.left_layout.add_widget(self.choose_another_btn)
            else:
                # Optional: Display error if the file is not an image
                print("Please select a valid image file!")

    def cancel_selection(self, instance):
        # Re-display the stored image (initial image) when the user clicks on "Cancel"
        if hasattr(self, 'stored_image') and self.stored_image:
            self.right_layout.clear_widgets()
            img_widget = Image(source=self.stored_image)
            self.right_layout.add_widget(img_widget)

        # Remove "Cancel" button and re-add "Choose Another Photo" button
        self.left_layout.remove_widget(self.cancel_btn)
        self.left_layout.add_widget(self.choose_another_btn)

# Run the app
if __name__ == '__main__':
    ColorShiftApp().run()
