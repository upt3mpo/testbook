#!/usr/bin/env python3
"""
Setup script to create placeholder images for Testbook.
This creates simple colored images with text labels to simulate real photos.
Cross-platform: Works on Windows, macOS, and Linux.
"""

import os
import platform

from PIL import Image, ImageDraw, ImageFont

# Try to import requests for better HTTP handling
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    import urllib.request

    HAS_REQUESTS = False

# Detect operating system
SYSTEM = platform.system()
print(f"🖥️  Detected OS: {SYSTEM}")

# Create directories if they don't exist
os.makedirs("backend/static/images", exist_ok=True)
os.makedirs("backend/static/videos", exist_ok=True)


def get_font(size):
    """Get a font appropriate for the operating system"""
    font_paths = []

    if SYSTEM == "Darwin":  # macOS
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "/Library/Fonts/Arial.ttf",
        ]
    elif SYSTEM == "Windows":
        font_paths = [
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\Arial.ttf",
            "C:\\Windows\\Fonts\\calibri.ttf",
            "C:\\Windows\\Fonts\\segoeui.ttf",
        ]
    elif SYSTEM == "Linux":
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",  # Arch Linux
        ]

    # Try each font path
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except (OSError, IOError):
            continue

    # Fallback to default font
    print("⚠️  Using default font (system font not found)")
    return ImageFont.load_default()


def create_image(filename, text, color, size=(800, 600)):
    """Create a simple placeholder image with text"""
    img = Image.new("RGB", size, color=color)
    draw = ImageDraw.Draw(img)

    # Get cross-platform font
    font = get_font(40)

    # Calculate text position (centered)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)

    # Draw text
    draw.text(position, text, fill="white", font=font)

    # Save image
    img.save(f"backend/static/images/{filename}")
    print(f"✅ Created: {filename}")


