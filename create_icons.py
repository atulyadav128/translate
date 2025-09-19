# Simple script to create PWA icons
from PIL import Image, ImageDraw
import os

def create_icon(size, filename):
    # Create a simple icon with AYBot text
    img = Image.new('RGB', (size, size), color='#007bff')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple robot icon
    # Body
    draw.rectangle([size//4, size//3, 3*size//4, 2*size//3], fill='white')
    # Head
    draw.rectangle([size//3, size//6, 2*size//3, size//3], fill='white')
    # Eyes
    draw.ellipse([size//3 + size//12, size//6 + size//12, size//3 + size//8, size//6 + size//8], fill='#007bff')
    draw.ellipse([2*size//3 - size//8, size//6 + size//12, 2*size//3 - size//12, size//6 + size//8], fill='#007bff')
    
    img.save(filename)
    print(f"Created {filename}")

# Create icons
create_icon(192, 'icon-192.png')
create_icon(512, 'icon-512.png')
