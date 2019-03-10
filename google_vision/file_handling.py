import io
import os
import pdf2image
from PIL import Image

"""
Opens a SINGLE image name specified by filename and returns a list containing
a corresponding single PIL image. Returns as a list for consistency with the
PDF function.
"""
def _open_single_image(filename):
    img = Image.open(filename)
    img = img.convert(mode="RGB")  
    return [img]
    
"""
Opens a PDF and converts to a list of PIL images.
"""
def _open_pdf(filename):
    imgs = pdf2image.convert_from_path(filename)
    map((lambda i: i.convert), imgs)
    return imgs

"""
Return the raw bytestream from filename, compressed for sending
to Google Vision.
"""
def open_file(filename):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    if ext == ".png" or ext == ".jpg" or ext == ".jpeg":
        imgs = _open_single_image(filename)
    elif ext == '.pdf':
        imgs = _open_pdf(filename)
    else:
        return IOError("Not a valid image file.")
    #TODO: Compression. Should only do if image is too large to send
    return imgs

    