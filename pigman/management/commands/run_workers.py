#!/usr/bin/env python
#
# Created by John Watson on 2012-08-29.
# Copyright (c) 2012 Eightyone Labs, Inc. All rights reserved.
#


from __future__ import print_function

from django.conf import settings
from django.core.management import BaseCommand
from multiprocessing import Process
from optparse import make_option
from photon.pigman import PigMan

import imp
import importlib
import inspect
import sys


def _find_jobs():
    def find_module(app, name):
        try:
            path = importlib.import_module(app).__path__
        except AttributeError:
            return

        try:
            imp.find_module(name, path)
        except ImportError:
            return

        return importlib.import_module("{0}.{1}".format(app, name))

    modules = filter(None, [find_module(app, 'jobs')
                            for app in settings.INSTALLED_APPS])

    # FIXME this seems a little grody.
    jobs = []
    for m in modules:
        mod_funcs = [inspect.getmembers(m, inspect.isfunction)
                     for m in modules]
        for funcs in mod_funcs:
            for fn_name, fn in funcs:
                name = "{0}.{1}".format(m.__name__.replace('.jobs', ''),
                                        fn_name)
                jobs.append((name, fn))
                print("  * found {0}".format(name))
    return jobs


def run_worker(tasks):
    worker = PigMan.worker()
    for name, fn in tasks:
        worker.register_task(name, fn)
    worker.work()


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-w',
                    '--workers',
                    action='store',
                    type='int',
                    dest='num_workers',
                    default=1,
                    help="The number of workers to spawn."),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.processes = []

    def handle(self, *args, **options):
        print("Searching for Gearman jobs...")
        jobs = _find_jobs()

        noun = "processes" if options['num_workers'] > 1 else "process"
        print("\nSpawning {0} worker {1}...".format(options['num_workers'],
                                                    noun))
        for i in xrange(0, options['num_workers']):
            p = Process(target=run_worker,
                        args=(jobs,),
                        name="worker{0}".format(i))
            self.processes.append(p)
            p.start()
            print("  * pid {0} started.".format(p.pid))

        print("\nPress <CTRL-C> to quit.")
        sys.stdout.flush()
        try:
            for p in self.processes:
                p.join()
        except KeyboardInterrupt:
            sys.exit(0)
