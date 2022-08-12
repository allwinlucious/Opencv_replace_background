# check for diagrams folder
import os
import random

import cv2
import numpy as np

def parse_config():
    if not os.path.exists('config.txt'):
        print("config.txt not found - please run configure.py before running this file")
        exit()
    else:
        with open('config.txt', 'r') as f:
            config = f.readlines()
            # parse config file
            for line in config:
                if line.startswith('white_threshold'):
                    white_threshold = int(line.split('=')[1])
                if line.startswith('dialate_kernel'):
                    dialate_kernel = int(line.split('=')[1])
                if line.startswith('erode_kernel'):
                    erode_kernel = int(line.split('=')[1])
                if line.startswith('dilate_iterations'):
                    dilate_iterations = int(line.split('=')[1])
                if line.startswith('erode_iterations'):
                    erode_iterations = int(line.split('=')[1])
                if line.startswith('anti_alias_kernel'):
                    anti_alias_kernel = int(line.split('=')[1])
                if line.startswith('anti_alias_sigma'):
                    anti_alias_sigma = int(line.split('=')[1])
                if line.startswith('background_blur'):
                    background_blur = int(line.split('=')[1])
    return white_threshold, dialate_kernel, erode_kernel, dilate_iterations, erode_iterations, anti_alias_kernel, anti_alias_sigma, background_blur
def replace_background(diagram, background):
    image = cv2.imread('diagrams/' + diagram)
    background_image = cv2.imread('backgrounds/' + bg)
    #parse config
    white_threshold, dialate_kernel, erode_kernel, dilate_iterations, erode_iterations, anti_alias_kernel, anti_alias_sigma, background_blur = parse_config()
    shape = image.shape

    cv2.imshow("OriginalImage", image)
    cv2.waitKey(200)
    cv2.destroyAllWindows()

    image_copy = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # mask
    mask = cv2.threshold(image_copy, 255 - white_threshold , 255, cv2.THRESH_BINARY)[1]
    masked_image = np.copy(image)
    masked_image[mask != 0] = [0, 0, 0]

    # dialate
    kernel = np.ones((dialate_kernel, dialate_kernel), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=dilate_iterations)
    masked_image = np.copy(image)
    masked_image[mask != 0] = [0, 0, 0]

    # erosion
    kernel = np.ones((erode_kernel, erode_kernel), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=erode_iterations)
    masked_image = np.copy(image)
    masked_image[mask != 0] = [0, 0, 0]

    # anti-alias
    mask = cv2.GaussianBlur(mask, (anti_alias_kernel, anti_alias_kernel), sigmaX=anti_alias_sigma, sigmaY=anti_alias_sigma,
                            borderType=cv2.BORDER_DEFAULT)
    mask = (2 * (mask.astype(np.float32)) - 255.0).clip(0, 255).astype(np.uint8)
    masked_image = np.copy(image)
    masked_image[mask != 0] = [0, 0, 0]

    # add background
    background_image = cv2.cvtColor(background_image, cv2.COLOR_BGR2RGB)
    # resize to diagram's shape
    background_image = cv2.resize(background_image, (shape[1], shape[0]), interpolation=cv2.INTER_AREA)
    crop_background = background_image[0:shape[0], 0:shape[1]]  # crop if needed
    # add blur
    crop_background = cv2.blur(crop_background, (background_blur, background_blur), 0)
    crop_background[mask == 0] = [0, 0, 0]
    complete_image = masked_image + crop_background
    print("background replaced successfully.")
    return complete_image

#for all images in folder diagrams read one by one and replace background
for filename in os.listdir('diagrams'):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg"):
        bg = random.choice(os.listdir('backgrounds'))
        cv2.imwrite('output/' + filename, replace_background(filename, bg))
        print("image saved successfully.")

