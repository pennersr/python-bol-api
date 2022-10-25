from setuptools import setup, find_packages

install_requires = [
    "python-dateutil",
    "requests",
]

setup(
    name="python-bol-api",
    version="0.9.1",
    description="Wrapper for the bol.com API",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: System",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    keywords="bol bol.com api wrapper",
    author="Raymond Penners",
    author_email="raymond.penners@intenct.nl",
    url="http://www.intenct.info/",
    license="",
    packages=find_packages(include=["bol"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points="",
)
