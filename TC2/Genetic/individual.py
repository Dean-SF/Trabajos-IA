from Genetic.image_size import ImageSize
from random import randint,sample
from copy import deepcopy
import parameters as c
import numpy as np
import cv2 as cv

# Basic stroke data, DNA is composed of strokes, we'll be evolving each stroke per generation.
class Stroke:

    def __init__(self, pos: tuple[int,int], size: int, angle: int, brush_type: int, dark_level: int):
        self.size = size

        self.posx = 0
        self.posy = 0
        self.setPos(pos)

        self.angle = angle

        self.brush_type = brush_type

        self.dark_level = dark_level

    def copy(self, other):
        self.size = other.size

        self.posx = other.posx
        self.posy = other.posy

        self.angle = other.angle

        self.brush_type = other.brush_type

        self.dark_level = other.dark_level

    # When setting size, we recalculate position in case the stroke is out of bounds.
    def setSize(self,size):
        self.size = size
        self.setPos((self.posx,self.posy))

    # When setting position, we need to calculate if the stroke is out of bounds in x or y direction.
    def setPos(self,pos: tuple[int,int]):
        new_x = pos[0]
        new_y = pos[1]

        stroke_max_x_pos = new_x+self.size
        stroke_max_y_pos = new_y+self.size

        if(stroke_max_x_pos >= ImageSize.width):
            new_x -= (stroke_max_x_pos - ImageSize.width)
        
        if(stroke_max_y_pos >= ImageSize.height):
            new_y -= (stroke_max_y_pos - ImageSize.height)

        self.posx = new_x
        self.posy = new_y

# the Individual is represented by DNA, it's composition was described in the previous class.
class Individual:

    brush_templates: list = None # Here we'll have the pictures of the brushes.

    def __init__(self, DNA = None):
        if(DNA is not None):
            self.DNA: list[Stroke] = deepcopy(DNA)
        else:
            self.DNA: list[Stroke] = []
            self._create_rand_individual()

        self.img = np.zeros(shape=(ImageSize.height,ImageSize.width)) # Blank image.
        self.fitness = None
        if(self.brush_templates == None):
            self._load_brushes()
        

    # Randomized the DNA
    def _create_rand_individual(self):
        for _ in range(c.STROKES_PER_INDIVIDUAL):
            size = randint(c.STROKE_MIN_SIZE,c.STROKE_MAX_SIZE)

            x = randint(0,ImageSize.width)
            y = randint(0,ImageSize.height)

            angle = randint(c.MIN_ANGLE,c.MAX_ANGLE)

            brush_type = randint(0,c.NUM_BRUSHES-1)

            dark_level = randint(c.MIN_DARK_LEVEL,c.MAX_DARK_LEVEL)

            new_brush = Stroke((x,y),size,angle,brush_type,dark_level)
            self.DNA.append(new_brush)

    # We take each stroke and put it in an image.
    def create_img(self):
        #self.img = np.zeros(shape=(ImageSize.height,ImageSize.width))
        for stroke in self.DNA:
            posy = stroke.posy
            posx = stroke.posx
            size = stroke.size

            # Getting the stroke drawing
            stroke_drawing = self._create_stroke_drawing(stroke)

            # Putting the stroke in the image we're creating.
            self.img[posy:posy+size,posx:posx+size][stroke_drawing>c.BACKGROUND_THRESHOLD] = stroke_drawing[stroke_drawing>c.BACKGROUND_THRESHOLD]

    # Each stroke have a size, rotation and dark level (represents how dark the 
    # color is), in this function we make the drawing to put it in the image.
    def _create_stroke_drawing(self,stroke: Stroke):
        size = stroke.size

        # Getting the brush from which the stroke is going to be generated
        stroke_drawing = self.brush_templates[stroke.brush_type]

        # Sizing the stroke
        stroke_drawing = cv.resize(stroke_drawing,(size,)*2,interpolation=cv.INTER_LANCZOS4)

        # Rotating the stroke.
        rotation = cv.getRotationMatrix2D((size//2,)*2,stroke.angle,1)
        stroke_drawing = cv.warpAffine(stroke_drawing,rotation,(size,)*2)

        # Masking the stoke
        _,stroke_drawing = cv.threshold(stroke_drawing, 1, 255, cv.THRESH_BINARY)

        # Changing how dark the stroke is going to be.
        stroke_drawing = cv.add(stroke_drawing, (stroke.dark_level*-1))
        
        return stroke_drawing

    def _load_brushes(self):
        self.brush_templates = []
        for i in range(c.NUM_BRUSHES):
            brush = cv.imread(f"brushes/{i}.jpg",cv.IMREAD_GRAYSCALE)
            self.brush_templates.append(brush)

    def calculate_fitness(self,goal):
        self.create_img()
        ravel_img = self.img.ravel()
        self.fitness = np.sum((ravel_img - goal)**2)

    def mutate(self):
        new_individual = Individual(self.DNA) # new mutated individual.

        # Here we get the strokes we are going to mutate.
        for stroke in sample(new_individual.DNA,randint(c.MIN_STROKE_TO_MUTATE,c.MAX_STROKE_TO_MUTATE)): 
            
            # Here we randomize which aspects of the stroke we are going to mutate.
            # We change a random amount of properties but which properties are changed 
            # is also random, for instance, 4 properties can be changed multiple times 
            # but there is a possibility that the properties changing aren't the same.
            # Can be changed later after experimentation.
            for i in sample(range(5),randint(c.MIN_MUTATIONS_STROKE,c.MAX_MUTATIONS_STROKE)):
                match i:
                    case 0:
                        stroke.setSize(randint(c.STROKE_MIN_SIZE,c.STROKE_MAX_SIZE))
                    case 1:
                        x = randint(0,ImageSize.width)
                        y = randint(0,ImageSize.height)
                        stroke.setPos((x,y))
                    case 2:
                        stroke.angle = randint(c.MIN_ANGLE,c.MAX_ANGLE)
                    case 3:
                        stroke.brush_type = randint(0,c.NUM_BRUSHES-1)
                    case 4:
                        stroke.dark_level = randint(c.MIN_DARK_LEVEL,c.MAX_DARK_LEVEL)
        
        return new_individual
    
    def crossover(self, other_dna: list[Stroke]):
        new_individual = Individual(self.DNA) # new crossed individual

        # We randomly select which strokes from the other DNA are going to change. 
        for i in sample(range(c.STROKES_PER_INDIVIDUAL),randint(c.MIN_STROKE_TO_CROSS,c.MAX_STROKE_TO_CROSS)):
            new_individual.DNA[i].copy(other_dna[i])
        return new_individual
    
    # Default Python operator overloading
    def __repr__(self):
        return str(self.fitness)
    
    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness
            