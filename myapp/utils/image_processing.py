from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile

TARGET_SIZE = 512
WEBP_QUALITY = 50

def compress_image(uploaded_image):
    #Takes uploaded image file and returns django contentfile containg compressed WebP image

    image = Image.open(uploaded_image)
    image = ImageOps.exif_transpose(image)

    # ensurue consistent color mode
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # normalize intrinsic size for all newly uploaded images
    image = ImageOps.fit(
        image,
        (TARGET_SIZE, TARGET_SIZE),
        method=Image.LANCZOS,
        centering=(0.5, 0.5),
    )

    buffer = BytesIO()

    # save as WebP (strips metadata)
    image.save(buffer, format="WEBP", quality=WEBP_QUALITY, optimize=True)
    return ContentFile(buffer.getvalue(), name=f"{uploaded_image.name.split('.')[0]}.webp")
