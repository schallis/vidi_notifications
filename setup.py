from setuptools import setup
import os

execfile("vidi_notifications/version.py"),


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name="vidi_notifications",
    version=__version__,
    url='http://zonza.tv',
    license='Proprietary',
    description="A Django application for handling Vidispine callbacks and "
                "raising signals",
    author='Hogarth Worldwide',
    author_email='tsd@hogarthww.com',
    packages=get_packages('vidi_notifications'),
    zip_safe=False,
    install_requires=[
        'Django==1.5.5',
        'ZonzaRest==0.3.3',
        'hwwutils==0.0.2',
        'hacked-urlobject==0.5.3',
        'mock==1.0.1',
    ],
    dependency_links=['http://pypi-zadar.hogarthww.prv/hogarthww/prod/'],
)
