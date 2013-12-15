from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '0.1'

install_requires = [
    # List of project dependencies
]


setup(name='Unifac',
    version=version,
    description="Implementation of UNIFAC model for Vapor-Liquid equilibrium",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      "Development Status :: 2 - Pre-Alpha",
      "Intended Audience :: Science/Research",
      "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
      "Programming Language :: Python :: 3",
      "Topic :: Scientific/Engineering :: Chemistry"
    ],
    keywords='',
    author='Jacek Przemieniecki',
    author_email='unifac@przemieniecki.net',
    url='unifac.przemieniecki.net',
    license='EUPL',
    packages=find_packages('unifac'),
    package_dir = {'': 'unifac'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['Unifac=unifac:main']
    }
)
