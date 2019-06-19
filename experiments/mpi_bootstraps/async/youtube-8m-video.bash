#!/usr/bin/env bash

export DEVICE=${DEVICE}/r${OMPI_COMM_WORLD_RANK}
export OUTPUT_PATH=results/async
export OUTPUT_FILE=results/async/youtube-8m-video.json.r${OMPI_COMM_WORLD_RANK}

mkdir -p ${DEVICE}
mkdir -p ${OUTPUT_PATH}

echo 	Running async/youtube-8m-video[r${OMPI_COMM_WORLD_RANK}]
${FIO:=fio} --output-format=json --output=${OUTPUT_FILE} experiments/async/youtube-8m-video.fio
echo 	Done async/youtube-8m-video[r${OMPI_COMM_WORLD_RANK}]
