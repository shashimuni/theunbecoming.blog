import os
import re
import shutil
from PIL import Image

# Paths (using raw strings to handle Windows backslashes correctly)
posts_dir = r"C:\Users\munis\Documents\theunbecoming.blog_hugo\content\english\blog"
attachments_dir = r"C:\Users\munis\Documents\theunbecoming.blog_obsidian"
static_images_dir = r"C:\Users\munis\Documents\theunbecoming.blog_hugo\static\images"

# Standard image size (4:3 aspect ratio)
TARGET_SIZE = (1600, 1200)

# Ensure the static images directory exists
os.makedirs(static_images_dir, exist_ok=True)

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format [[image.png]]
        images = re.findall(r'\[\[([^]]*\.(?:png|jpg|jpeg|gif|bmp|svg|webp))\]\]', content)
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            # Prepare the Markdown-compatible link with %20 replacing spaces
            markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
            content = content.replace(f"[[{image}]]", markdown_image)
            
            # Step 4: Process the image file
            image_source = os.path.join(attachments_dir, image)
            image_destination = os.path.join(static_images_dir, image)
            
            if os.path.exists(image_source):
                try:
                    with Image.open(image_source) as img:
                        # Create a new image with the target size and a white background
                        resized_img = Image.new("RGB", TARGET_SIZE, (255, 255, 255))
                        
                        # Preserve aspect ratio and center the image
                        img.thumbnail(TARGET_SIZE, Image.ANTIALIAS)
                        
                        # Calculate position to paste centered
                        x_offset = (TARGET_SIZE[0] - img.width) // 2
                        y_offset = (TARGET_SIZE[1] - img.height) // 2
                        resized_img.paste(img, (x_offset, y_offset))
                        
                        # Save resized image to a temporary location
                        temp_resized_path = os.path.join(static_images_dir, f"resized_{image}")
                        resized_img.save(temp_resized_path)
                        
                        # Explicitly copy the resized image to the static directory
                        shutil.copy(temp_resized_path, image_destination)
                        
                        print(f"Resized and copied: {image}")
                        
                        # Remove the temporary resized file
                        os.remove(temp_resized_path)
                        
                except Exception as e:
                    print(f"Failed to process {image}: {e}")
            
            else:
                # If the image does not need resizing or is not an image, copy directly
                shutil.copy(image_source, image_destination)
                print(f"Copied without resizing: {image}")
        
        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

print("Markdown files processed, images resized, and copied successfully.")