def create_avatar(filename, initial, color):
    """Create a simple avatar with an initial"""
    img = Image.new("RGB", (200, 200), color=color)
    draw = ImageDraw.Draw(img)

    # Get cross-platform font
    font = get_font(80)

    bbox = draw.textbbox((0, 0), initial, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((200 - text_width) // 2, (200 - text_height) // 2)

    draw.text(position, initial, fill="white", font=font)
    img.save(f"backend/static/images/{filename}")
    print(f"✅ Created: {filename}")


def download_image(source, filename):
    """Download a real image from a URL or Unsplash photo ID"""
    filepath = f"backend/static/images/{filename}"

    # Set headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://unsplash.com/",
    }

    # Determine if it's a direct URL or Unsplash photo ID
    if source.startswith("http://") or source.startswith("https://"):
        # Direct URL
        print(f"Downloading {filename} from {source[:50]}...")
        urls_to_try = [source]
    elif source.startswith("unsplash:"):
        # Unsplash photo ID
        photo_id = source.replace("unsplash:", "")
        print(f"Downloading {filename} from Unsplash (photo: {photo_id})...")
        urls_to_try = [
            f"https://unsplash.com/photos/{photo_id}/download?force=true",
            f"https://images.unsplash.com/photo-{photo_id}?w=1600&q=80",
        ]
    else:
        print(f"❌ Invalid source format for {filename}: {source}")
        return False

    # Try with requests library first (if available)
    if HAS_REQUESTS:
        for url in urls_to_try:
            try:
                response = requests.get(
                    url, headers=headers, allow_redirects=True, timeout=15
                )
                content_type = response.headers.get("content-type", "")

                if response.status_code == 200 and (
                    "image" in content_type or len(response.content) > 1000
                ):
                    with open(filepath, "wb") as f:
                        f.write(response.content)

                    # Verify it's actually an image
                    try:
                        img = Image.open(filepath)
                        img.verify()
                        print(f"✅ Downloaded: {filename}")
                        return True
                    except:
                        os.remove(filepath)
                        continue
            except Exception:
                continue

    # Fallback: try with urllib
    for url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                content_type = response.headers.get("content-type", "")
                if "image" in content_type:
                    image_data = response.read()
                    with open(filepath, "wb") as f:
                        f.write(image_data)
                    print(f"✅ Downloaded: {filename}")
                    return True
        except Exception:
            continue

    print(f"❌ Failed to download {filename}")
    print("   Falling back to placeholder image")
    return False


# Optional: Map filenames to download URLs for real images
# Supports both Unsplash photo IDs and direct image URLs
# Format:
#   "filename.jpg": "unsplash:photo-id" for Unsplash photos
#   "filename.jpg": "https://direct-url-to-image.jpg" for direct URLs
# Note: This project now uses real photos - download feature available if needed
real_images = {}

# Create avatar images for users
avatars = [
    ("avatar-sarah.jpg", "S", "#E91E63"),
    ("avatar-mike.jpg", "M", "#2196F3"),
    ("avatar-emma.jpg", "E", "#9C27B0"),
    ("avatar-alex.jpg", "A", "#FF5722"),
    ("avatar-lisa.jpg", "L", "#4CAF50"),
    ("avatar-james.jpg", "J", "#FF9800"),
    ("avatar-olivia.jpg", "O", "#00BCD4"),
    ("avatar-daniel.jpg", "D", "#795548"),
    ("default-avatar.jpg", "?", "#9E9E9E"),
]

print("Creating avatar images...")
for filename, initial, color in avatars:
    filepath = f"backend/static/images/{filename}"
    if os.path.exists(filepath):
        print(f"Skipped: {filename} (already exists)")
    else:
        create_avatar(filename, initial, color)

# Create post images
images = [
    ("christmas-family.jpg", "🎄 Christmas Family Photo", "#c41e3a"),
    ("kids-playing.jpg", "👶 Kids Playing", "#87CEEB"),
    ("mountain-view.jpg", "🏔️ Mountain View", "#4169E1"),
    ("sunset-hike.jpg", "🌅 Sunset During Hike", "#FF6347"),
    ("dog-buddy.jpg", "🐕 Buddy the Dog", "#8B4513"),
    ("forest-morning.jpg", "🌲 Forest Morning", "#228B22"),
    ("gaming-setup.jpg", "🎮 Gaming Setup", "#1a1a1a"),
    ("gym-workout.jpg", "💪 Gym Workout", "#FF4500"),
    ("meal-prep.jpg", "🥗 Healthy Meal Prep", "#32CD32"),
    ("pasta-dish.jpg", "🍝 Amazing Pasta", "#FFD700"),
    ("tokyo-street.jpg", "🇯🇵 Tokyo Street", "#DC143C"),
    ("code-screen.jpg", "💻 Clean Code", "#2F4F4F"),
]

print("\nCreating post images...")
downloaded_count = 0
skipped_count = 0
created_count = 0

for filename, text, color in images:
    filepath = f"backend/static/images/{filename}"

    # Check if image already exists
    if os.path.exists(filepath):
        print(f"Skipped: {filename} (already exists)")
        skipped_count += 1
    # Check if we should download a real image instead
    elif filename in real_images:
        success = download_image(real_images[filename], filename)
        if success:
            downloaded_count += 1
        else:
            # Fallback to placeholder if download fails
            create_image(filename, text, color)
            created_count += 1
    else:
        create_image(filename, text, color)
        created_count += 1

print("\n✅ Setup complete!")
print(f"   🖥️  Platform: {SYSTEM}")
if skipped_count > 0:
    print(f"   📸 Kept {skipped_count} existing image(s)")
if created_count > 0:
    print(f"   🎨 Created {created_count} placeholder image(s)")
if downloaded_count > 0:
    print(f"   ⬇️  Downloaded {downloaded_count} real image(s)")
print("\n💡 Tip: To download real images, add URLs to the 'real_images' dictionary")
print("   in setup_images.py and delete the image files you want to replace.")
print("\n🌍 This script works on Windows, macOS, and Linux!")
