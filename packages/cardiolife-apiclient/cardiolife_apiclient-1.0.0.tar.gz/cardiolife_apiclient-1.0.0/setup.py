from setuptools import setup, find_packages
import os
import re

def read_version():
    with open(os.path.join("cardiolife_apiclient", "__init__.py")) as f:
        content = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", content, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='cardiolife-apiclient',  # Hífen aqui é o padrão para PyPI
    version=read_version(),
    description='Python client for the Cardiolife ECG API Server',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andre Costa',
    author_email='ac@cardiolife.global',
    url='https://cardiolife.global',  # opcional, mas bom ter
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'numpy>=1.21.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
