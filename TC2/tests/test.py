import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import parameters as c

img = cv.imread("BW-using-curves.jpg",cv.IMREAD_GRAYSCALE)

aspect_ratio = img.shape[1] / img.shape[0]

if img.shape[1] < img.shape[0]:
    new_img_height = c.IMG_SIZE
    new_img_width = int(new_img_height * aspect_ratio)
else:
    new_img_width = c.IMG_SIZE
    new_img_height = int(new_img_width / aspect_ratio)

img = cv.resize(img,(new_img_width,new_img_height),interpolation=cv.INTER_LANCZOS4)

# ------------------------------------------------------------------------


brush = cv.imread("brushes/1.jpg",cv.IMREAD_GRAYSCALE)

center = (brush.shape[1]//2,brush.shape[0]//2)

angle = 45

rotation = cv.getRotationMatrix2D(center,angle,1.0)

rotated = cv.warpAffine(brush,rotation,(brush.shape[1],brush.shape[0]))

brush_max = cv.resize(rotated,(c.BRUSH_MAX_SIZE,c.BRUSH_MAX_SIZE),interpolation=cv.INTER_LANCZOS4)
_, brush_max1 = cv.threshold(brush_max, 1, 255, cv.THRESH_BINARY)

brush_max = cv.add(brush_max1, -225)

brush_min = cv.resize(rotated,(c.BRUSH_MIN_SIZE,c.BRUSH_MIN_SIZE),interpolation=cv.INTER_LANCZOS4)


# ------------------------------------------------------------------------


blank_img = np.zeros(shape=(new_img_height,new_img_width))

new = blank_img.copy()

posx = 0
posy = 0

new[posy:posy+c.BRUSH_MAX_SIZE,posx:posx+c.BRUSH_MAX_SIZE][brush_max>c.BACKGROUND_THRESHOLD] = brush_max[brush_max>c.BACKGROUND_THRESHOLD]

posx = 50
posy = 50

brush_max = cv.add(brush_max1, -185)
new[posy:posy+c.BRUSH_MAX_SIZE,posx:posx+c.BRUSH_MAX_SIZE][brush_max>c.BACKGROUND_THRESHOLD] = brush_max[brush_max>c.BACKGROUND_THRESHOLD]
#new[posy:posy+c.BRUSH_MIN_SIZE,posx:posx+c.BRUSH_MIN_SIZE][brush_min>c.BACKGROUND_THRESHOLD] = brush_min[brush_min>c.BACKGROUND_THRESHOLD]

plt.imshow(new,cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.show()

