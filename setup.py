"""tensorflow/datasets is a library of datasets ready to use with TensorFlow.

tensorflow/datasets is a library of public datasets ready to use with
TensorFlow. Each dataset definition contains the logic necessary to download and
prepare the dataset, as well as to read it into a model using the
`tf.data.Dataset` API.

Usage outside of TensorFlow is also supported.

See the README on GitHub for further documentation.
"""

import datetime
import os
import sys

from setuptools import find_packages
from setuptools import setup

nightly = False
if '--nightly' in sys.argv:
  nightly = True
  sys.argv.remove('--nightly')

project_name = 'tensorflow-datasets'
version = '0.0.2'
if nightly:
  project_name = 'tfds-nightly'
  datestring = datetime.datetime.now().strftime('%Y%m%d%H%M')
  version = '%s-dev%s' % (version, datestring)

DOCLINES = __doc__.split('\n')

REQUIRED_PKGS = [
    'absl-py',
    'future',
    'promise',
    'protobuf>=3.6.1',
    'pydub',  # actual use requires ffmpeg
    'pytz',
    'requests',
    'scipy',
    'six',
    'tensorflow-metadata',
    'termcolor',
    'tqdm',
    'wrapt',
]

TESTS_REQUIRE = [
    'jupyter',
    'pytest',
]

if sys.version_info.major == 3:
  # Packages only for Python 3
  pass
else:
  # Packages only for Python 2
  TESTS_REQUIRE.append('mock')
  REQUIRED_PKGS.append('functools32')
  REQUIRED_PKGS.append('futures')  # concurrent.futures

if sys.version_info < (3, 4):
  # enum introduced in Python 3.4
  REQUIRED_PKGS.append('enum34')

# DatasetInfo and Metadata files - everything under the
# dataset_info directory.
DATASET_INFO_AND_METADATA_FILES = [
    os.path.join(dirpath, filename)[len('tensorflow_datasets/'):]
    for dirpath, _, files in os.walk('tensorflow_datasets/dataset_info/')
    for filename in files
] + [  # Static files needed by datasets.
    'image/imagenet2012_labels.txt',
    'image/imagenet2012_validation_labels.txt',
]

DATASET_EXTRAS = {
    'librispeech': ['pydub'],  # and ffmpeg installed
}

all_dataset_extras = []
for deps in DATASET_EXTRAS.values():
  all_dataset_extras.extend(deps)

EXTRAS_REQUIRE = {
    'tensorflow': ['tf-nightly>=1.12.0.dev20181008'],
    'tensorflow_gpu': ['tf-nightly-gpu>=1.12.0.dev20181008'],
    'tests': TESTS_REQUIRE + all_dataset_extras,
}
EXTRAS_REQUIRE.update(DATASET_EXTRAS)

setup(
    name=project_name,
    version=version,
    description=DOCLINES[0],
    long_description='\n'.join(DOCLINES[2:]),
    author='Google Inc.',
    author_email='packages@tensorflow.org',
    url='http://github.com/tensorflow/datasets',
    download_url='https://github.com/tensorflow/datasets/tags',
    license='Apache 2.0',
    packages=find_packages(),
    package_data={
        'tensorflow_datasets': DATASET_INFO_AND_METADATA_FILES,
    },
    scripts=[],
    install_requires=REQUIRED_PKGS,
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='tensorflow machine learning datasets',
)
