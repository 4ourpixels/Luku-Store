from PIL import Image
from PIL import ImageDraw
import os


def compress_and_add_watermark(input_path, output_path, max_size, watermark_path):
    with Image.open(input_path) as image:
        # Calculate the aspect ratio to maintain the image's original proportions
        width, height = image.size
        aspect_ratio = width / height

        # Calculate the new dimensions based on the desired maximum size
        new_width = int(max_size * aspect_ratio)
        new_height = max_size

        # Resize the image while maintaining the aspect ratio
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

        # Create a copy of the resized image to apply the watermark
        watermarked_image = resized_image.copy()

        # Open the watermark image and resize it to a suitable size
        with Image.open(watermark_path) as watermark:
            # Calculate the size of the watermark based on a fraction of the image's width
            watermark_size = int(new_width * 0.2)
            watermark = watermark.resize(
                (watermark_size, watermark_size), Image.ANTIALIAS)

            # Calculate the position to place the watermark at the bottom right corner
            watermark_position = (new_width - watermark_size,
                                  new_height - watermark_size)

            # Paste the watermark onto the watermarked image
            watermarked_image.paste(
                watermark, watermark_position, mask=watermark)

        # Save the watermarked and compressed image
        watermarked_image.save(output_path)


# Define the input and output paths
input_folder = "target"
output_folder = "output"
watermark_path = "watermark.png"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate through the input folder and its subfolders
for root, dirs, files in os.walk(input_folder):
    for file in files:
        # Check if the file is an image
        if file.endswith((".png", ".jpg", ".jpeg")):
            # Compose the input and output file paths
            input_file_path = os.path.join(root, file)
            output_file_path = os.path.join(output_folder, file)

            # Compress the image, add watermark, and save it to the output folder
            compress_and_add_watermark(
                input_file_path, output_file_path, max_size=1024, watermark_path=watermark_path)
