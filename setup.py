from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='dynamic_threadlocal',
      version=version,
      description="Dynamic scoping using thread-local scoping",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jonathan Gardner',
      author_email='jgardner@jonathangardner.net',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
