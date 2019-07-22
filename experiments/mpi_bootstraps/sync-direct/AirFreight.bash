#!/usr/bin/env bash

export DEVICE=${DEVICE}/r${OMPI_COMM_WORLD_RANK}
export OUTPUT_PATH=results/sync-direct
export OUTPUT_FILE=results/sync-direct/AirFreight.json.r${OMPI_COMM_WORLD_RANK}

mkdir -p ${DEVICE}
mkdir -p ${OUTPUT_PATH}

echo ----Running sync-direct/AirFreight[r${OMPI_COMM_WORLD_RANK}]
${FIO:=fio} --output-format=json --output=${OUTPUT_FILE} experiments/sync-direct/AirFreight.fio
echo ----Done sync-direct/AirFreight[r${OMPI_COMM_WORLD_RANK}]
