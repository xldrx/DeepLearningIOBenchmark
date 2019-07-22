#!/usr/bin/env bash

echo
echo Running sync/general
mkdir -p results/sync
${FIO:=fio} --output-format=json --output=results/sync/general.json experiments/sync/general.fio

echo
echo Running async/general
mkdir -p results/async
${FIO:=fio} --output-format=json --output=results/async/general.json experiments/async/general.fio

echo
echo Running sync-direct/general
mkdir -p results/sync-direct
${FIO:=fio} --output-format=json --output=results/sync-direct/general.json experiments/sync-direct/general.fio

echo
echo Running async-indirect/general
mkdir -p results/async-indirect
${FIO:=fio} --output-format=json --output=results/async-indirect/general.json experiments/async-indirect/general.fio

echo
echo Running sync/youtube-8m-video
mkdir -p results/sync
${FIO:=fio} --output-format=json --output=results/sync/youtube-8m-video.json experiments/sync/youtube-8m-video.fio

echo
echo Running async/youtube-8m-video
mkdir -p results/async
${FIO:=fio} --output-format=json --output=results/async/youtube-8m-video.json experiments/async/youtube-8m-video.fio

echo
echo Running sync-direct/youtube-8m-video
mkdir -p results/sync-direct
${FIO:=fio} --output-format=json --output=results/sync-direct/youtube-8m-video.json experiments/sync-direct/youtube-8m-video.fio

echo
echo Running async-indirect/youtube-8m-video
mkdir -p results/async-indirect
${FIO:=fio} --output-format=json --output=results/async-indirect/youtube-8m-video.json experiments/async-indirect/youtube-8m-video.fio

echo
echo Running sync/youtube-8m-frame
mkdir -p results/sync
${FIO:=fio} --output-format=json --output=results/sync/youtube-8m-frame.json experiments/sync/youtube-8m-frame.fio

echo
echo Running async/youtube-8m-frame
mkdir -p results/async
${FIO:=fio} --output-format=json --output=results/async/youtube-8m-frame.json experiments/async/youtube-8m-frame.fio

echo
echo Running sync-direct/youtube-8m-frame
mkdir -p results/sync-direct
${FIO:=fio} --output-format=json --output=results/sync-direct/youtube-8m-frame.json experiments/sync-direct/youtube-8m-frame.fio

echo
echo Running async-indirect/youtube-8m-frame
mkdir -p results/async-indirect
${FIO:=fio} --output-format=json --output=results/async-indirect/youtube-8m-frame.json experiments/async-indirect/youtube-8m-frame.fio

echo
echo Running sync/flickr30k
mkdir -p results/sync
${FIO:=fio} --output-format=json --output=results/sync/flickr30k.json experiments/sync/flickr30k.fio

echo
echo Running async/flickr30k
mkdir -p results/async
${FIO:=fio} --output-format=json --output=results/async/flickr30k.json experiments/async/flickr30k.fio

echo
echo Running sync-direct/flickr30k
mkdir -p results/sync-direct
${FIO:=fio} --output-format=json --output=results/sync-direct/flickr30k.json experiments/sync-direct/flickr30k.fio

echo
echo Running async-indirect/flickr30k
mkdir -p results/async-indirect
${FIO:=fio} --output-format=json --output=results/async-indirect/flickr30k.json experiments/async-indirect/flickr30k.fio

echo
echo Running sync/google_house_number
mkdir -p results/sync
${FIO:=fio} --output-format=json --output=results/sync/google_house_number.json experiments/sync/google_house_number.fio

echo
echo Running async/google_house_number
mkdir -p results/async
${FIO:=fio} --output-format=json --output=results/async/google_house_number.json experiments/async/google_house_number.fio

echo
echo Running sync-direct/google_house_number
mkdir -p results/sync-direct
${FIO:=fio} --output-format=json --output=results/sync-direct/google_house_number.json experiments/sync-direct/google_house_number.fio

echo
echo Running async-indirect/google_house_number
mkdir -p results/async-indirect
${FIO:=fio} --output-format=json --output=results/async-indirect/google_house_number.json experiments/async-indirect/google_house_number.fio

echo
echo Running sync/berkeley_segmentation
mkdir -p results/sync
${FIO:=fio} --output-format=json --output=results/sync/berkeley_segmentation.json experiments/sync/berkeley_segmentation.fio

echo
echo Running async/berkeley_segmentation
mkdir -p results/async
${FIO:=fio} --output-format=json --output=results/async/berkeley_segmentation.json experiments/async/berkeley_segmentation.fio

echo
echo Running sync-direct/berkeley_segmentation
mkdir -p results/sync-direct
${FIO:=fio} --output-format=json --output=results/sync-direct/berkeley_segmentation.json experiments/sync-direct/berkeley_segmentation.fio

echo
echo Running async-indirect/berkeley_segmentation
mkdir -p results/async-indirect
${FIO:=fio} --output-format=json --output=results/async-indirect/berkeley_segmentation.json experiments/async-indirect/berkeley_segmentation.fio

echo
echo Running sync/imagenet
mkdir -p results/sync
${FIO:=fio} --output-format=json --output=results/sync/imagenet.json experiments/sync/imagenet.fio

echo
echo Running async/imagenet
mkdir -p results/async
${FIO:=fio} --output-format=json --output=results/async/imagenet.json experiments/async/imagenet.fio
