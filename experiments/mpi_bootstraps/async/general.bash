#!/usr/bin/env bash

export DEVICE=${DEVICE}/r${OMPI_COMM_WORLD_RANK}
export OUTPUT_PATH=results/async
export OUTPUT_FILE=results/async/general.json.r${OMPI_COMM_WORLD_RANK}

mkdir -p ${DEVICE}
mkdir -p ${OUTPUT_PATH}

echo 	Running async/general[r${OMPI_COMM_WORLD_RANK}]
${FIO:=fio} --output-format=json --output=${OUTPUT_FILE} experiments/async/general.fio
echo 	Done async/general[r${OMPI_COMM_WORLD_RANK}]
