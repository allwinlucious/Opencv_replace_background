#check for diagrams folder
import os
import numpy as np
import cv2
import random
import time

if not os.path.exists('diagrams'):
    print("diagrams folder not found - creating...")
    os.makedirs('diagrams')
    print("diagrams folder created successfully")
    print("add your diagrams to the diagrams folder and run configure.py again")
    exit()
else:
    #count number of diagrams in folder
    diagram_count = 0
    for file in os.listdir('diagrams'):
        if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
            diagram_count += 1
    if diagram_count == 0:
        print("no diagrams found in diagrams folder - add your diagrams to the diagrams folder and run configure.py again")
        exit()
    else:
        print("found " + str(diagram_count) + " diagrams in diagrams folder")

#tune the paramaeters for one diagram

threshold_bg = 20

print("tune the parameters for one diagram  :")
image = cv2.imread("diagrams/" + random.choice(os.listdir("diagrams/")))
shape = image.shape
image_copy = np.copy(image)
image_copy = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Originaldiagram", image)
cv2.waitKey(2000)
cv2.destroyAllWindows()
#create mask

print("removing background...")
lower = np.array([255 - threshold_bg])
upper = np.array([255])
mask = cv2.threshold(image_copy, 250, 255, cv2.THRESH_BINARY)[1]
masked_image = np.copy(image)
masked_image[mask != 0] = [0, 0, 0]
cv2.imshow("backgroundRemoved",masked_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
