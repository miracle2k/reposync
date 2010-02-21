from os import path
import subprocess


class GitBackend(object):

    def can_handle(self, job):
        git_dir = path.join(job.repository, '.git')
        if path.exists(git_dir):
            job.__git_dir = git_dir
            return True
        return False

    def run(self, job):
        # We can't use --tags and --all in one call, so we need two:
        args=[
            'git',
            '--git-dir=%s' % job.__git_dir,
            'push',
            '--mirror',
            '--force',
            '%s' % job.push_url
            ]
        returncode = subprocess.call(args, close_fds=True)
        if returncode != 0:
            raise RuntimeError(('git returned non-zero exit code: %d, '
                                ' call was: %s') % (
                                   returncode, " ".join(args)))
