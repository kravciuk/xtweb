from .celery import app

from logging import getLogger
log = getLogger(__name__)


@app.task()
def periodic_task_backup():
    from django.core.management import execute_from_command_line
    argv = ['', 'dbbackup', '--compress', '--clean']
    execute_from_command_line(argv)


@app.task(priority=1)
def sample_task():
    log.info('Sample task executed')
    return 'Sample task executed'

