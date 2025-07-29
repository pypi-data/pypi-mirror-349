from docutils.nodes import description
from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='tcqi',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'numpy>=2.2.0',
        'pandas>=2.2.3',
        'plotly>=6.1.0'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)