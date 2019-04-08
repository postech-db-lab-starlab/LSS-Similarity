#!/bin/bash
$p=0
for (( i=0; i<=32; i++))
do
  let p=40000+$i
  python corenlp.py -p $p > log/$i &
done
