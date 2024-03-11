import matplotlib.pyplot as plt
from Genetic.image_size import ImageSize
from Genetic.population import Population
import cv2 as cv
import parameters as c

# --------------------------------------------------------------------------------------
# ---------------------------------GOAL IMAGE READING-----------------------------------
# --------------------------------------------------------------------------------------

img = cv.imread("BW-using-curves.jpg",cv.IMREAD_GRAYSCALE)

aspect_ratio = img.shape[1] / img.shape[0]

if img.shape[1] < img.shape[0]:
    new_img_height = c.IMG_SIZE
    new_img_width = int(new_img_height * aspect_ratio)
else:
    new_img_width = c.IMG_SIZE
    new_img_height = int(new_img_width / aspect_ratio)

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

