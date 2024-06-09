# THIS IS EXPERIMENTAL NOT STABLE SOLUTION() IT WORKS BUT I DON'T KNOW HOW IT EFFECTIVE IS!!!! IT'S NOT FOR PRODUCTION
import os
import glob
from PIL import Image

# Request the path to the folder with JPG images
input_folder = input("Enter the path to the folder with JPG images: ").strip()
# Request the path to the folder for saving WEBP images
output_folder = input("Enter the path to the folder for saving WEBP images: ").strip()

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Iterate over all .jpg files in the input folder
for jpg_file in glob.glob(os.path.join(input_folder, '*.jpg')):
    # Open the image
    image = Image.open(jpg_file)
    
    # Get the file name without the extension
    base_name = os.path.basename(jpg_file).rsplit('.', 1)[0]
    
    # Path to save the converted image
    webp_file = os.path.join(output_folder, f'{base_name}.webp')
    
    # Save the image in WEBP format
    image.save(webp_file, 'WEBP')

    print(f'Converted: {jpg_file} to {webp_file}')

print("All conversions complete.")
