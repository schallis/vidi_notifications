from setuptools import setup

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
    author='Hogarth',
    author_email='steven.challis@hogarthww.com',
    packages=get_packages('vidi_notifications'),
    zip_safe=False,
    install_requires=[
        'Django>=1.4.3',
        'ZonzaRest>=0.1.1',
        'hwwutils>=0.0.1',
    ],
    dependency_links=['http://dev-jen1/pypi/'],
)
