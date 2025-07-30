from setuptools import setup, find_packages

setup(
    name='dapcy',
    version='1.3.0',
    author='Alejandro Correa Rojo',
    author_email='alejandro.correarojo@uhasselt.be',
    description='A sklearn implementation of DAPC for population genetics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/uhasselt-bioinfo/dapcy',  # Update with your repo URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
        'matplotlib',
        'joblib',
        'sgkit',
        'pandas',
        'seaborn',
        'bio2zarr',
    ],
)