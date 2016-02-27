#!/usr/bin/env python

from setuptools import setup

# Make sure that python 2.7 and FFMPEG are installed
setup(name='youtube-song-downloader',
      version='0.3',
      description='A program used to search and download songs from Youtube.',
      url='https://github.com/dszopa/youtube-song-downloader',
      author='Daniel Szopa',
      author_email='dszopa@iastate.edu',
      license='MIT',
      install_requires=[
          'youtube_dl',
          'google-api-python-client',
          'pytest',
      ],
      packages=['ytsdl'],
      package_dir={'youtube-song-downloader': 'ytsdl'},
      entry_points={
        'console_scripts': [
          'youtube-song-downloader = ytsdl.cli:main',
        ],
      },
      include_package_data=True,
      zip_safe=False)
