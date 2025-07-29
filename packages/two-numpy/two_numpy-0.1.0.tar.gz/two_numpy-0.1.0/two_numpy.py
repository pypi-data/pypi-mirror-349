"""
This script checks if the numpy package is installed and if its version matches the one specified 
in the environment variable NUMPY_VERSION.
In python 3.13, there are two python interpreters: python.exe and python3.13t.exe. 
Different interpreters have different numpy versions to installed and import. 
This script is used to ensure that the correct numpy version is used in the correct interpreter.
If set the environment variable NUMPY_VERSION, it will check the version of numpy.
If the numpy hasn't been installed, it will install the numpy package.
If the numpy is not suitable for the current interpreter, it will reinstall the numpy package.

Note: please set the official wersion as the environment variable NUMPY_VERSION.
For example: 2.2.0, 2.2.1, etc.
Don't set the version like 2.2.0rc1, 2.2.0dev0, 2.2.0beta, etc.
"""

import os
import sys
import subprocess
from importlib.metadata import version
from packaging.version import parse

def is_valid_version(version_str):
    try:
        parsed = parse(version_str)
        return not parsed.is_prerelease and not parsed.is_devrelease
    except:
        return False


if 'NUMPY_VERSION' not in os.environ:
    version_information = ''
else:
    if not is_valid_version(os.environ['NUMPY_VERSION']):
        raise ValueError('''Wrong version information: 'NUMPY_VERSION' must be the official version.
                         For example: 2.2.0, 2.2.1, etc.
                         Don't set the version like 2.2.0rc1, 2.2.0dev0, 2.2.0beta, etc.''')
    version_information = '=='+os.environ['NUMPY_VERSION']

def get_version():
    try:
        return version("numpy")
    except Exception:
        return ''

def setup_np():
    setup_numpy = subprocess.Popen([
        sys.executable,
        '-m',
        'pip',
        'install',
        '--force-reinstall',
        f'numpy{version_information}'
        ], stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    _, stderr = setup_numpy.communicate()
    return (setup_numpy.returncode, stderr)

if not get_version():
    if (result := setup_np())[0] != 0:
        raise ImportError(f"cannot setup numpy: \n{result[1]}")
    import numpy as np

elif version_information and version_information != get_version():
    if (result := setup_np())[0] != 0:
        raise ImportError(f"cannot setup numpy: \n{result[1]}")
    import numpy as np
else:
    try:
        import numpy as np
    except Exception:
        if (result := setup_np())[0] != 0:
            raise ImportError(f"cannot setup numpy: \n{result[1]}") from None
        import numpy as np
