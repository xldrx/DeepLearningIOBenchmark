#! /usr/bin/env python -u
# coding=utf-8

# Deep Learning I/O Benchmark
# Copyright (C) 2018  Sayed Hadi Hashemi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import argparse
import json
import os
import re
from collections import OrderedDict
from configparser import ConfigParser
import numpy as np
import random

__author__ = 'Sayed Hadi Hashemi'


class FioRunBase:
    global_configurations = {}

    def __init__(self, name, **kwargs):
        super().__init__()
        self.global_configurations.update(kwargs)
        self.tests = OrderedDict()
        self.name = name

    def add_test(self, name, stonewall=True, **kwargs):
        test = {}
        if stonewall:
            test["stonewall"] = None
        test.update(kwargs)
        self.tests[name] = test

    @staticmethod
    def _add_section(config, name, values):
        if values:
            config[name] = values

    def generate_config_file(self):
        config = ConfigParser(allow_no_value=True)
        self._add_section(config, "global", self.global_configurations)
        for name, test in self.tests.items():
            self._add_section(config, name, test)
        file_name = 'experiments/%s.fio' % self.name
        if not os.path.exists(os.path.dirname(file_name)):
            os.mkdir(os.path.dirname(file_name))
        with open(file_name, 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)

        result_file_name = 'results/%s.json' % self.name
        result_folder = os.path.dirname(result_file_name)

        with open("experiments/run-all.bash", 'a') as script_file:
            script_file.write("echo\necho Running {}\n".format(self.name))
            script_file.write("mkdir -p {}\n".format(result_folder))
            script_file.write(
                "${{FIO:=fio}} --output-format=json --output={result_file_name} {test_file_name}\n".format(
                    test_file_name=file_name, result_file_name=result_file_name))


class FioRun(FioRunBase):
    total_size = "256g"
    global_configurations = {
        "directory": "${DEVICE}",
        "filename_format": "data-$filenum.bin",
        "thread": "1",
        "time_based": "1",
        "runtime": "30s",
        "invalidate": "1",
        "nrfiles": "1",
        "filesize": "256g",
        "fadvise_hint": "1",
        "ramp_time": "5",
        "disk_util": "1",
        "bssplit": "128k/1",
        "rw": "randread"
    }

    sync_configurations = {
        "ioengine": "sync",
        "group_reporting": "1",
        "thread": "1",
        # "norandommap" : 1,
        "numjobs": 1,
        "direct": 1
    }

    async_configurations = {
        "ioengine": "libaio",
        "direct": 1,
        "iodepth": 1
    }

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.global_configurations["filesize"] = self.total_size
        self.global_configurations["size"] = self.total_size

    def _add_sync(self, name, stonewall=True, depth=1, **kwargs):
        experiment = self.sync_configurations.copy()
        experiment["numjobs"] = depth
        experiment.update(kwargs)
        self.add_test(name, stonewall, **experiment)

    def _add_async(self, name, stonewall=True, depth=1, **kwargs):
        experiment = self.async_configurations.copy()
        experiment["iodepth"] = depth
        experiment.update(kwargs)
        self.add_test(name, stonewall, **experiment)

    def add(self, name, api, stonewall=True, depth=1, **kwargs):
        if api == "sync":
            kwargs["direct"] = 0
            return self._add_sync(name, stonewall, depth, **kwargs)
        elif api == "sync-direct":
            kwargs["direct"] = 1
            return self._add_sync(name, stonewall, depth, **kwargs)
        elif api == "async":
            kwargs["direct"] = 1
            return self._add_async(name, stonewall, depth, **kwargs)
        elif api == "async-indirect":
            kwargs["direct"] = 0
            return self._add_async(name, stonewall, depth, **kwargs)
        else:
            raise Exception("API is not found: {}".format(api))


class FioGeneralExperiment:
    depths = [1, 8, 32, 128]
    sizes = [64, 256, 1024, 4096, 32768, 262144, 2 ** 32]
    apis = ["sync", "async", "sync-direct", "async-indirect"]

    def __init__(self) -> None:
        super().__init__()

    def generate_experiment(self):
        runs = []
        for api in self.apis:
            name = "{}/general".format(api)
            run = FioRun(name=name)

            for size in self.sizes:
                for depth in self.depths:
                    run.add("{api}-d{depth}-s{size}".format(api=api, depth=depth, size=size),
                            api=api,
                            depth=depth,
                            bssplit="{}/1".format(size)
                            )
            run.generate_config_file()
            print(run.name)
            runs.append(run)


