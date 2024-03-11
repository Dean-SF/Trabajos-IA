import matplotlib.pyplot as plt

from Genetic.individual import Individual
from Genetic.image_size import ImageSize
import cv2 as cv
import parameters as c

from time import sleep


img = cv.imread("BW-using-curves.jpg",cv.IMREAD_GRAYSCALE)

aspect_ratio = img.shape[1] / img.shape[0]

if img.shape[1] < img.shape[0]:
    new_img_height = c.IMG_SIZE
    new_img_width = int(new_img_height * aspect_ratio)
else:
    new_img_width = c.IMG_SIZE
    new_img_height = int(new_img_width / aspect_ratio)

img = cv.resize(img,(new_img_width,new_img_height),interpolation=cv.INTER_LANCZOS4)

ImageSize.height = new_img_height
ImageSize.width = new_img_width

indiv = Individual()

indiv.calculate_fitness(img.ravel())

print(indiv.fitness)

other_indiv = Individual()

other_indiv.calculate_fitness(img.ravel())

print(other_indiv.fitness)

child_indiv = indiv.crossover(other_indiv.DNA)

child_indiv.calculate_fitness(img.ravel())

print(child_indiv.fitness)
'''
plt.imshow(indiv.img,cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.figure(1)

plt.imshow(other_indiv.img,cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.figure(2)

plt.imshow(child_indiv.img,cmap='gray', vmin=0, vmax=255)
plt.axis('off')
plt.figure(3)
'''

f, subplots = plt.subplots(1,3)

subplots[0].imshow(indiv.img,cmap='gray', vmin=0, vmax=255)
subplots[0].axis('off')
subplots[1].imshow(other_indiv.img,cmap='gray', vmin=0, vmax=255)
subplots[1].axis('off')
subplots[2].imshow(child_indiv.img,cmap='gray', vmin=0, vmax=255)
subplots[2].axis('off')


plt.show()