#!/bin/bash
for (( i=0; i<=63; i++))
do
  python Batch_aligner.py $i sentences1 > alignment5/re_$i &
done
