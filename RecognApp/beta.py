import color_recogn
import find_axes
import find_text
import parse_text
import column
import xlsxwriter
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import cv2
import xlsxwriter
import numpy as np
import math
from collections import namedtuple
import random
import sys


def x_val_for_column(array_of_column, text):
    columns = sorted(array_of_column, key=lambda col: col.x_coordinate)
    for i, column in enumerate(columns):
        column.x_val = text[i]
    return columns


def table_creation(data):
    full_path = "./" + sys.argv[1].split(".")[0] + ".xlsx"
    workbook = xlsxwriter.Workbook(full_path)

    worksheet = workbook.add_worksheet()
    for column in range(len(data)):
        worksheet.write(column, 0, data[column].x_val)
        worksheet.write(column, 1, data[column].y_val)
    workbook.close()


color_black = (0, 0, 0)
# нахождение границ столбиков
diagram_image = cv2.imread(sys.argv[1])
boarder = color_recogn.recogn_column(diagram_image, 10)
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

# фикс смещения
min = 0
for i in range(len(bounds[0])):
    if (int(bounds[0][i]['bottom'])) > min:
        min = int(bounds[0][i]['bottom'])

bias = abs(min - lines[1][0][0])
# обнуление неправильно сдвига на случай, если не была распознана подпись, ближайшая к оси ox, или если ее нет
if bias > 5:
    bias = 0

# заполнение значений столбиков
final_answer_column = x_val_for_column(array_of_column, text[1])
parse_text.set_coefficients(bounds[0], text[0])

for i in range(len(final_answer_column)):
    final_answer_column[i].y_val = parse_text.get_value(final_answer_column[i].y_coordinate, bias)

table_creation(final_answer_column)

cv2.imshow('image', diagram_image)
cv2.waitKey(0)
