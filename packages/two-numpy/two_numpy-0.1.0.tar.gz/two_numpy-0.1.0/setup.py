from setuptools import setup

setup(
    name='two_numpy',
    version='0.1.0',
    description='A simple library for manager the numpy version to different python interpreters.',
    author='Huang Hao Hua',
    author_email='13140752715@163.com',
    url='https://github.com/Locked-chess-official/two_numpy',
    py_modules=['two_numpy'],
    install_requires=[
        'numpy',
        'packaging'
    ],
    python_requires='>=3.13',
    long_description=open('readme.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT',
)