from os import path
import subprocess


class GitBackend(object):

    def can_handle(self, job):
        """This is adapted based on the detection code in git/setup.c
        """
        for possibility in ('', '.git'):
            possible_git_dir = path.join(job.repository, possibility)
            for requirement in ('objects', 'refs', 'HEAD'):
                if not path.exists(path.join(possible_git_dir, requirement)):
                    break
            else:
                job.__git_dir = possible_git_dir
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
