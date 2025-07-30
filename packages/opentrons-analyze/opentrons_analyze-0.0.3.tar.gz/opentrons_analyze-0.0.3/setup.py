from setuptools import setup, find_packages
setup(
   name='opentrons_analyze',
   version='0.0.3',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      opentrons_analyze = analyze:analyze
      ''',
)