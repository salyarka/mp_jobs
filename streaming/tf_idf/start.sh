#!/usr/bin/env bash

HADOOP_STREAMING=$1
TERM=$2
INPUT_DIR=$3
STOP_WORDS=$4
ARTICLE_ID=$5
OUT_DIR="result_1"

hdfs dfs -rm -r -skipTrash ${OUT_DIR} > /dev/null

yarn jar ${HADOOP_STREAMING} \
    -D mapred.jab.name="IDF" \
    -files mapper.py,reducer.py \
    -mapper "python mapper.py -t "${TERM} \
    -combiner "python reducer.py" \
    -reducer "python reducer.py" \
    -input ${INPUT_DIR} \
    -output ${OUT_DIR} > /dev/null

OUT_DIR2="result_2"

hdfs dfs -rm -r skipTrash ${OUT_DIR2} > /dev/null

yarn jar ${HADOOP_STREAMING} \
    -D mapred.jab.name="TF" \
    -files mapper2.py,${STOP_WORDS} \
    -mapper "python mapper2.py -f "${STOP_WORDS}" -a "${ARTICLE_ID}"-t "${TERM} \
    -reducer "cat" \
    -input ${INPUT_DIR} \
    -output ${OUT_DIR2} > /dev/null

DOCUMENTS_TOTAL=$(hdfs dfs -cat ${OUT_DIR}/part* | grep 'total' | tr -d -c 0-9)
DOCUMENTS_TERM=$(hdfs dfs -cat ${OUT_DIR}/part* | grep 'term' | tr -d -c 0-9)
TF=$(hdfs dfs -cat ${OUT_DIR2}/part*)

python idf_tf.py -t $DOCUMENTS_TOTAL -d $DOCUMENTS_TERM -f $TF
