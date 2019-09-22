#!/usr/bin/env python
"""
Forked from https://gist.github.com/810399
"""
from __future__ import with_statement, print_function
import os
import re
import shutil
import subprocess
import sys
import tempfile

# don't fill in both of these
ignore_codes = []
select_codes = []
# Add things like "--max-line-length=120" below
overrides = ["--max-line-length=120"]


def system(*args, **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    out, err = proc.communicate()
    return out


def main():
    print("Checking format of python files before commit.")
    modified = re.compile(r'^[AM]+\s+(?P<name>.*\.py$)', re.MULTILINE)
    files = system('git', 'status', '--porcelain').decode("utf-8")
    files = modified.findall(files)

    tempdir = tempfile.mkdtemp()
    for name in files:
        filename = os.path.join(tempdir, name)
        filepath = os.path.dirname(filename)

        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(filename, 'w') as f:
            system('git', 'show', ':' + name, stdout=f)

    args = ['pycodestyle']
    if select_codes and ignore_codes:
        print(u'Error: select and ignore codes are mutually exclusive')
        sys.exit(1)
    elif select_codes:
        args.extend(('--select', ','.join(select_codes)))
    elif ignore_codes:
        args.extend(('--ignore', ','.join(ignore_codes)))
    args.extend(overrides)
    args.append('.')
    output = system(*args, cwd=tempdir)
    shutil.rmtree(tempdir)
    if output:
        print(u'PEP8 style violations have been detected.  Please fix them\n'
              'by following the guide at "github.com/google/yapf".\n')
        print(output.decode("utf-8"), )
        sys.exit(1)


if __name__ == '__main__':
    main()