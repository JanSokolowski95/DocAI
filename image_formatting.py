import pymupdf

from PIL import Image


def merge_imgs(images):
    background_width = max([image.width for image in images])
    background_height = sum([image.height for image in images])
    background = Image.new(
        "RGB", (background_width, background_height), (255, 255, 255)
    )
    y = 0
    for image in images:
        background.paste(image, (0, y))
        y += image.height

    return background


def img_from_pdf(stream):
    doc = pymupdf.open(stream=stream)

    imgs = []

    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        imgs.append(img)

    return merge_imgs(imgs)
