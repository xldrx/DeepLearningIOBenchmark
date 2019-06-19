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
import random
import re
from abc import ABC
from collections import OrderedDict
from configparser import ConfigParser
from pathlib import Path

import numpy as np

from dio import defaults

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

    def generate_config_file(self, run_scripts):
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

        for script in run_scripts:
            script.add_test(test_name=self.name,
                            test_file_name=file_name,
                            result_path=result_folder,
                            result_file_name=result_file_name)


class FioRun(FioRunBase):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.global_configurations["filesize"] = defaults.total_size

    def _add_sync(self, name, stonewall=True, depth=1, **kwargs):
        experiment = defaults.sync_configurations.copy()
        experiment["numjobs"] = depth
        experiment.update(kwargs)
        self.add_test(name, stonewall, **experiment)

    def _add_async(self, name, stonewall=True, depth=1, **kwargs):
        experiment = defaults.async_configurations.copy()
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


class FioExperimentBase(ABC):
    def __init__(self, *, run_scripts=None):
        if run_scripts:
            self.run_scripts = run_scripts
        else:
            self.run_scripts = []

    def generate_experiment(self):
        raise NotImplementedError()


class FioGeneralExperiment(FioExperimentBase):
    def __init__(self, *, run_scripts=None):
        super().__init__(run_scripts=run_scripts)

    def generate_experiment(self):
        runs = []
        for api in defaults.apis:
            name = "{}/general".format(api)
            run = FioRun(name=name)

            for size in defaults.sizes:
                for depth in defaults.depths:
                    run.add("{api}-d{depth}-s{size}".format(api=api, depth=depth, size=size),
                            api=api,
                            depth=depth,
                            bssplit="{}/1".format(size)
                            )
            run.generate_config_file(self.run_scripts)
            print(run.name)
            runs.append(run)


class FioDatasetExperiment(FioExperimentBase):
    def __init__(self, dataset_name, dataset_file=None, *, run_scripts=None) -> None:
        super().__init__(run_scripts=run_scripts)
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
        for api in defaults.apis:
            name = "{}/{}".format(api, self.dataset_name)
            run = FioRun(name=name)

            for sequence_size in defaults.sequence_sizes:
                mix = self.get_dataset_mix(sequence_size)
                for mix_name, dist in mix.items():
                    for depth in defaults.depths:
                        run.add("{api}-{mix}-s{sequence_size}-d{depth}".format(
                            mix=mix_name, api=api, depth=depth, sequence_size=sequence_size),
                            api=api,
                            depth=depth,
                            bssplit=self.get_bssplit(dist)
                        )
            run.generate_config_file(self.run_scripts)
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


class ScriptFileBase(ABC):
    def __init__(self, filename):
        self._filename = filename
        dir_path = Path(os.path.dirname(filename))
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

        with open(self._filename, "w") as fp:
            self._begin(fp)

    def add_test(self, *args, **kwargs):
        with open(self._filename, "a") as fp:
            self._add_test(fp, *args, **kwargs)

    def _begin(self, fp):
        raise NotImplementedError()

    def _add_test(self, fp, *args, **kwargs):
        raise NotImplementedError()


class RunAllScript(ScriptFileBase):
    def __init__(self, filename):
        super().__init__(filename)

    def _begin(self, fp, *args, **kwargs):
        fp.write("#!/usr/bin/env bash\n")

    def _add_test(self, fp, *, test_name, test_file_name, result_path, result_file_name):
        fp.write(defaults.run_all_script_body.format(
            test_name=test_name, test_file_name=test_file_name, result_path=result_path,
            result_file_name=result_file_name))

class MPIBootstrapScript(ScriptFileBase):
    def __init__(self, filename):
        super().__init__(filename)

    def _begin(self, fp, *args, **kwargs):
        fp.write("#!/usr/bin/env bash\n")

    def _add_test(self, fp, *, test_file_name, result_path, result_file_name):
        fp.write(defaults.mpi_bootstrap_script_body.format(
            test_file_name=test_file_name, result_path=result_path, result_file_name=result_file_name
        ))


class RunMPIScript(ScriptFileBase):
    def __init__(self, filename):
        super().__init__(filename)

    def _begin(self, fp, *args, **kwargs):
        fp.write("#!/usr/bin/env bash\n")
        fp.write("SCRIPT=`realpath $0`\n")
        fp.write("SCRIPTPATH=`dirname $SCRIPT`\n")

    def _add_test(self, fp, *, test_name, test_file_name, result_path, result_file_name):
        fp.write("echo\necho Running {}\n".format(test_name))
        test_bootstrap_path = "mpi_bootstraps/" + test_name + ".bash"

        test_bootstrap_script = MPIBootstrapScript(
            os.path.join(os.path.dirname(self._filename), test_bootstrap_path))

        test_bootstrap_script.add_test(test_file_name=test_file_name,
                                       result_path=result_path,
                                       result_file_name=result_file_name)

        fp.write("${{MPIRUN:=mpirun}} ${{MPI_ARGS}} bash ${{SCRIPTPATH}}/{test_bootstrap_path}\n".format(
            test_bootstrap_path=test_bootstrap_path))


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
        default=[256, 1024, 4096, 32768, 262144, 2 ** 32],
        required=False
    )

    parser.add_argument(
        "--apis",
        type=str,
        nargs='+',
        help="List of APIs to test.",
        default=["sync", "async", "sync-direct", "async-indirect"],
        required=False
    )

    FLAGS, unparsed = parser.parse_known_args()

    if unparsed:
        print("Unknown argument:", unparsed)
        exit(1)

    defaults.total_size = FLAGS.total_size
    defaults.depths = FLAGS.depths
    defaults.sizes = FLAGS.sizes
    defaults.sequence_sizes = FLAGS.seqs
    defaults.apis = FLAGS.apis


def main():
    parse_args()
    scripts = [RunAllScript(defaults.run_all_script_path), RunMPIScript(defaults.run_mpi_script_path)]
    FioGeneralExperiment(run_scripts=scripts).generate_experiment()
    for dataset in FioDatasetExperiment.list_datasets():
        FioDatasetExperiment(dataset_name=dataset, run_scripts=scripts).generate_experiment()


if __name__ == "__main__":
    raise NotImplementedError()
