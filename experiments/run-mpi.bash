#!/usr/bin/env bash
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
echo
echo Running sync/general
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/general.bash
echo
echo Running async/general
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/general.bash
echo
echo Running sync-direct/general
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/general.bash
echo
echo Running async-indirect/general
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/general.bash
echo
echo Running sync/youtube-8m-video
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/youtube-8m-video.bash
echo
echo Running async/youtube-8m-video
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/youtube-8m-video.bash
echo
echo Running sync-direct/youtube-8m-video
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/youtube-8m-video.bash
echo
echo Running async-indirect/youtube-8m-video
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/youtube-8m-video.bash
echo
echo Running sync/youtube-8m-frame
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/youtube-8m-frame.bash
echo
echo Running async/youtube-8m-frame
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/youtube-8m-frame.bash
echo
echo Running sync-direct/youtube-8m-frame
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/youtube-8m-frame.bash
echo
echo Running async-indirect/youtube-8m-frame
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/youtube-8m-frame.bash
echo
echo Running sync/flickr30k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/flickr30k.bash
echo
echo Running async/flickr30k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/flickr30k.bash
echo
echo Running sync-direct/flickr30k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/flickr30k.bash
echo
echo Running async-indirect/flickr30k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/flickr30k.bash
echo
echo Running sync/google_house_number
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/google_house_number.bash
echo
echo Running async/google_house_number
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/google_house_number.bash
echo
echo Running sync-direct/google_house_number
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/google_house_number.bash
echo
echo Running async-indirect/google_house_number
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/google_house_number.bash
echo
echo Running sync/berkeley_segmentation
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/berkeley_segmentation.bash
echo
echo Running async/berkeley_segmentation
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/berkeley_segmentation.bash
echo
echo Running sync-direct/berkeley_segmentation
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/berkeley_segmentation.bash
echo
echo Running async-indirect/berkeley_segmentation
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/berkeley_segmentation.bash
echo
echo Running sync/imagenet
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/imagenet.bash
echo
echo Running async/imagenet
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/imagenet.bash
echo
echo Running sync-direct/imagenet
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/imagenet.bash
echo
echo Running async-indirect/imagenet
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/imagenet.bash
echo
echo Running sync/COCO
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/COCO.bash
echo
echo Running async/COCO
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/COCO.bash
echo
echo Running sync-direct/COCO
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/COCO.bash
echo
echo Running async-indirect/COCO
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/COCO.bash
echo
echo Running sync/AirFreight
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/AirFreight.bash
echo
echo Running async/AirFreight
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/AirFreight.bash
echo
echo Running sync-direct/AirFreight
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/AirFreight.bash
echo
echo Running async-indirect/AirFreight
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/AirFreight.bash
echo
echo Running sync/flickr8k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync/flickr8k.bash
echo
echo Running async/flickr8k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async/flickr8k.bash
echo
echo Running sync-direct/flickr8k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/sync-direct/flickr8k.bash
echo
echo Running async-indirect/flickr8k
${MPIRUN:=mpirun} ${MPI_ARGS} bash ${SCRIPTPATH}/mpi_bootstraps/async-indirect/flickr8k.bash
