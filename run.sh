echo "Script started"
export JAVA_HOME=/usr/lib/jvm/default-java
export PYTHON_PATH=`which python`

#remove output folder on hadoop
bin/hdfs dfs -rm -r -f /output

#run hadoop
bin/hadoop jar streaming.jar -mapper "$PYTHON_PATH mapper.py" -reducer "$PYTHON_PATH reducer.py" -input /input -output /output > output.txt
#get results
rm -f hadoop-output.txt
touch hadoop-output.txt
bin/hdfs dfs -getmerge /output hadoop-output.txt

#print results
head hadoop-output.txt
echo "Script finished"

