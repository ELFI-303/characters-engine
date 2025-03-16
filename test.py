import os
from PIL import ImageDraw,Image,ImageOps
import numpy as np
import time
import sys

def asciiCharMat(low=32,high=255):
    char_weight = []
    for c in (chr(i) for i in range(low, high)):
        img = Image.new("RGB",(30,30),"white")
        I1 = ImageDraw.Draw(img)
        I1.text((5, 5), c, fill=(0, 0, 0))
        pixel_matrix = list(img.getdata())
        length = len(pixel_matrix)
        pixel_sum = 0
        for pixels in pixel_matrix:
            for pixel in pixels:
                pixel_sum += pixel
        weight = pixel_sum / length
        char_weight.append([c,weight])
    less = char_weight[0][1]
    more = char_weight[0][1]
    for element in char_weight:
        if element[1] <= less:
            less = element[1]
        if element[1] >= more:
            more = element[1]
    liste = []
    for element in char_weight:
        element[1] = ( (element[1] - less) / (more-less) ) * 255
        if element[1] != 84.73814626305905:
            liste.append(element)
    return liste

liste = asciiCharMat()
liste.sort(key=lambda x: x[1])

def resize_image( image: Image, length: int) -> Image:
    if image.size[0] < image.size[1]:
        resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))
        required_loss = (resized_image.size[1] - length)
        resized_image = resized_image.crop( 
            box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))
        resized_image = resized_image.resize((length,round(length*(1/1.8))))
        return resized_image
    else:
        resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))
        required_loss = resized_image.size[0] - length
        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))
        resized_image = resized_image.resize((length,round(length*0.5)))
        return resized_image
    
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def image_to_char(image: Image,inv: bool):
    image = image.convert('L')
    if inv == True:
        image = ImageOps.invert(image)
    r_image = resize_image(image,max([os.get_terminal_size().columns,os.get_terminal_size().lines]))
    image_pixels = np.asarray(r_image)
    image_low = 255
    image_high = 0
    for pixels in image_pixels:
        if np.min(pixels) <= image_low:
            image_low = np.min(pixels)
        if np.max(pixels) >= image_high:
            image_high = np.max(pixels)
    string_array = []
    for pixels in image_pixels:
        string_line = ""
        for pixel in pixels:
            pix = ((pixel - image_low ) / ( image_high - image_low )) * 255
            mini = liste[0]
            for element in liste:
                if np.abs(element[1]-pix) <= np.abs(mini[1]-pix):
                    mini = element
            string_line += mini[0]
        string_array.append(string_line)
    return string_array

def animation(gif_path: str,inv: bool):
    i=0
    with Image.open(gif_path) as im:
        im.seek(1)  # skip to the second frame
        try:
            while 1:
                im.seek(im.tell() + 1)
                im.save("gif/"+str(i)+".png")
                i+=1
        except EOFError:
            pass  # end of sequence
    charnimation = []
    for j in range(0,i,1):
        image = Image.open("gif/"+str(j)+".png")
        charimage = image_to_char(image,inv)
        charnimation.append(charimage)
        os.unlink("gif/"+str(j)+".png")

    for y in range(30):
        for frame in charnimation:
            for element in frame:
                print(element)
            time.sleep(0.05)
            for i in range(os.get_terminal_size().lines):
                print(" ")

def image(image_path: str, inv: bool):
    image = Image.open(image_path)
    charimage = image_to_char(image,inv)
    for element in charimage:
        print(element)

def charimage(path: str,inv: bool):
    if ".gif" in path:
        animation(path,inv)
    else:
        image(path,inv)


path = input("Enter the path of the file you want to convert:")
invert = input("Enter 1 to invert image and 0 for no modifications:")
inv = False
if invert == '1':
    inv = True
charimage(path,inv)