from os import path

from setuptools import setup, find_packages


setup(
    name='alembic-vis',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    long_description=open(path.join(path.dirname(__file__), 'README.md')).read(),
    install_requires=['graphviz'],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'alembic_vis = alembic_vis.main:run',
        ],
    },
)
