#!/bin/bash
trap "exit" INT
for i in {1..50}
do
  echo "_______________________________"
  echo "             " $i "             "
  echo "_______________________________"
  python beta.py ../GenerateApp/tables_short_horiz/Data/$i/image.png
done
