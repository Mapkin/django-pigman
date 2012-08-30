django-pigman - Gearman Integration for Django
==============================================

django-pigman provides Gearman integration for Django. It enables discovery
of job modules for applications listed in `INSTALLED_APPS` and provides a
management command for launching workers.

Installation
------------

You can install `django-pigman` using `pip`:

    $ pip install git+git@github.com/Mapkin/django-pigman.git

To enable `django-pigman` for your project you need to add `pigman` to
your `INSTALLED_APPS`:

    INSTALLED_APPS += ('pigman',)

Additionally, you must specify one or more Gearman servers in your
`settings.py`:

    PIGMAN_SERVERS = (
        '10.0.0.1',
        '10.0.0.2',
    )

Workers
-------
### Registering Jobs

Create a file called `jobs.py` in any of your Django apps, and define as many
job functions as you need. Each job function should be decorated with the
`pigman.job` decorator:

    @pigman.job
    def reverse(text):
        return text[::-1]

Jobs can take positional and keyword arguments.

### Job Names

Jobs are given the name of their import path, with 'jobs' stripped out for
readability purposes. E.g., if the `reverse` example above were in
`frob/jobs.py`, its task name would be `frob.reverse`.

### Running Workers

To start a worker, run `python manage.py run_workers`. It will discover and
serve all registered jobs. To start more than one worker, use the `-w` option:

    $ python manage.py run_workers -w 5
    Searching for Gearman jobs...
      * found frob.reverse

    Spawning 5 worker processes...
      * pid 1511 started.
      * pid 1512 started.
      * pid 1513 started.
      * pid 1514 started.
      * pid 1515 started.

    Press <CTRL-C> to quit.

This process remains in the foreground, so you will probably want to run it in
a [Screen](http://www.gnu.org/software/screen/) session or as an
[Upstart](http://upstart.ubuntu.com/) service.

Clients
-------

The `pigman.PigMan` class manages the Gearman client connection, job queueing,
submission, and data marshalling. All `run_` methods are asynchronous, and do
not wait for the job to complete before returning.

### Run a Job Immediately

To run a single job immediately, use the `pigman.PigMan.run_job` method. Its
arguments are the task name, along with any arguments the task accepts.

    import pigman

    p = pigman.PigMan()
    p.run_job('frob.reverse', 'Hello, world!')

### Queue Several Jobs

If you have a batch of jobs that you want to submit to the Gearman job server
in one shot, you can queue them up using `pigman.PigMan.queue_job` and then
submit them with `pigman.PigMan.run_queued`.

    import pigman

    p = pigman.PigMan()
    p.queue_job('frob.reverse', 'Hello, world!')
    p.queue_job('frob.reverse', 'Mapkin rocks!')
    p.queue_job('frob.reverse', 'Superfluous!')

    # Some time later...

    p.run_queued()
