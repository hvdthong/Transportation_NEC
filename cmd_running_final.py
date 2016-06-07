__author__ = 'vdthoang'
from main.loadFile import load_file
import subprocess
import multiprocessing
import os
from subprocess import Popen
from sys import stdout, stdin, stderr
import time


def call_cmd(cmd):
    Popen(cmd, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)


if __name__ == '__main__':
    path = 'd:'
    name = 'twitter_cmd.txt'
    list_ = load_file(path, name)
    numProcess = 10

    for i in range(0, len(list_), numProcess):
        jobs = []
        for j in range(0, numProcess):
            if (i + j) >= len(list_):
                print 'The programming is finished'
            else:
                p = multiprocessing.Process(target=call_cmd(list_[i + j]))
                p.start()
                jobs.append(p)
        for job in jobs:
            job.join()
        time.sleep(1000)
