from setuptools import setup, find_packages

setup(
    name='time-tracker-cli-keerthana',
    version='0.1.0',
    author='Keerthana P S',
    author_email='keerthanaps.work@gmail.com',
    description='A simple CLI tool to track tasks and time logs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/time-tracker-cli',  # optional
    packages=find_packages(),
    install_requires=[
        'rich',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'time-tracker = time_tracker.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)
