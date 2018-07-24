#! /usr/bin/env python -u
# coding=utf-8
import json
import os
import re
from collections import OrderedDict
from configparser import ConfigParser
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
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
        with open('experiments/%s.fio' % self.name, 'w') as configfile:
            config.write(configfile, space_around_delimiters=False)


class FioRun(FioRunBase):
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

    def add_sync(self, name, stonewall=True, depth=1, **kwargs):
        experiment = self.sync_configurations.copy()
        experiment["numjobs"] = depth
        experiment.update(kwargs)
        self.add_test(name, stonewall, **experiment)

    def add_async(self, name, stonewall=True, depth=1, **kwargs):
        experiment = self.async_configurations.copy()
        experiment["iodepth"] = depth
        experiment.update(kwargs)
        self.add_test(name, stonewall, **experiment)


class FioGeneralExperiment:
    depths = [1, 8, 32, 512]
    sizes = [64, 256, 1024, 4096, 32768, 262144, 2 ** 32]
    variations = ["sync", "async"]

    def __init__(self) -> None:
        super().__init__()

    def generate_experiment(self):
        runs = []
        for var in self.variations:
            name = "general-{}".format(var)
            run = FioRun(name=name)

            for size in self.sizes:
                for depth in self.depths:
                    func = run.add_sync if var == "sync" else run.add_async
                    func("{var}-d{depth}-s{size}".format(var=var, depth=depth, size=size),
                         depth=depth,
                         bssplit="{}/1".format(size)
                         )
            run.generate_config_file()
            print(run.name)
            runs.append(run)


class FioDatasetExperiment:
    depths = [1, 2, 8, 32, 512]
    sequence_sizes = [1, 32, 256]
    variations = ["sync", "async"]

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
        for var in self.variations:
            name = "{}-{}".format(self.dataset_name, var)
            run = FioRun(name=name)
            func = run.add_sync if var == "sync" else run.add_async

            for sequence_size in self.sequence_sizes:
                mix = self.get_dataset_mix(sequence_size)
                for mix_name, dist in mix.items():
                    for depth in self.depths:
                        func("{var}-{mix}-s{sequence_size}-d{depth}".format(
                            mix=mix_name, var=var, depth=depth, sequence_size=sequence_size),
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


if __name__ == '__main__':
    FioGeneralExperiment().generate_experiment()
    for dataset in FioDatasetExperiment.list_datasets():
        FioDatasetExperiment(dataset_name=dataset).generate_experiment()
