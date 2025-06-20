import os
from PIL import Image, ImageDraw, ImageFont
import random

# Create directory for product images if it doesn't exist
images_dir = 'app/static/images/products'
os.makedirs(images_dir, exist_ok=True)

# List of product image filenames from our sample products
image_files = [
    # Men's products
    'mens_dress_shirt.jpg',
    'mens_chino.jpg',
    'mens_blazer.jpg',
    'mens_belt.jpg',
    'mens_sweater.jpg',
    'mens_suit.jpg',
    'mens_ties.jpg',
    'mens_jeans.jpg',
    'mens_socks.jpg',
    'mens_wallet.jpg',
    
    # Women's products
    'womens_blouse.jpg',
    'womens_skirt.jpg',
    'womens_cardigan.jpg',
    'womens_handbag.jpg',
    'womens_blazer.jpg',
    'womens_scarf.jpg',
    'womens_dress.jpg',
    'womens_boots.jpg',
    'womens_sunglasses.jpg',
    'womens_necklace.jpg',
    
    # Kids' products
    'kids_tshirt.jpg',
    'kids_jeans.jpg',
    'kids_jacket.jpg',
    'kids_backpack.jpg',
    'kids_sneakers.jpg',
    'kids_pajama.jpg',
    'kids_dress.jpg',
    'kids_rainboots.jpg',
    'kids_winterset.jpg',
    'kids_swimset.jpg'
]

# Colors for different categories
category_colors = {
    'mens': (100, 100, 200),  # Blue-ish
    'womens': (200, 100, 150),  # Pink-ish
    'kids': (100, 200, 100)   # Green-ish
}

def create_placeholder_image(filename, size=(600, 600)):
    # Determine category from filename
    category = None
    for cat in category_colors.keys():
        if cat in filename:
            category = cat
            break
    
    if not category:
        category = 'mens'  # Default
    
    # Create a new image with a colored background
    color = category_colors[category]
    
    # Add some randomness to the color
    color = tuple(max(0, min(255, c + random.randint(-30, 30))) for c in color)
    
    image = Image.new('RGB', size, color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a font, fall back to default if not available
    try:
        font = ImageFont.truetype('Arial.ttf', 40)
    except IOError:
        font = ImageFont.load_default()
    
    # Extract product name from filename
    product_name = ' '.join(filename.split('_')[1:]).split('.')[0].title()
    
    # Draw product name
    text_width, text_height = draw.textsize(product_name, font=font) if hasattr(draw, 'textsize') else (200, 40)
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    
    # Draw text with shadow for better visibility
    draw.text((position[0]+2, position[1]+2), product_name, font=font, fill=(0, 0, 0))
    draw.text(position, product_name, font=font, fill=(255, 255, 255))
    
    # Draw a border
    draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline=(200, 200, 200), width=5)
    
    # Save the image
    image_path = os.path.join(images_dir, filename)
    image.save(image_path)
    print(f"Created {image_path}")

def main():
    print(f"Creating {len(image_files)} placeholder images...")
    for filename in image_files:
        create_placeholder_image(filename)
    print("Done creating placeholder images!")

if __name__ == "__main__":
    main() 