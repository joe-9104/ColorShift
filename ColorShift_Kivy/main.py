from PIL import Image as PILImage
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
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
        self.dynamic_left_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6), spacing = "10")
        
        # Add logo to static part
        logo = Image(source='assets/logo.png', size_hint=(1, 0.3))  # Logo takes 30% of the static layout
        self.static_left_layout.add_widget(logo)
        
        # Add dropdown for effect selection
        self.effect_spinner = Spinner(
            text="Select effect",
            values=("Black and White", 
                    "Change Color", 
                    "Sharpen or Blur", 
                    "Apply Color Preset", 
                    "Apply Gradient", 
                    "Adjust Contrast or Brightness", 
                    "Apply Transparency",
                    "Apply Color Mask"),
            size_hint=(1, 0.1)
        )
        self.effect_spinner.bind(text=self.on_effect_selected)
        self.static_left_layout.add_widget(self.effect_spinner)

        # Add info message
        self.instruction_label = Label(text="Choose an image to proceed with modification", size_hint=(1, 0.3))
        self.dynamic_left_layout.add_widget(self.instruction_label)
        
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

        if text == "Black and White":
            bw_btn = Button(text="Apply Black and White", size_hint=(1, 0.1), on_press=self.start_black_and_white_transformation)
            self.dynamic_left_layout.add_widget(BoxLayout(size_hint = (1, 0.6)))
            self.dynamic_left_layout.add_widget(bw_btn)
        elif text == "Change Color":
            self.target_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.4))

            self.target_layout.add_widget(Label(text = "Select the target color:"))

            self.target_r_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.target_g_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.target_b_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))

            self.target_r_label = Label(text=f"R: {int(self.target_r_slider.value)}")
            self.target_g_label = Label(text=f"G: {int(self.target_g_slider.value)}")
            self.target_b_label = Label(text=f"B: {int(self.target_b_slider.value)}")

            self.target_r_slider.bind(value=lambda instance, value: self.update_slider_label(self.target_r_label, "R", value))
            self.target_g_slider.bind(value=lambda instance, value: self.update_slider_label(self.target_g_label, "G", value))
            self.target_b_slider.bind(value=lambda instance, value: self.update_slider_label(self.target_b_label, "B", value))

            self.target_layout.add_widget(self.target_r_label)
            self.target_layout.add_widget(self.target_r_slider)

            self.target_layout.add_widget(self.target_g_label)
            self.target_layout.add_widget(self.target_g_slider)

            self.target_layout.add_widget(self.target_b_label)
            self.target_layout.add_widget(self.target_b_slider)

            self.dynamic_left_layout.add_widget(self.target_layout)

            self.color_to_change_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.3))

            self.color_to_change_layout.add_widget(Label(text="Select the color to change:"))

            self.toggle_group = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))

            self.toggle_r = ToggleButton(text="R", group="color", state="normal")
            self.toggle_g = ToggleButton(text="G", group="color", state="normal")
            self.toggle_b = ToggleButton(text="B", group="color", state="normal")

            self.toggle_group.add_widget(self.toggle_r)
            self.toggle_group.add_widget(self.toggle_g)
            self.toggle_group.add_widget(self.toggle_b)

            self.color_to_change_layout.add_widget(self.toggle_group)
            self.dynamic_left_layout.add_widget(self.color_to_change_layout)

            apply_color_change_btn = Button(
                text="Apply Color Change",
                size_hint=(1, 0.1),
                on_press=self.start_color_change_transformation
            )

            self.dynamic_left_layout.add_widget(apply_color_change_btn)
        elif text == "Sharpen or Blur":

            # Add dropdown for sharpen/blur selection
            self.sharpen_blur_layout = BoxLayout(size_hint = (1, 0.1))
            self.sharpen_blur_spinner = Spinner(
                text="Select effect",
                values=("sharpen", "blur"),
                size_hint=(1, 0.1)
            )
            self.sharpen_blur_layout.add_widget(self.sharpen_blur_spinner)
            self.dynamic_left_layout.add_widget(self.sharpen_blur_layout)
            self.dynamic_left_layout.add_widget(BoxLayout())

            # Add button to apply sharpen or blur effect
            sharpen_blur_btn = Button(text="Apply Sharpen or Blur", size_hint=(1, 0.2), on_press=self.start_sharpen_blur_transformation)
            self.dynamic_left_layout.add_widget(sharpen_blur_btn)

        elif text == "Apply Color Preset":

            self.preset_layout = BoxLayout(size_hint = (1, 0.1))
            self.preset_spinner = Spinner(
                text="Select preset",
                values=("warm", "cool", "vintage", "sepia"),
                size_hint=(1, 0.1)
            )
            self.preset_layout.add_widget(self.preset_spinner)
            self.dynamic_left_layout.add_widget(self.preset_layout)
            self.dynamic_left_layout.add_widget(BoxLayout())

            preset_btn = Button(text="Apply Preset", size_hint=(1, 0.2), on_press=self.start_preset_transformation)
            self.dynamic_left_layout.add_widget(preset_btn)

        elif text == "Apply Gradient":

            self.colors_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.6))
            self.color1_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.5))
            # Add gradient sliders for two colors
            self.color1_layout.add_widget(Label(text="Color 1 (RGB):"))

            # Sliders for color 1
            self.r1_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.g1_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.b1_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))

            # Labels to show current values
            self.r1_label = Label(text=f"R: {int(self.r1_slider.value)}")
            self.g1_label = Label(text=f"G: {int(self.g1_slider.value)}")
            self.b1_label = Label(text=f"B: {int(self.b1_slider.value)}")

            # Bind slider values to update labels dynamically
            self.r1_slider.bind(value=lambda instance, value: self.update_slider_label(self.r1_label, "R", value))
            self.g1_slider.bind(value=lambda instance, value: self.update_slider_label(self.g1_label, "G", value))
            self.b1_slider.bind(value=lambda instance, value: self.update_slider_label(self.b1_label, "B", value))

            # Add sliders and labels to the layout
            self.color1_layout.add_widget(self.r1_label)
            self.color1_layout.add_widget(self.r1_slider)
            self.color1_layout.add_widget(self.g1_label)
            self.color1_layout.add_widget(self.g1_slider)
            self.color1_layout.add_widget(self.b1_label)
            self.color1_layout.add_widget(self.b1_slider)

            self.colors_layout.add_widget(self.color1_layout)
            self.color2_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.5))

            self.color2_layout.add_widget(Label(text="Color 2 (RGB):"))

            # Sliders for color 2
            self.r2_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.g2_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.b2_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))

            # Labels to show current values
            self.r2_label = Label(text=f"R: {int(self.r2_slider.value)}")
            self.g2_label = Label(text=f"G: {int(self.g2_slider.value)}")
            self.b2_label = Label(text=f"B: {int(self.b2_slider.value)}")

            # Bind slider values to update labels dynamically
            self.r2_slider.bind(value=lambda instance, value: self.update_slider_label(self.r2_label, "R", value))
            self.g2_slider.bind(value=lambda instance, value: self.update_slider_label(self.g2_label, "G", value))
            self.b2_slider.bind(value=lambda instance, value: self.update_slider_label(self.b2_label, "B", value))

            # Add sliders and labels to the layout
            self.color2_layout.add_widget(self.r2_label)
            self.color2_layout.add_widget(self.r2_slider)
            self.color2_layout.add_widget(self.g2_label)
            self.color2_layout.add_widget(self.g2_slider)
            self.color2_layout.add_widget(self.b2_label)
            self.color2_layout.add_widget(self.b2_slider)

            self.colors_layout.add_widget(self.color2_layout)
            self.dynamic_left_layout.add_widget(self.colors_layout)

            # Add button to apply the gradient effect
            apply_gradient_btn = Button(text="Apply Gradient", size_hint=(1, 0.1), on_press=self.start_gradient_transformation)
            self.dynamic_left_layout.add_widget(apply_gradient_btn)

        elif text == "Adjust Contrast or Brightness":

            self.slider_layout = BoxLayout(orientation = "vertical", size_hint = (1, 2/3))
            self.slider_layout.add_widget(Label(text="Contrast factor:"))

            self.contrast_slider = Slider(min=0, max=2.0, value=1.0, step=0.1, size_hint=(1, 0.1))
            self.contrast_label = Label(text=f"Contrast: {int(self.contrast_slider.value)}")

            self.contrast_slider.bind(value=lambda instance, value: self.update_slider_label(self.contrast_label, "Contrast", value, "float"))

            self.slider_layout.add_widget(self.contrast_slider)
            self.slider_layout.add_widget(self.contrast_label)

            self.slider_layout.add_widget(Label(text="Brightness factor:"))

            self.brightness_slider = Slider(min=0, max=2.0, value=1.0, step=0.1, size_hint=(1, 0.1))
            self.brightness_label = Label(text=f"Brightness: {int(self.contrast_slider.value)}")

            self.brightness_slider.bind(value=lambda instance, value: self.update_slider_label(self.brightness_label, "Brightness", value, "float"))

            self.slider_layout.add_widget(self.brightness_slider)
            self.slider_layout.add_widget(self.brightness_label)

            self.dynamic_left_layout.add_widget(self.slider_layout)

            apply_contrast_brightness_btn = Button(text="Apply Contrast or Brightness", size_hint=(1, 0.1), on_press = self.start_contrast_brightness_transformation)
            self.dynamic_left_layout.add_widget(apply_contrast_brightness_btn)

        elif text == "Apply Transparency":
            self.transparency_layout = BoxLayout(orientation = "vertical", size_hint = (1, 0.5))

            self.transparency_layout.add_widget(Label(text="Transparency level:"))

            self.transparency_slider = Slider(min=0, max=255, value=255, step=1, size_hint=(1, 0.1))
            self.transparency_label = Label(text=f"Transparency: {int(self.transparency_slider.value)}")
            self.transparency_slider.bind(value=lambda instance, value: self.update_slider_label(self.transparency_label, "Transparency", value))

            self.transparency_layout.add_widget(self.transparency_slider)
            self.transparency_layout.add_widget(self.transparency_label)

            self.dynamic_left_layout.add_widget(self.transparency_layout)

            apply_transparency_btn = Button(text = "Apply Transparency", size_hint=(1, 0.1), on_press = self.start_transparency_transformation)
            self.dynamic_left_layout.add_widget(apply_transparency_btn)

        elif text == "Apply Color Mask":
            self.color_layout = BoxLayout(orientation = "vertical", size_hint=(1, 0.5))
            self.color_layout.add_widget(Label(text="Mask color:"))

            self.r_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.g_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))
            self.b_slider = Slider(min=0, max=255, value=128, step=1, size_hint=(1, 0.1))

            self.r_label = Label(text=f"R: {int(self.r_slider.value)}")
            self.g_label = Label(text=f"G: {int(self.g_slider.value)}")
            self.b_label = Label(text=f"B: {int(self.b_slider.value)}")

            self.r_slider.bind(value=lambda instance, value: self.update_slider_label(self.r_label, "R", value))
            self.g_slider.bind(value=lambda instance, value: self.update_slider_label(self.g_label, "G", value))
            self.b_slider.bind(value=lambda instance, value: self.update_slider_label(self.b_label, "B", value))

            self.color_layout.add_widget(self.r_label)
            self.color_layout.add_widget(self.r_slider)
            self.color_layout.add_widget(self.g_label)
            self.color_layout.add_widget(self.g_slider)
            self.color_layout.add_widget(self.b_label)
            self.color_layout.add_widget(self.b_slider)

            self.dynamic_left_layout.add_widget(self.color_layout)
            self.dynamic_left_layout.add_widget(BoxLayout(size_hint = (1, 0.1)))

            apply_mask_btn = Button(text = "Apply Color Mask", size_hint=(1, 0.1), on_press = self.start_color_mask_transformation)
            self.dynamic_left_layout.add_widget(apply_mask_btn)

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
            # Save the modified image with a new name (append the modification type to the original file name)
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

    def process_and_update_image(self, effect_name, ColorShiftInstance):
        # Save the modified image temporarily and display it
        modified_img_path = os.path.join(os.getcwd(), "ColorShift_Kivy/images", f"{effect_name}_image.png")
        ColorShiftInstance.save_image(modified_img_path)
        self.stored_modified_image = modified_img_path

        # Update the Kivy UI with the modified image
        self.img_widget.source = modified_img_path
        self.img_widget.reload()  # Reload the image to reflect changes

        # Add Save and Cancel buttons
        self.modification_type = effect_name
        self.add_save_cancel_buttons(effect_name)


    # Update the label for RGB slider
    def update_slider_label(self, label, attribute, value, valueType = 'int'):
        if valueType == 'int':
            label.text = f"{attribute}: {int(value)}"
        elif valueType == 'float':
            label.text = f"{attribute}: {float(value)}"


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
            self.process_and_update_image(selected_effect, ColorShiftInstance)
        else:
            print("Please select an effect and an image.")

    def start_preset_transformation(self, instance):
        selected_preset = self.preset_spinner.text
        if self.current_image and selected_preset in ("warm", "cool", "vintage", "sepia"):
            self.stored_original_image = self.current_image
            ColorShiftInstance = ColorShift(self.current_image)
            ColorShiftInstance.apply_color_preset(selected_preset)
            self.process_and_update_image(selected_preset, ColorShiftInstance)
        else:
            print("Please select a preset.")

    # Function to get RGB values from sliders and apply gradient
    def start_gradient_transformation(self, instance):
        color1 = (int(self.r1_slider.value), int(self.g1_slider.value), int(self.b1_slider.value))
        color2 = (int(self.r2_slider.value), int(self.g2_slider.value), int(self.b2_slider.value))
        if color1 and color2 and self.current_image:
            self.stored_original_image = self.current_image
            ColorShiftInstance = ColorShift(self.current_image)
            ColorShiftInstance.apply_gradient(color1, color2)
            self.process_and_update_image("gradient", ColorShiftInstance)

    def start_contrast_brightness_transformation(self, instance):
        contrast = float(self.contrast_slider.value)
        brightness = float(self.brightness_slider.value)
        if contrast and brightness and self.current_image:
            self.stored_original_image = self.current_image
            ColorShiftInstance = ColorShift(self.current_image)
            ColorShiftInstance.adjust_contrast_brightness(contrast, brightness)
            self.process_and_update_image("contrast_brightness", ColorShiftInstance)
        else:
            print("Please select a valid image or a valid contrast / brightness factor.")
    
    def start_transparency_transformation(self, instance):
        transparency_factor = int(self.transparency_slider.value)
        if transparency_factor and self.current_image:
            self.stored_original_image = self.current_image
            ColorShiftInstance = ColorShift(self.current_image)
            ColorShiftInstance.apply_transparency(transparency_factor)
            self.process_and_update_image("transparent", ColorShiftInstance)
    
    def start_color_mask_transformation(self, instance):
        color = (int(self.r_slider.value), int(self.g_slider.value), int(self.b_slider.value))
        if color and self.current_image:
            self.stored_original_image = self.current_image
            ColorShiftInstance = ColorShift(self.current_image)
            ColorShiftInstance.apply_color_mask(color)
            self.process_and_update_image("color_mask", ColorShiftInstance)

    def start_color_change_transformation(self, instance):
        target_color = (int(self.target_r_slider.value), int(self.target_g_slider.value), int(self.target_b_slider.value))
        if self.toggle_r.state == "down":
            color_to_change = "r"
        elif self.toggle_g.state == "down":
            color_to_change = "g"
        elif self.toggle_b.state == "down":
            color_to_change = "b"
        if self.current_image and color_to_change and target_color:
            self.stored_original_image = self.current_image
            ColorShiftInstance = ColorShift(self.current_image)
            ColorShiftInstance.change_color(target_color, color_to_change)
            self.process_and_update_image("modified", ColorShiftInstance)

# Run the app
if __name__ == '__main__':
    ColorShiftApp().run()
