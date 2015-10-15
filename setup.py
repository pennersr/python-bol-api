from setuptools import setup, find_packages

VERSION = '0.2.0'

setup(name='python-bol-api',
      version=VERSION,
      description="Wrapper for the bol.com API",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Topic :: System',
          'Topic :: System :: Software Distribution',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
      ],
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
