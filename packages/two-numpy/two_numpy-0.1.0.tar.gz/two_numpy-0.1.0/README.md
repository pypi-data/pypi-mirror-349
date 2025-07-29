# Two numpy


This is the module that ensure that you import the right version of numpy.

In python3.13, there are two python interpreters, different interpreters have different numpy versions.

This module will help you to import the right version of numpy.



## Install

```bash
pip install two_numpy
```

## Usage

It will import the right version of numpy based on the python interpreter you are using.

```python
from two_numpy import np
```

You can also use it like this:

```python
import two_numpy
two_numpy.np
```

You can also set the version of numpy you want to use:

```python
import os
os.environ["NUMPY_VERSION"] = "2.2.0"
from two_numpy import np
```

Tips: can only set the official version of numpy, such as "2.2.0", "2.2.1" and so on.

Don't set the other version of numpy, such as "2.2.0.dev0", "2.2.0rc1" and so on.

## License

MIT
