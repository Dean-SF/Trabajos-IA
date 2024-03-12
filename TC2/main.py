import matplotlib.pyplot as plt
from Genetic.image_size import ImageSize
from Genetic.population import Population
import cv2 as cv
import parameters as c

# --------------------------------------------------------------------------------------
# ---------------------------------GOAL IMAGE READING-----------------------------------
# --------------------------------------------------------------------------------------

# Reading the original picture
img = cv.imread("BW-using-curves.jpg",cv.IMREAD_GRAYSCALE)

# calculate the original aspect ratio to mantain it in the final downscale size
aspect_ratio = img.shape[1] / img.shape[0] 

# Here we downscale the biggest dimension of the picture
# to the maximum image size defined in parameters
# the other dimension is adjusted according to the aspect ratio
if img.shape[1] < img.shape[0]:
    new_img_height = c.IMG_SIZE
    new_img_width = int(new_img_height * aspect_ratio)
else:
    new_img_width = c.IMG_SIZE
    new_img_height = int(new_img_width / aspect_ratio)

# Original picture downscaled
img = cv.resize(img,(new_img_width,new_img_height),interpolation=cv.INTER_LANCZOS4) 

# Global variables
ImageSize.height = new_img_height
ImageSize.width = new_img_width

# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# -----------------------------GENETIC ALGORITHM INIT PROCESS---------------------------
# --------------------------------------------------------------------------------------

Genetic = Population(img.ravel())
last_img = Genetic.process_generations()

# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# ---------------------------SHOW GOAL IMAGE AND LAST GENERATION------------------------
# --------------------------------------------------------------------------------------
_, subplots = plt.subplots(1,2)

subplots[0].imshow(img,cmap='gray', vmin=0, vmax=255)
subplots[0].axis('off')
subplots[1].imshow(last_img,cmap='gray', vmin=0, vmax=255)
subplots[1].axis('off')

plt.show()

# --------------------------------------------------------------------------------------

