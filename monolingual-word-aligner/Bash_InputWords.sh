#!/bin/bash
for (( i=0; i<=15; i++))
do
  python3 InputWords.py sqls/re_$i
done
