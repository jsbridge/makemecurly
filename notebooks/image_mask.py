# This code applies the Figaro1k masks to the images

import numpy as np
import cv2
from glob import glob 

def masks(type, tt):

    # Read in the images and masks
    images = np.sort(glob('Figaro1k/Original/'+tt+'/'+type+'/*'))
    masks = np.sort(glob('Figaro1k/GT/'+tt+'/'+type+'/*'))

    for i, img in enumerate(images):

        # Get filename
        fn = img.split('/')[-1]

        im = cv2.imread(img)
        mk = cv2.imread(masks[i])

        # Combine mask and image
        new_img = im * mk

        # Save image
        cv2.imwrite('Figaro1k/Combo/'+tt+'/'+type+'/'+fn, new_img)

    return
