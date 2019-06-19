#!/usr/bin/env bash

export DEVICE=${DEVICE}/r${OMPI_COMM_WORLD_RANK}
export OUTPUT_PATH=results/sync
export OUTPUT_FILE=results/sync/google_house_number.json.r${OMPI_COMM_WORLD_RANK}

mkdir -p ${DEVICE}
mkdir -p ${OUTPUT_PATH}

echo 	Running sync/google_house_number[r${OMPI_COMM_WORLD_RANK}]
${FIO:=fio} --output-format=json --output=${OUTPUT_FILE} experiments/sync/google_house_number.fio
echo 	Done sync/google_house_number[r${OMPI_COMM_WORLD_RANK}]
