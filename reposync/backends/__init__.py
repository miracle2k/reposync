from reposync.backends.git import GitBackend

BACKENDS = [
    GitBackend()
]


def get_backend(job):
    """Return a backend that can handle the repository type of ``job``,
    or ``None`` if no fitting backend is available.
    """
    for backend in BACKENDS:
        if backend.can_handle(job):
            return backend