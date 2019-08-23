#!/usr/bin/env python

from setuptools import setup


setup(name='c3cloudsis-client',
      version='1.0',
      description='Client to the Semantic mapper of C3-Cloud',
      author='Mikael Dusenne',
      author_email='mikaeldusenne@gmail.com',
      url='',
      packages=[ 'c3_cloud_client' ],
      install_requires=[
                        'requests',
                        'pandas',
                        'xlrd',
                        'schema',
                        'jsonpickle',
                        'pyyaml'
                        
      ],
     )
