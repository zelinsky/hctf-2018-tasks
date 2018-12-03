from PIL import Image
from random import sample
from helpers import text_helper

PIXEL_OFFSET = 5
PIXEL_INDEX = 2


def encode(text, path_orig, path_stego):
    im1 = Image.open(path_orig)
    px1 = im1.load()
    im2 = Image.new(im1.mode, im1.size)
    px2 = im2.load()

    # convert the text to a list of integers
    lst = text_helper.convert_to_list(text)

    # calculate a random distribution for the whole image
    indices = sorted(sample(range(0, im1.size[0] * im1.size[1]), len(lst)))
    indices_counter = 0

    i = 0
    for x in range(0, im1.size[0]):
        for y in range(0, im1.size[1]):
            col = px1[x, y]

            # retrieve one encoded character
            val = 0
            if indices_counter < len(indices) and indices[indices_counter] <= i:
                val = lst[indices_counter]

            # calculate the new rgb-value based on the encoded text and the pixel-offset
            if val != 0 and col[2] + val + PIXEL_OFFSET <= 255:
                col_new = (col[0], col[1], col[2] + val + PIXEL_OFFSET)
                indices_counter += 1
            else:
                col_new = (col[0], col[1], col[2] + PIXEL_OFFSET)

            # add the new has-value to the stego-image
            px2[x, y] = col_new

            i += 1

    # save the stego image
    im2.save(path_stego)


def decode(path_orig, path_stego):
    im1 = Image.open(path_orig)
    px1 = im1.load()
    im2 = Image.open(path_stego)
    px2 = im2.load()

    lst = []

    for x in range(0, im1.size[0]):
        for y in range(0, im1.size[1]):
            # subtract each pixel from stego and original
            val = px2[x, y][PIXEL_INDEX] - px1[x, y][PIXEL_INDEX]

            # if the value without the offset is larger then 0 it includes a character
            if val - PIXEL_OFFSET > 0:
                lst.append(val - PIXEL_OFFSET)

    return text_helper.convert_to_string(lst)
