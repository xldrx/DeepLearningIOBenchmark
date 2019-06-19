#!/usr/bin/env bash

export DEVICE=${DEVICE}/r${OMPI_COMM_WORLD_RANK}
export OUTPUT_PATH=results/sync
export OUTPUT_FILE=results/sync/flickr30k.json.r${OMPI_COMM_WORLD_RANK}

mkdir -p ${DEVICE}
mkdir -p ${OUTPUT_PATH}

echo 	Running sync/flickr30k[r${OMPI_COMM_WORLD_RANK}]
${FIO:=fio} --output-format=json --output=${OUTPUT_FILE} experiments/sync/flickr30k.fio
echo 	Done sync/flickr30k[r${OMPI_COMM_WORLD_RANK}]
