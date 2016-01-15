#!/bin/sh
for i in 1 2 3 4 5 6 7 8 9
do
	base="author_labels/200${i}_labels.txt"
	cmp="200${i}_pred_label_text.txt"
	echo -n "${base} (purity.py) "
	python Purity.py $base $cmp
	a=`diff $base $cmp | grep "<" | wc -l`
	b=`wc -l $base | awk '{print $1;}'`
	echo -n "${base} (custom) "
	echo `echo "$a / $b" | bc -l`
	
	cmp="200${i}_pred_label_graph.txt"
	echo -n "${base} (purity.py) "
        python Purity.py $base $cmp
        a=`diff $base $cmp | grep "<" | wc -l`
        b=`wc -l $base | awk '{print $1;}'`
        echo -n "${base} (custom) "
        echo `echo "$a / $b" | bc -l`
done
base="author_labels/2010_labels.txt"
cmp="2010_pred_label_text.txt"
echo -n "${base} (purity.py) "
python Purity.py $base $cmp
a=`diff $base $cmp | grep "<" | wc -l`
b=`wc -l $base | awk '{print $1;}'`
echo -n "${base} (custom) "
echo `echo "$a / $b" | bc -l`

cmp="2010_pred_label_graph.txt"
echo -n "${base} (purity.py) "
python Purity.py $base $cmp
a=`diff $base $cmp | grep "<" | wc -l`
b=`wc -l $base | awk '{print $1;}'`
echo -n "${base} (custom) "
echo `echo "$a / $b" | bc -l`
