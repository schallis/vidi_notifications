from setuptools import setup, find_packages

setup(
    name="vidi-notifications",
    version='2.1.1.dev0',
    packages=find_packages('src', exclude=('tests',)),
    package_dir={'': 'src'},
    include_package_data=True,
    license='proprietary',
    url='http://zonza.tv',
    description="A Django application for handling Vidispine callbacks and "
                "raising signals",
    author='Hogarth Worldwide',
    author_email='tsd@hogarthww.com',
    zip_safe=True,
    install_requires=[
        'django>=1.5.5, <1.7.0',
        'celery==3.1.12',
        'django-celery==3.1.10',
        'hwwutils==0.0.2',
    ],
)
