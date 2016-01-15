#!/bin/sh
for i in 1 2 3 4 5 6 7 8 9
do
	echo -n "200${i}_pred_label_text.txt "
	python Purity.py author_labels/200${i}_labels.txt 200${i}_pred_label_graph.txt
done
echo -n "2010_pred_label_text.txt "
python Purity.py author_labels/2010_labels.txt 2010_pred_label_graph.txt
