from PIL import Image, ImageFilter, ImageEnhance
import numpy
from random import randrange

def blur_image(image):
    blurry = image.filter(ImageFilter.BLUR)
    return blurry

def enhance_edges(image):
    edgey = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return edgey

def find_contours(image):
    contoured = image.filter(ImageFilter.CONTOUR)
    return contoured

def edge_detector(image):
    edge_detector = numpy.array([[1,0,-1],
                             [0,0,0],
                             [-1,0,1]])
    
    edged = image.filter(ImageFilter.Kernel(size=(3,3), kernel=edge_detector.flatten(), scale=0.2))
    return edged

def max_image(image):
    maxy = image.filter(ImageFilter.MaxFilter(size=5))
    return maxy

def min_image(image):
    miny = image.filter(ImageFilter.MinFilter(size=5))
    return miny

def emboss_image(image):
    embossed = image.filter(ImageFilter.EMBOSS)
    return embossed

def colorfy(image):
    im = image.convert('RGBA')

    data = numpy.array(im)
    red, green, blue, alpha = data.T
    min_range = randrange(50,200)
    white_areas = (red>min_range) & (blue>min_range) & (green>min_range)
    data[..., :-1][white_areas.T] = (randrange(0,255), randrange(0,255), randrange(0,255))

    colored = Image.fromarray(data)
    return colored

def filterify(image):
    r = randrange(1,8)

    if r == 1:
        image = colorfy(image)
    elif r == 2:
        image = find_contours(image)
    elif r == 3:
        image = blur_image(image)
    elif r == 4:
        image = emboss_image(image)
    elif r == 4:
        image = min_image(image)
    elif r == 5:
        image = max_image(image)
    elif r == 6:
        image = edge_detector(image)
    elif r == 7:
        image = enhance_edges(image)

    return image

def starify(background, image, angle, alpha):

    image = image.rotate(angle)
    image = filterify(image)

    image.putalpha(alpha)

    background.paste(image, (0,0), image)
    return background

def create_new_star():

    image = Image.open("bouyant.jpg")
    star = Image.open("bouyant.jpg")
    
    angle = 90
    alpha = 255

    for i in range(4):
        star = starify(star, image, angle, alpha)
        alpha = randrange(110,130)
        angle += 90

    star = filterify(star)
    enhancer = ImageEnhance.Contrast(star)

    star = enhancer.enhance(1)
    star.show()

if __name__ == "__main__":
    print("hello gravity")
    create_new_star()
    