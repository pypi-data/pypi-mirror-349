from setuptools import setup, find_packages

setup(
    name='cpu-scheduling-tk09',
    version='0.1.0',
    packages=find_packages(),
    description='CPU Scheduling Algorithms: FCFS, SJF, SRTF, Round Robin, Priority',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='you@example.com',
    url='https://github.com/yourusername/cpu-scheduling-tk09',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
