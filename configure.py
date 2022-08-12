# check for diagrams folder
import os
import random

import cv2
import numpy as np

if not os.path.exists('diagrams'):
    print("diagrams folder not found - creating...")
    os.makedirs('diagrams')
    print("diagrams folder created successfully")
    print("add your diagrams to the diagrams folder and run configure.py again")
    exit()
else:
    # count number of diagrams in folder
    diagram_count = 0
    for file in os.listdir('diagrams'):
        if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
            diagram_count += 1
    if diagram_count == 0:
        print(
            "no diagrams found in diagrams folder - add your diagrams to the diagrams folder and run configure.py again")
        exit()
    else:
        print("found " + str(diagram_count) + " diagrams in diagrams folder")

if not os.path.exists('backgrounds'):
    print("backgrounds folder not found - creating...")
    os.makedirs('backgrounds')
    print("background folder created successfully")
    print("add your backgrounds to the backgrounds folder and run configure.py again")
    exit()
else:
    # count number of backgrounds in folder
    bg_count = 0
    for file in os.listdir('diagrams'):
        if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
            bg_count += 1
    if bg_count == 0:
        print(
            "no backgrounds found in backgrounds folder - add your backgrounds to the backgrounds folder and run configure.py again")
        exit()
    else:
        print("found " + str(bg_count) + " backgrounds in backgrounds folder")
if not os.path.exists('output'):
    print("output folder not found - creating...")
    os.makedirs('output')
    print("output folder created successfully")

# check if config file exists and create if not
if not os.path.exists('config.txt'):
    print("config.txt not found - creating...")
    with open('config.txt', 'w') as f:
        f.write(
            "\nwhite_threshold = 5\ndialate_kernel = 3\nerode_kernel = 3\ndilate_iterations = 1\nerode_iterations = 3\nanti_alias_kernel = 3\nanti_alias_sigma = 4\nbackground_blur=5")
    print("config.txt created successfully")
    print("edit config.txt if needed and run configure.py again")
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

# randomly choose one diagram and one background and import using opencv
diagram = random.choice(os.listdir('diagrams'))
image = cv2.imread('diagrams/' + diagram)
bg = random.choice(os.listdir('backgrounds'))
background_image = cv2.imread('backgrounds/' + bg)

shape = image.shape
image_copy = np.copy(image)

cv2.imshow("OriginalImage", image)
cv2.waitKey(2000)
cv2.destroyAllWindows()

image_copy = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# mask
mask = cv2.threshold(image_copy, 255-white_threshold, 255, cv2.THRESH_BINARY)[1]
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
print("image generated successfully.....")
cv2.imshow("final", complete_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
