import os
from setuptools import setup

__currdir__ = os.getcwd()
__readme__ = os.path.join(__currdir__, 'README.md')


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name='plantpredict',
    version=get_version("plantpredict/__init__.py"),
    description='Python SDK for PlantPredict (https://ui.plantpredict.terabase.energy).',
    url='https://github.com/plantpredict/python-sdk',
    author='Kurt Rhee & Jese Milam.',
    author_email='support@plantpredic.com',
    license='LICENSE.txt',
    long_description=open(__readme__).read(),
    packages=['plantpredict'],
    python_requires='>=3.10, <4',
    install_requires=[
        'requests',
        'pandas',
        'six',
        'mock',
        'xlrd',
        'openpyxl'
    ]
)
