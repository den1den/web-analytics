#Check if first argument is given
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi


export JAVA_HOME=/usr/lib/jvm/default-java
export PYTHON_PATH=`which python`

#remove output folder on hadoop
bin/hdfs dfs -rm -r -f /output_ny

#run hadoop
echo "Starting Hadoop on NewYear"
start=`date +%s`
bin/hadoop jar streaming.jar -mapper "$PYTHON_PATH mapper.py $1" -reducer "$PYTHON_PATH reducer.py $1" -input /input_ny -output /output_ny
end=`date +%s`
#get results
echo "Downloading results of NewYear"
rm -f output_ny-$1.csv
touch output_ny-$1.csv
bin/hdfs dfs -getmerge /output_ny output_ny-$1.csv

#print results
echo "Printing results of NewYear"
head output_ny-$1.csv
echo "Hadoop finished on NewYear in $((end-start)) seconds"
