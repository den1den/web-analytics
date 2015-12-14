export JAVA_HOME=/usr/lib/jvm/default-java
export PYTHON_PATH=`which python`

#remove output folder on hadoop
bin/hdfs dfs -rm -r -f /output

#run hadoop
echo "Starting Hadoop"
start=`date +%s`
bin/hadoop jar streaming.jar -mapper "$PYTHON_PATH mapper.py $1" -reducer "$PYTHON_PATH reducer.py $1" -input /input_newyear -output /output > output.txt
end=`date +%s`
#get results
echo "Downloading results"
rm -f hadoop-output.txt
touch hadoop-output.txt
bin/hdfs dfs -getmerge /output hadoop-output.txt

#print results
echo ""
head hadoop-output.txt
echo "Hadoop finished in $((end-start)) seconds"
