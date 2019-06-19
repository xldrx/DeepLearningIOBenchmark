# Deep Learning IO Benchmark
The goal of this project is to simulate a deep learning training job load on a storage device.

## Requirements
* `fio`. It has been tested on `3.8`.
* `Python 3`. Tested on `3.6`.
* packages in `requirements.txt`. Install by:
    ```bash
    pip3 install -r requirements.txt
    ```


## Run
1. choose a set of API and workload.
2. Set `DEVICE` environment variable to the target mount point.
    ```bash
    export DEVICE=/mnt/target
    ```
3. Run the `fio`:
    ```bash
    fio --output-format=json --output=OUTPUT experiments/API/WORKLOAD.fio
    ```
    where `API` is the chosen API, `WORKLOAD` is the workload, and `OUTPUT` is the output file.
    for example for `sync` API and `imagenet` workload run:
    ```bash
    fio --output-format=json --output=results.json experiments/sync/imagenet.fio
    ```

* (Alternative) 3. Run all tests by:
    ```bash
    export DEVICE=/mnt/target
    bash experiments/run-all.bash
    ```
    The results will be stored in `results/` folder.

## API sets
There are 4 different API sets for the benchmarks.
While all sets simulate the same workload, they use different kernel calls for reading the data.
Some APIs may not be supported on some systems. 
* `sync`: Use the standard `read` API. It is compatible with all settings.
* `async`: This uses `AIO` library. Usually it provides better throughput in exchange to worst latency. It may not be supported on some platforms.
* `sync-direct`: It uses the same API as `sync` but bypass the kernel. In theory, it should have better performance, but may not be fully supported in some settings. 
* `async-indirect`: It uses the same API as `async` but *does not* bypass the kernel. In theory, it should have worse performance than `async` but supports more settings. 

## Workloads
1. **General**: This workload simulates random read of a fixed size buffer.
2. **Dataset**: This workload simulates a random read of examples of different sizes following the distribution of a dataset. Additionally, this workload mimicking the behavior of sequence files (e.g. `TFRecords`) by reading a group of examples together.

## Datasets
The following datasets are included in this suite:
* AirFreight
* COCO
* berkeley_segmentation
* flickr30k
* flickr8k
* google_house_number
* imagenet
* youtube-8m-frame
* youtube-8m-video
 
# Notes
* Make sure the data is not cached in memory before running any benchmark. To flush the cache run the following as `root`:
    ```bash
    free && sync && echo 3 > /proc/sys/vm/drop_caches && free
    ```
* Make the total data size is large enough (at least 10 times the size of memory) while still fit on the disk. By default, this value is `256GB`. If you need to change this value, generate new benchmarks by running:
    ```bash
    python3 -m dio --total_size=256g
    ``` 

## Add a Custom Workload
1. Add a stat file to `dataset-stats` folder. The name of the file should be in form of `stat_DATASET.json` where DATASET is the name of the dataset. See `dataset-stats/stat_imagenet.json` to learn about the structure of stats files.
2. generate new benchmarks by running:
    ```bash
    python3 dio/generate_fio.py
    ``` 

## Advance Options
```text
python3 dio/generate_fio.py -h
usage: generate_fio.py [-h] [--total_size TOTAL_SIZE]
                       [--depths DEPTHS [DEPTHS ...]] [--seqs SEQS [SEQS ...]]
                       [--sizes SIZES [SIZES ...]]

optional arguments:
  -h, --help            show this help message and exit
  --total_size TOTAL_SIZE
                        Total data size
  --depths DEPTHS [DEPTHS ...]
                        List of IO depth sizes.
  --seqs SEQS [SEQS ...]
                        List of sequence file sizes in dataset workloads.
  --sizes SIZES [SIZES ...]
                        List of fixed sizes in general workloads.
  --apis APIS [APIS ...]
                        List of APIs to test.
```

## License
Deep Learning I/O Benchmark
Copyright (C) 2018  Sayed Hadi Hashemi.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
