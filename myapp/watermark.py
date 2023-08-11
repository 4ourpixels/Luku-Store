from PIL import Image
import os


def add_watermark(input_path, output_path, watermark_path, watermark_scale):
    with Image.open(input_path) as image:
        # Calculate the new dimensions based on the desired scale
        watermark_width = int(image.width * watermark_scale)
        watermark_height = int(image.height * watermark_scale)

        # Open the watermark image and resize it
        with Image.open(watermark_path) as watermark:
            watermark.thumbnail(
                (watermark_width, watermark_height), Image.ANTIALIAS)

            # Calculate the position to place the watermark at the bottom left corner
            watermark_position = (100, image.height - watermark.height)

            # Create a copy of the image and paste the watermark on it
            watermarked_image = image.copy()
            watermarked_image.paste(
                watermark, watermark_position, mask=watermark)

        # Save the watermarked image
        watermarked_image.save(output_path)


# Define the input and output paths
input_folder = "target"
output_folder = "output"
watermark_path = "watermark.png"
watermark_scale = 0.2  # Adjust the watermark scale as needed

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through the input folder and its subfolders
for root, dirs, files in os.walk(input_folder):
    for file in files:
        # Check if the file is an image
        if file.endswith((".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG")):
            # Compose the input and output file paths
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_folder, file)

            # Add watermark to the image and save it to the output folder
            add_watermark(input_file_path, output_file_path,
                          watermark_path, watermark_scale)
