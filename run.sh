export JAVA_HOME=/usr/lib/jvm/default-java
PYTHON_PATH=`which python`

bin/hdfs dfs -rm -r -f /output
bin/hadoop jar streaming.jar -mapper "$PYTHON_PATH mapper.py" -reducer "$PYTHON_PATH reducer.py" -input /input -output /output > output.txt

echo "Done"
