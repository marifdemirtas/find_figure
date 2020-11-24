'''
Tool to find a bounding box for the largest in a pdf document,
prints the distance from the paper edge, starting from left, ccw.
'''

import pdf2image
import numpy as np
from PIL import ImageDraw


def read_from_path(filepath, dpi=300):
    '''
    Given a path to a pdf file and a dpi value,
    returns the first page of the pdf as a PIL image
    and returns the scale factor for px to cm conversion.
    '''
    raw_image = pdf2image.convert_from_path(filepath, dpi=dpi)[0]
    gray_image = raw_image.convert('L')
    scale_factor = 2.54 / dpi  # 1 cm = 2.54 inch
    return gray_image, scale_factor


def find_change(mat):
    '''
    Checks the rows of a matrix and returns the
    index of the first row where a color change happens.
    '''
    border = 0
    color = mat[0, 0]
    for i, vec in enumerate(mat):
        if np.any(vec != color):
            border = i
            break
    return border


def find_distances(image_data):
    '''
    Finds a bounding box around the largest figure
    in the image, returns the distances between the
    borders of the box and the page in px.
    '''
    top_distance = find_change(image_data)
    bottom_distance = find_change(np.flip(image_data, axis=0))
    left_distance = find_change(image_data[top_distance:-bottom_distance].T)
    right_distance = find_change(np.flip(image_data[top_distance:-bottom_distance].T, axis=0))
    return left_distance, bottom_distance, right_distance, top_distance


def plot_borders_on(image, distances):
    '''
    Given a PIL image and the distances of the borders,
    draws the borders on image.
    '''
    left, bottom, right, top = distances
    bottom = image.height - bottom
    right = image.width - right
    draw = ImageDraw.Draw(image)
    draw.line([(left, 0), (left, image.height)])
    draw.line([(right, 0), (right, image.height)])
    draw.line([(0, top), (image.width, top)])
    draw.line([(0, bottom), (image.width, bottom)])
    return image


if __name__ == '__main__':
    DPI = 300
    filepath = input("Enter the path to the PDF file: ")

    image, scale_factor = read_from_path(filepath, dpi=DPI)
    image_data = np.array(image)

    distances = find_distances(image_data)
    plot_borders_on(image, distances).show()

    cm_distances = [dist * scale_factor for dist in distances]
    print("Left: {:.2f} cm, bottom: {:.2f} cm, right: {:.2f} cm, top: {:.2f} cm".format(*cm_distances))
