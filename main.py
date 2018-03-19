from PIL import Image
import numpy as np
from functools import reduce
import numpy.ma as ma

# Image to characters by Thijs Hermans
# example in the bottom
def image_to_characters(input_file, repword='LIBRARY', sizes = [120, 9999]):

    # Open Image
    im = Image.open(input_file)

    # Resize image to smaller size (aspect ratio to smallest available vector size)
    im.thumbnail(sizes, Image.ANTIALIAS)
    im = _remove_transparency(im)
    im_mat = np.asarray(im)

    # Create boolean mask of black and white image, scale to max value
    lim = np.max(im_mat[:,:,:3])
    im_lims = np.array([lim,lim,lim])
    im_mask = np.array([[any((im_lims / 2) < col[:3]) for col in row] for row in im_mat])

    # Create the character matrix on which the mask will be applied
    shp = im_mask.shape
    sz = im_mask.size
    reps = np.ceil(sz / len(repword))
    str_arr = np.array([a for a in (repword * int(reps))])[:sz]
    str_arr = str_arr.reshape(shp)

    # Return empty spaces for all false statements in the image mask
    result_arr = np.array([[' ' if im_mask[ix, iy] else y for iy, y in enumerate(x)] for ix, x in enumerate(str_arr)])
    hls = [['\n'] for x in result_arr]
    result_arr = np.hstack((result_arr, hls))
    result = ''.join([y for x in result_arr for y in x])

    return result


# source: https://stackoverflow.com/questions/35859140/remove-transparency-alpha-from-any-image-using-pil
def _remove_transparency(im, bg_colour=(255, 255, 255)):

    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im

# testing
if __name__ == '__main__':

    # image_to_characters(filename, sizes) returns the transformed image in a numpy string array
    result = image_to_characters('world_map_bw.png')

    # save results in old-school python style
    text_file = open("result.txt", "w")
    text_file.write(result)
    text_file.close()


