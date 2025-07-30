from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "DESCRIPTION.md").read_text()

setup(
    name='pipebio',
    version='2.0.0',
    description='A PipeBio client package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pipebio/python-library',
    author='PipeBio',
    author_email='support@pipebio.com',
    license='BSD 3-clause',
    packages=[
        'pipebio',
        'pipebio.models'
    ],
    install_requires=[
        "requests==2.32.2",
        "urllib3==2.4.0",
        'pandas~=2.2.2',
        'setuptools~=80.7.1',
        'biopython~=1.78',
        'python-dotenv~=1.1.0',
        'requests-toolbelt~=1.0.0',
        'openpyxl~=3.1.5',
        'pyarrow~=17.0.0',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
)
