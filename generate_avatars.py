from PIL import Image, ImageDraw, ImageFont
import os
import config

def create_avatar(text, output_path, size=(200, 200), bg_color="#FFFFFF", text_color="#000000"):
    """Create a simple avatar with initials."""
    print(f"Creating avatar for '{text}' at '{output_path}'")
    
    # Create new image with background
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Get initials from text
    initials = ''.join(word[0].upper() for word in text.split() if word)
    if len(initials) > 2:
        initials = initials[:2]
    
    print(f"Using initials: {initials}")
    
    # Try to load a font, fall back to default if not available
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=80)
        print("Using Helvetica font")
    except:
        print("Using default font")
        font = ImageFont.load_default()
    
    # Get text size
    text_bbox = draw.textbbox((0, 0), initials, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate text position for center alignment
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2
    
    # Draw text
    draw.text((x, y), initials, font=font, fill=text_color)
    
    # Draw circle border
    padding = 10
    draw.ellipse([padding, padding, size[0]-padding, size[1]-padding], 
                 outline=text_color, width=2)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save image
    try:
        image.save(output_path, 'PNG')
        print(f"Successfully saved avatar to {output_path}")
    except Exception as e:
        print(f"Error saving avatar: {e}")

def generate_app_logo():
    """Generate a simple app logo."""
    print("Generating app logo...")
    size = (400, 200)
    image = Image.new('RGB', size, "#FFFFFF")
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size=40)
        print("Using Helvetica font for logo")
    except:
        print("Using default font for logo")
        font = ImageFont.load_default()
    
    text = "Persona\nSimulator"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2
    
    draw.text((x, y), text, font=font, fill="#000000", align="center")
    
    try:
        image.save(config.APP_LOGO, 'PNG')
        print(f"Successfully saved app logo to {config.APP_LOGO}")
    except Exception as e:
        print(f"Error saving app logo: {e}")

def main():
    """Generate all avatar images and app logo."""
    print("\n=== Starting Avatar Generation ===\n")
    
    # Create directories if they don't exist
    print(f"Creating directories:")
    print(f"STATIC_DIR: {config.STATIC_DIR}")
    print(f"AVATARS_DIR: {config.AVATARS_DIR}")
    os.makedirs(config.STATIC_DIR, exist_ok=True)
    os.makedirs(config.AVATARS_DIR, exist_ok=True)
    
    # Generate default avatar
    print("\nGenerating default avatar...")
    create_avatar("Default User", config.DEFAULT_AVATAR)
    
    # Generate character avatars
    print("\nGenerating character avatars...")
    for char_type, char_config in config.CHARACTERS.items():
        print(f"\nProcessing {char_type}:")
        avatar_path = char_config['image']
        create_avatar(
            char_config['name'],
            avatar_path,
            bg_color=char_config['color'],
            text_color="#FFFFFF"
        )
    
    # Generate app logo
    print("\nGenerating app logo...")
    generate_app_logo()
    
    print("\n=== Avatar Generation Complete ===")
    
    # Verify files
    print("\nVerifying generated files:")
    if os.path.exists(config.APP_LOGO):
        print(f"✓ App logo exists: {config.APP_LOGO}")
    else:
        print(f"✗ App logo missing: {config.APP_LOGO}")
        
    if os.path.exists(config.DEFAULT_AVATAR):
        print(f"✓ Default avatar exists: {config.DEFAULT_AVATAR}")
    else:
        print(f"✗ Default avatar missing: {config.DEFAULT_AVATAR}")
        
    for char_type, char_config in config.CHARACTERS.items():
        avatar_path = char_config['image']
        if os.path.exists(avatar_path):
            print(f"✓ Avatar exists for {char_type}: {avatar_path}")
        else:
            print(f"✗ Avatar missing for {char_type}: {avatar_path}")

if __name__ == "__main__":
    main()
