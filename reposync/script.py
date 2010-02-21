import sys
import os
import re

from reposync.backends import get_backend


def parse_options(argv):
    """Parse the given argument array, and return a 2-tuple
    (repositories, options).
    """
    return [], {}


class SyncJob(object):

    def __init__(self, repository, push_url):
        self.repository = repository
        self.push_url = push_url

    def __unicode__(self):
        return self.repository


def parse_config():
    """Parse the config file, return a list of the stuff
    we are supposed to sync (``SyncJob`` instances).

    The config file contains one sync job per line. Each line is a list
    of columns separted by whitespace.

    Currently, only two columns are expected: repository and push url.
    As an example, a line might look like this:

    /home/git/repos/reposync.git   git@github.com:miracle2k/reposync.git
    """
    config_path = None
    for path in ('.reposync.conf',
                 os.path.expanduser('~/.reposync.conf'),
                 '/etc/reposync.conf'):
        if os.path.exists(path):
            config_path = path
            break

    if not config_path:
        raise EnvironmentError("config file not found")

    result = []
    f = open(config_path, 'r');
    try:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            bits = re.split(r'\s*', line)
            if len(bits) != 2:
                raise ValueError('Invalid line in config file: %s' % line)
            result.append(SyncJob(*bits))
    finally:
        f.close()

    return result


def main():
    repositories, options = parse_options(sys.argv[1:])
    jobs = parse_config()
    for job in jobs:
        backend = get_backend(job)
        if not backend:
            raise RuntimeError('Unable to process %s: Not a repository, or '+
                               'unsupported repository type.' % job.repository)
        backend.run(job)


if __name__ == '__main__':
    sys.exit(main() or 0)