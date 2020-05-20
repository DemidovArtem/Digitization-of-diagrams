import color_recogn
import find_axes
import find_text
import parse_text
import column
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import cv2
import numpy as np
import math
from collections import namedtuple
import random
import sys


def x_val_for_column(columns, text_part):
    a = sorted(columns, key=lambda col: col.x_coordinate)
    for j in range(len(a)):
        a[j].x_val = text_part[j]
    return a


color_black = (0, 0, 0)
# нахождение границ столбиков
diagram_image = cv2.imread(sys.argv[1])
boarder = color_recogn.recogn_column(diagram_image, 10)
# отрисовка границ столбцов
array_of_column = color_recogn.draw_boarder(diagram_image, boarder)
# нахождение осей
lines = find_axes.find_axes(sys.argv[1])

axes = {'left': int(lines[0][0][0]),
        'right': int(lines[1][0][0]),
        'bottom': int(lines[2][0][0])}
# нахождение текста на диаграммах
bounds, counts, text = find_text.find_text(sys.argv[1], axes, array_of_column, language='English')
if counts[1] > counts[0]:
    lines.pop(0)
    bounds.pop(0)
    text.pop(0)
else:
    lines.pop(1)
    bounds.pop(1)
    text.pop(1)


# отрисовка
find_axes.draw_lines_on_image(diagram_image, lines)
find_text.draw_rectangles(diagram_image, bounds)

# заполнение значений столбиков
final_answer_column = x_val_for_column(array_of_column, text[-1])


parse_text.set_coefficients(bounds[0], text[0])

for i in range(len(final_answer_column)):
    final_answer_column[i].y_val = parse_text.get_value(final_answer_column[i].y_coordinate)

# печать всех столбиков и их значение в консоль
for i in range(len(final_answer_column)):
    print('№', i, '| название', final_answer_column[i].x_val, '| знаечние', final_answer_column[i].y_val, '\n')

cv2.imshow('image', diagram_image)
cv2.waitKey(0)
