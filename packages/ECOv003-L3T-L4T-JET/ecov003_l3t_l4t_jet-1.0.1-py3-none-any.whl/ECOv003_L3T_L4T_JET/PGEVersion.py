from os.path import join, abspath, dirname

with open(join(abspath(dirname(__file__)), 'version.txt')) as f:
    PGEVersion = f.read().strip()
