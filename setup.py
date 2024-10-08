import os
import setuptools

__authors__ = 'Damian Guenzing \n Dayne Y. Sasaki \n Zoey Tumbleson'


__version__ = None
with open(os.path.join('BL7011', '_version.py'), 'r') as version_file:
    lines = version_file.readlines()
    for line in lines:
        line = line[:-1]
        if line.startswith('__version__'):
            key, vers = [w.strip() for w in line.split('=')]
            __version__ = vers.replace("'", "").replace('"', "").strip()


setuptools.setup(
    name='BL7011',
    packages=setuptools.find_packages(""),
    version=__version__,
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='package for analysis of experimental xray absorption spectroscopy data',
    author=__authors__,
    url='https://github.com/ALS-Scattering/BL7011',
    keywords=['xray scattering'],
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'matplotlib',
        'tqdm',
        'scikit-learn'],
    classifiers=[
        'Development Status :: 4 - Beta',  # Chose either "3 - Alpha", "4 - Beta" or "5 -
                                           # Production/Stable" as the current state
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.7',])
