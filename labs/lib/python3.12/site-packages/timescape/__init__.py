__all__ = []


def _everything(*args, **kwargs):
    raise NotImplementedError('''This is not the timescape package you are looking for.

Do not blindly install packages from PyPI. Ask for instructions from whomever asked you to install this.

I have registered this project to prevent name-squatting by a bad actor, and all names will raise this error.''')


def __getattr__(name):
    return _everything
