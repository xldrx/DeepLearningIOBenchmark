#!/usr/bin/env bash

export DEVICE=${DEVICE}/r${OMPI_COMM_WORLD_RANK}
export OUTPUT_PATH=results/sync-direct
export OUTPUT_FILE=results/sync-direct/imagenet.json.r${OMPI_COMM_WORLD_RANK}

mkdir -p ${DEVICE}
mkdir -p ${OUTPUT_PATH}

echo ----Running sync-direct/imagenet[r${OMPI_COMM_WORLD_RANK}]
${FIO:=fio} --output-format=json --output=${OUTPUT_FILE} experiments/sync-direct/imagenet.fio
echo ----Done sync-direct/imagenet[r${OMPI_COMM_WORLD_RANK}]
