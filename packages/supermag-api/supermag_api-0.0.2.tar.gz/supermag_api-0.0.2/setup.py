from setuptools import setup, find_packages

setup(
    name='supermag_api',
    version='0.0.2',
    description='Python software to fetch SuperMag data',
    author='Sandy Antunes',
    author_email='sandy.antunes@jhuapl.edu',
    url='https://github.com/elwinter/supermag_api',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'certifi',
        'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD 3-Clause',
        'Programming Language :: Python :: 3',
    ],
)
