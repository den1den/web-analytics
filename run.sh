#Check if first argument is given
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi


export JAVA_HOME=/usr/lib/jvm/default-java
export PYTHON_PATH=`which python`

#remove output folder on hadoop
bin/hdfs dfs -rm -r -f /output

#run hadoop
echo "Starting Hadoop"
start=`date +%s`
bin/hadoop jar streaming.jar -mapper "$PYTHON_PATH mapper.py $1" -reducer "$PYTHON_PATH reducer.py $1" -input /input -output /output
end=`date +%s`
#get results
echo "Downloading results"
rm -f output-$1.csv
touch output-$1.csv
bin/hdfs dfs -getmerge /output output-$1.csv

#print results
echo "Printing results"
head output-$1.csv
echo "Hadoop finished in $((end-start)) seconds"
