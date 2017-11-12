#!/usr/bin/env bash

OUT_DIR="result_"$(date +"%s%6N")
NUM_REDUCERS=8

hdfs dfs -rm -r -skipTrash ${OUT_DIR} > /dev/null

yarn jar $1 \
    -D mapred.jab.name="Stop words" \
    -D mapreduce.job.reduces=${NUM_REDUCERS} \
    -files mapper.py,reducer.py,$3 \
    -mapper "python sw_mapper.py -f"$4 \
    -combiner "python sw_reducer.py" \
    -reducer "python sw_reducer.py" \
    -input $2 \
    -output ${OUT_DIR} > /dev/null


OUT_DIR2="result_"$(date +"%s%6N")
NUM_REDUCERS=8

hdfs dfs -rm -r -skipTrash ${OUT_DIR2} > /dev/null

yarn jar $1 \
    -D mapred.jab.name="Stop words percent" \
    -D mapreduce.job.reduces=${NUM_REDUCERS} \
    -files mapper2.py,reducer.py,$3 \
    -mapper "python sw_mapper2.py"$4 \
    -reducer "python sw_reducer.py" \
    -input ${OUT_DIR} \
    -output ${OUT_DIR2} > /dev/null

hdfs dfs -cat ${OUT_DIR2}/* | grep 'total\|stops' | \
awk 'BEGIN {total=0; stops=0}{if ($1=="stops") {stops+=$2} else {total+=$2}}END{print stops/total*100}'
