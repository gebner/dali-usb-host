#!/usr/bin/env python

from distutils.core import setup

setup(name='dali-usb',
      version='0.1',
      description='Host utilities for the DALI-USB interface',
      author='Gabriel Ebner',
      author_email='gebner@2b7e.org',
      url='http://2b7e.org/',
      packages=['daliusb'],
      scripts=['dali','dali-indicator'],
      requires=['pyusb'],
      data_files=[('share/icons/ubuntu-mono-dark/apps/22', ['dali-usb.svg']),
		 ],
     )
