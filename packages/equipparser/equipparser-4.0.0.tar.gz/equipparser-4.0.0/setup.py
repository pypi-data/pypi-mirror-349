from distutils.core import setup
import os

NAME = 'equipparser'
HUMAN_NAME = 'equipparser'
HERE = os.path.abspath(os.path.dirname(__file__))
version_ns = {}
with open(os.path.join(HERE, 'irs_reader', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup(name=HUMAN_NAME,
      description = "XML Parser",
      version = '4.0.0',
      author = 'Vishal Avalani',
      author_email = 'vishal.avalani@gmail.com',
      url = 'https://github.com/vishalavalani/990-xml-reader',
      license = 'MIT',
      setup_requires = ["setuptools", ],
      install_requires = ['requests', 'xmltodict', 'unicodecsv'],
      tests_require = ['nose', 'requests', 'xmltodict', 'unicodecsv', 'tox', 'tox-pyenv',],
      packages = ['equipparser'],
      package_dir = {'equipparser': 'irs_reader'},
      package_data = {'equipparser': ['metadata/*.csv']},
      keywords = ['XML'],
      entry_points = {
          "console_scripts": ["equipparser=equipparser.irsx_cli:main",
                              "irsx_index=equipparser.irsx_index_cli:main",
                              "irsx_retrieve=equipparser.irsx_retrieve_cli:main"]
      },
      classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
        ],
      )
