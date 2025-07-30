from setuptools import setup, find_packages

setup(
    name='aptamer',
    version='0.1.0',
    description='Evolve DNA aptamers using RNA folding energy',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'viennarna',
        'pytest',
    ],
    python_requires='>=3.7',
)
