from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    description = fh.read()

setup(
    name='debugonce',
    version='0.5.1',
    author='Sujith Joseph',
    author_email='nsjr2002@gmail.com',
    url='https://github.com/Sujith-sunny/debugonce',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'psutil',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    long_description=description,
    long_description_content_type='text/markdown',
    keywords='debugging, bug reproduction, python, decorator, cli, logging',
    entry_points={
        'console_scripts': [
            'debugonce=debugonce_packages.cli:cli',
        ],
    },
)


#python3 setup.py sdist bdist_wheel
#pip install dist/debugonce-0.*.0-py3-none-any.whl
#twine upload dist/*