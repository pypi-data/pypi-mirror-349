from setuptools import setup, find_packages

setup(
    name='tcqi',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=2.2.0',
        'pandas>=2.2.3',
        'plotly>=6.1.0'
    ]
)