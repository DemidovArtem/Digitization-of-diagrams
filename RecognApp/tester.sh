#!/bin/bash
# This script will sequentially analyze first 50 images from directory "D:\images".
# After analyzing each image press any key to continue processing next image.
trap "exit" INT
for i in {1..50}
do
  echo "_______________________________"
  echo "             " $i "             "
  echo "_______________________________"
  python beta.py $1/$i/image.png
done
