from os import name
from turtle import st
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageOps, ImageChops
import numpy
from random import randint, randrange, choice

names = ["jewel","star","ruby","emerald","moon","planet","galaxy","shard","fragment","eye","wheel","pattern","reality","ghost","flower","eye"]
descriptions = ["green","chaos","dark","light","ruptured","timeless","broken","spidery","forever","ruby","cobalt","diamond","starlight","twilight"]

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

def invert(image):
    inverted = ImageOps.invert( image.convert('RGB'))
    return inverted

def greyscale(image):
    grey = image.convert("1")
    return grey

def chops(image):
    choppy = ImageChops.offset(image, int(image.size[0]/2))
    return choppy

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
    r = randrange(1,12)

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
    elif r == 8:
        image = invert(image)
    elif r == 9:
        image = chops(image)
    elif r == 10:
        image = color_shift(image)
    elif r == 11:
        image = random_gradient(image)
    else:
        pass

    return image

def color_shift(image):

    i = image.convert('LA')
    L,A = i.split()
    S, = Image.new('L', i.size, randrange(100,255)).split()

    colorified = Image.merge('RGBA', (L,L,S,A))
    r = randrange(1,3)
    if r == 1:
        colorified = Image.merge('RGBA', (S,L,L,A))
    if r == 2:
        colorified = Image.merge('RGBA', (L,S,L,A))

    return colorified

def starify(background, image, angle, alpha):

    image = image.rotate(angle)
    image = filterify(image)

    image.putalpha(alpha)

    background.paste(image, (0,0), image)
    return background

def draw_lines(image):
    draw = ImageDraw.Draw(image)
    colors = ["black","white","red","orange","yellow","green","blue","purple"]

    line_color = choice(colors)

    #top
    for i in range(0, image.size[0], randrange(50,image.size[0])):
        line_color = choice(colors)
        draw.line((i,0) + (image.size[0]/2,image.size[1]/2), width = randrange(1,8),fill=line_color)

    #bottom
    for i in range(0, image.size[0], randrange(50, image.size[0])):
        line_color = choice(colors)
        draw.line((i,image.size[1]) + (image.size[0]/2,image.size[1]/2), width = randrange(2,6),fill=line_color)

    #left
    for i in range(0, image.size[1], randrange(50,image.size[0])):
        line_color = choice(colors)
        draw.line((0,i) + (image.size[0]/2,image.size[1]/2), width = randrange(1,9),fill=line_color)

    return image

def random_gradient(image):
    img = Image.new('RGB',(image.width,image.height),"#FFFFFF")
    ImageDraw.draw = ImageDraw.Draw(img)

    r,g,b = randint(0,255),randint(0,255),randint(0,255)
    dr = (randint(0,255) - r)/img.width
    dg = (randint(0,255) - r)/img.width
    db = (randint(0,255) - r)/img.width

    for i in range(img.width):
        r,g,b = r+dr, g+dg,b+db
        ImageDraw.draw.line((i,0,i,img.width), fill=(int(r),int(g),int(b)))


    star = greyscale(image)
    star = star.convert("RGBA")
    img = img.convert("RGBA")

    blended = Image.blend(img, star, alpha=0.4)

    return blended

def create_new_star():

    image = Image.open("bouyant.jpg")
    star = Image.open("forever_shard801.jpg")
    
    angle = 90
    alpha = 255
    steps = randrange(2,7)

    for i in range(steps):
        star = starify(star, image, angle, alpha)
        alpha = randrange(110,130)
        angle += 90


    star = random_gradient(star)
    star = filterify(star)
    
    enhancer = ImageEnhance.Contrast(star)

    star = enhancer.enhance(5)

    enhancer = ImageEnhance.Brightness(star)
    
    factor = randrange(1,5)
    star = enhancer.enhance(factor)

    if randrange(1,10) < 2:
        star = draw_lines(star)

    if randrange(1,10) < 2.5:
        star = chops(star)

    star_name = choice(descriptions) + "_" + choice(names) + str(randrange(1000)) 
    star.save(star_name + ".png", "PNG")
    star.show()