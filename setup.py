from setuptools import setup, find_packages

VERSION = '0.1'

setup(name='python-bol-api',
      version=VERSION,
      description="Wrapper for the bol.com API",
      classifiers=[],
      keywords='bol bol.com api wrapper',
      author='Raymond Penners',
      author_email='raymond.penners@intenct.nl',
      url='http://www.intenct.info/',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['python-dateutil',
                        'requests'],
      entry_points="")
