
import numpy as np
from scipy import misc, fftpack, ndimage
import matplotlib.pyplot as plt


def threshold(im, a=255/2, max=255):
    new = np.where(im > a, max, 0)
    return new


def normalize(image, range=1):
    if image.min() < 0:
        image += abs(image.min())
    image *= (range / (image.max()))
    return image


def remove_holes(image, structure=None):
    new_image = ndimage.morphology.binary_closing(image, structure=structure, iterations=6)
    return new_image


def remove_small_elements(image, structure=None):
    new_image = ndimage.morphology.binary_opening(image, structure=structure, iterations=7)
    return new_image


def distance_transform(image, structure=None):
    result = np.zeros_like(image).astype('int16')

    while True in image:
        # As long as there is some white parts in the image, we well continue with erosion, and add that to result
        result += image
        image = ndimage.morphology.binary_erosion(image, structure=structure)

    return result


def boundary_extraction(image, structure=None):
    new_image = image - ndimage.morphology.binary_erosion(image, structure=structure)
    return new_image


structure = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
image = misc.imread('images/noisy.tiff', flatten=True)
image = normalize(image, 255)
image = threshold(image)

""" The image before anything is done """
plt.imshow(image, cmap="gray")
plt.show()

""" All white spots are removed """
new = remove_small_elements(image)
plt.imshow(new, cmap="gray")
plt.show()

""" And all black holes are filled """
new = remove_holes(new)
plt.imshow(new, cmap="gray")
plt.show()

""" The distance transformation is computed """
distance_trans = distance_transform(new, structure=structure)
plt.imshow(distance_trans, cmap="gray")
plt.show()

""" And the boundary is computed """
boundary = boundary_extraction(new, structure=structure)
plt.imshow(boundary, cmap="gray")
plt.show()

# Saving results
misc.imsave("images/2a.png", new)
misc.imsave("images/2b.png", distance_trans)
misc.imsave("images/2c.png", boundary)
