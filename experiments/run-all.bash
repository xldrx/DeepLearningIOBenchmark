#!/usr/bin/env bash
echo
echo Running sync/general
${FIO:=fio} --output-format=json --output=results/sync/general.json experiments/sync/general.fio
echo
echo Running async/general
${FIO:=fio} --output-format=json --output=results/async/general.json experiments/async/general.fio
echo
echo Running sync-direct/general
${FIO:=fio} --output-format=json --output=results/sync-direct/general.json experiments/sync-direct/general.fio
echo
echo Running async-indirect/general
${FIO:=fio} --output-format=json --output=results/async-indirect/general.json experiments/async-indirect/general.fio
echo
echo Running sync/youtube-8m-video
${FIO:=fio} --output-format=json --output=results/sync/youtube-8m-video.json experiments/sync/youtube-8m-video.fio
echo
echo Running async/youtube-8m-video
${FIO:=fio} --output-format=json --output=results/async/youtube-8m-video.json experiments/async/youtube-8m-video.fio
echo
echo Running sync-direct/youtube-8m-video
${FIO:=fio} --output-format=json --output=results/sync-direct/youtube-8m-video.json experiments/sync-direct/youtube-8m-video.fio
echo
echo Running async-indirect/youtube-8m-video
${FIO:=fio} --output-format=json --output=results/async-indirect/youtube-8m-video.json experiments/async-indirect/youtube-8m-video.fio
echo
echo Running sync/youtube-8m-frame
${FIO:=fio} --output-format=json --output=results/sync/youtube-8m-frame.json experiments/sync/youtube-8m-frame.fio
echo
echo Running async/youtube-8m-frame
${FIO:=fio} --output-format=json --output=results/async/youtube-8m-frame.json experiments/async/youtube-8m-frame.fio
echo
echo Running sync-direct/youtube-8m-frame
${FIO:=fio} --output-format=json --output=results/sync-direct/youtube-8m-frame.json experiments/sync-direct/youtube-8m-frame.fio
echo
echo Running async-indirect/youtube-8m-frame
${FIO:=fio} --output-format=json --output=results/async-indirect/youtube-8m-frame.json experiments/async-indirect/youtube-8m-frame.fio
echo
echo Running sync/flickr30k
${FIO:=fio} --output-format=json --output=results/sync/flickr30k.json experiments/sync/flickr30k.fio
echo
echo Running async/flickr30k
${FIO:=fio} --output-format=json --output=results/async/flickr30k.json experiments/async/flickr30k.fio
echo
echo Running sync-direct/flickr30k
${FIO:=fio} --output-format=json --output=results/sync-direct/flickr30k.json experiments/sync-direct/flickr30k.fio
echo
echo Running async-indirect/flickr30k
${FIO:=fio} --output-format=json --output=results/async-indirect/flickr30k.json experiments/async-indirect/flickr30k.fio
echo
echo Running sync/google_house_number
${FIO:=fio} --output-format=json --output=results/sync/google_house_number.json experiments/sync/google_house_number.fio
echo
echo Running async/google_house_number
${FIO:=fio} --output-format=json --output=results/async/google_house_number.json experiments/async/google_house_number.fio
echo
echo Running sync-direct/google_house_number
${FIO:=fio} --output-format=json --output=results/sync-direct/google_house_number.json experiments/sync-direct/google_house_number.fio
echo
echo Running async-indirect/google_house_number
${FIO:=fio} --output-format=json --output=results/async-indirect/google_house_number.json experiments/async-indirect/google_house_number.fio
echo
echo Running sync/berkeley_segmentation
${FIO:=fio} --output-format=json --output=results/sync/berkeley_segmentation.json experiments/sync/berkeley_segmentation.fio
echo
echo Running async/berkeley_segmentation
${FIO:=fio} --output-format=json --output=results/async/berkeley_segmentation.json experiments/async/berkeley_segmentation.fio
echo
echo Running sync-direct/berkeley_segmentation
${FIO:=fio} --output-format=json --output=results/sync-direct/berkeley_segmentation.json experiments/sync-direct/berkeley_segmentation.fio
echo
echo Running async-indirect/berkeley_segmentation
${FIO:=fio} --output-format=json --output=results/async-indirect/berkeley_segmentation.json experiments/async-indirect/berkeley_segmentation.fio
echo
echo Running sync/imagenet
${FIO:=fio} --output-format=json --output=results/sync/imagenet.json experiments/sync/imagenet.fio
echo
echo Running async/imagenet
${FIO:=fio} --output-format=json --output=results/async/imagenet.json experiments/async/imagenet.fio
echo
echo Running sync-direct/imagenet
${FIO:=fio} --output-format=json --output=results/sync-direct/imagenet.json experiments/sync-direct/imagenet.fio
echo
echo Running async-indirect/imagenet
${FIO:=fio} --output-format=json --output=results/async-indirect/imagenet.json experiments/async-indirect/imagenet.fio
echo
echo Running sync/COCO
${FIO:=fio} --output-format=json --output=results/sync/COCO.json experiments/sync/COCO.fio
echo
echo Running async/COCO
${FIO:=fio} --output-format=json --output=results/async/COCO.json experiments/async/COCO.fio
echo
echo Running sync-direct/COCO
${FIO:=fio} --output-format=json --output=results/sync-direct/COCO.json experiments/sync-direct/COCO.fio
echo
echo Running async-indirect/COCO
${FIO:=fio} --output-format=json --output=results/async-indirect/COCO.json experiments/async-indirect/COCO.fio
echo
echo Running sync/AirFreight
${FIO:=fio} --output-format=json --output=results/sync/AirFreight.json experiments/sync/AirFreight.fio
echo
echo Running async/AirFreight
${FIO:=fio} --output-format=json --output=results/async/AirFreight.json experiments/async/AirFreight.fio
echo
echo Running sync-direct/AirFreight
${FIO:=fio} --output-format=json --output=results/sync-direct/AirFreight.json experiments/sync-direct/AirFreight.fio
echo
echo Running async-indirect/AirFreight
${FIO:=fio} --output-format=json --output=results/async-indirect/AirFreight.json experiments/async-indirect/AirFreight.fio
echo
echo Running sync/flickr8k
${FIO:=fio} --output-format=json --output=results/sync/flickr8k.json experiments/sync/flickr8k.fio
echo
echo Running async/flickr8k
${FIO:=fio} --output-format=json --output=results/async/flickr8k.json experiments/async/flickr8k.fio
echo
echo Running sync-direct/flickr8k
${FIO:=fio} --output-format=json --output=results/sync-direct/flickr8k.json experiments/sync-direct/flickr8k.fio
echo
echo Running async-indirect/flickr8k
${FIO:=fio} --output-format=json --output=results/async-indirect/flickr8k.json experiments/async-indirect/flickr8k.fio
