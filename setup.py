import os
from setuptools import setup

__currdir__ = os.getcwd()
__readme__ = os.path.join(__currdir__, 'README.md')

version = '1.0.11'

if __name__ == '__main__':
    setup(
        name='plantpredict',
        version=version,
        description='Python SDK for PlantPredict (https://ui.plantpredict.terabase.energy).',
        url='https://github.com/plantpredict/python-sdk',
        author='Kurt Rhee, previously Stephen Kaplan',
        author_email='krhee@terabase.energy',
        license='LICENSE.txt',
        long_description=open(__readme__).read(),
        packages=['plantpredict'],
        python_requires='>=3.5, <4',
        install_requires=[
            'requests',
            'pandas',
            'six',
            'mock',
            'xlrd',
            'openpyxl'
        ]
    )
