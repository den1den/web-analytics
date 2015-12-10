export JAVA_HOME=/usr/lib/jvm/default-java
PYTHON_PATH=`which python`

#remove output folder on hadoop
bin/hdfs dfs -rm -r -f /output

#run hadoop
bin/hadoop jar streaming.jar -mapper "$PYTHON_PATH mapper.py" -reducer "$PYTHON_PATH reducer.py" -input /input -output /output > output.txt

#get results
bin/hdfs dfs -getmerge /output hadoop-output.txt
#print results
head hadoop-output.txt

echo "Script finished"
