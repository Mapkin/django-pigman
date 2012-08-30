#!/usr/bin/env python
#
# Created by John Watson on 2012-08-29.
# Copyright (c) 2012 Eightyone Labs, Inc. All rights reserved.
#


from django.conf import settings
from functools import wraps

import gearman

try:
    import cPickle as pickle
except ImportError:
    import pickle


class PickleDataEncoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, obj):
        return pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def decode(cls, string):
        return pickle.loads(string)


class PigMan(object):
    """PYthon Gearman -> pygman -> pigman."""
    def __init__(self, hosts):
        self.client = gearman.GearmanClient(hosts)
        self.client.data_encoder = PickleDataEncoder()

    @staticmethod
    def worker():
        worker = gearman.GearmanWorker(settings.PIGMAN_SERVERS)
        worker.data_encoder = PickleDataEncoder()
        return worker

    def run_job(self, task, *args, **kwargs):
        """Run a job immediately."""
        data = {
            'args': args,
            'kwargs': kwargs,
        }
        self.client.submit_job(task, data, wait_until_complete=False)

    def queue_job(self, task, *args, **kwargs):
        """Queue a job to be run later."""
        if not hasattr(self, 'queue'):
            self.queue = []

        data = {
            'args': args,
            'kwargs': kwargs,
        }
        job = {'task': task, 'data': data}
        self.queue.append(job)

    def run_queued(self):
        """Run all queued jobs."""
        assert(len(self.queue) > 0)
        self.client.submit_multiple_jobs(self.queue, wait_until_complete=False)
        del self.queue


def job(fn):
    @wraps(fn)
    def wrapper(gearman_worker, current_job):
        data = current_job.data
        return fn(*data['args'], **data['kwargs'])

    return wrapper
