from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

MAX_SIZE = 960
WEBP_QUALITY = 50

def compress_image(uploaded_image):
    #Takes uploaded image file and returns django contentfile containg compressed WebP image

    image = Image.open(uploaded_image)

    # ensurue consistent color mode
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # resize image, maintain aspect ratio
    image.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)

    buffer = BytesIO()

    # save as WebP (strips metadata)
    image.save(buffer, format="WEBP", quality=WEBP_QUALITY, optimize=True)
    return ContentFile(buffer.getvalue(), name=f"{uploaded_image.name.split('.')[0]}.webp")