class FioDatasetExperiment:
    depths = [1, 2, 8, 32, 128]
    sequence_sizes = [1, 32, 256]
    apis = ["sync", "async", "sync-direct", "async-indirect"]

    def __init__(self, dataset_name, dataset_file=None) -> None:
        super().__init__()
        self.dataset_name = dataset_name
        if dataset_file:
            self.dataset_file = dataset_file
        else:
            self.dataset_file = os.path.realpath("dataset-stats/stat_{}.json".format(dataset_name))

    @staticmethod
    def get_distribution(sizes, sequence_size):
        ret = []
        random.seed = 42
        random.shuffle(sizes)
        chunks = []
        for i in range(0, len(sizes), sequence_size):
            chunks.append(sum(sizes[i:i + sequence_size]))

        hist = np.histogram(chunks, bins=64, density=False)
        total = sum(hist[0]) / 100
        for a1, a2, c in zip(hist[1][:-1], hist[1][1:], hist[0]):
            percentage = c // total
            mean = (a1 + a2) // 2
            if percentage >= 1:
                ret.append((int(mean), int(percentage)))
        return ret

    def get_dataset_mix(self, sequence_size=1):
        ret = {}
        with open(self.dataset_file, "r") as fp:
            stats = json.load(fp)

        for collection in stats["collections"]:
            name = collection["type"]
            sizes = collection["sizes"]
            dist = self.get_distribution(sizes, sequence_size)
            ret[name] = dist
        return ret

    @staticmethod
    def get_bssplit(dataset_mix):
        total = sum([d[1] for d in dataset_mix])
        pairs = ["{size}/{probability}".format(size=size, probability=int(probability * 100 / total))
                 for size, probability in dataset_mix]
        ret = ":".join(pairs)
        return ret

    def generate_experiment(self):
        runs = []
        for api in self.apis:
            name = "{}/{}".format(api, self.dataset_name)
            run = FioRun(name=name)

            for sequence_size in self.sequence_sizes:
                mix = self.get_dataset_mix(sequence_size)
                for mix_name, dist in mix.items():
                    for depth in self.depths:
                        run.add("{api}-{mix}-s{sequence_size}-d{depth}".format(
                            mix=mix_name, api=api, depth=depth, sequence_size=sequence_size),
                            api=api,
                            depth=depth,
                            bssplit=self.get_bssplit(dist)
                        )
            run.generate_config_file()
            print(run.name)
            runs.append(run)

    @staticmethod
    def list_datasets():
        ret = []
        for name in os.listdir("dataset-stats/"):
            ds = re.findall("stat_(.+?).json", name)
            if ds:
                ret.append(ds[0])
        return ret


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--total_size",
        type=str,
        help="Total data size",
        default="256g",
        required=False
    )

    parser.add_argument(
        "--depths",
        type=int,
        nargs='+',
        help="List of IO depth sizes.",
        default=[1, 2, 8, 32, 128],
        required=False
    )

    parser.add_argument(
        "--seqs",
        type=int,
        nargs='+',
        help="List of sequence file sizes in dataset workloads.",
        default=[1, 32, 256],
        required=False
    )

    parser.add_argument(
        "--sizes",
        type=int,
        nargs='+',
        help="List of fixed sizes in general workloads.",
        default=[64, 256, 1024, 4096, 32768, 262144, 2 ** 32],
        required=False
    )

    FLAGS, unparsed = parser.parse_known_args()

    if unparsed:
        print("Unknown argument:", unparsed)
        exit(1)

    FioRun.total_size = FLAGS.total_size

    FioGeneralExperiment.depths = FLAGS.depths
    FioGeneralExperiment.sizes = FLAGS.sizes

    FioDatasetExperiment.depths = FLAGS.depths
    FioDatasetExperiment.sequence_sizes = FLAGS.seqs


if __name__ == '__main__':
    parse_args()

    with open("experiments/run-all.bash", 'w') as script_file:
        script_file.write("#!/usr/bin/env bash\n")

    FioGeneralExperiment().generate_experiment()
    for dataset in FioDatasetExperiment.list_datasets():
        FioDatasetExperiment(dataset_name=dataset).generate_experiment()
