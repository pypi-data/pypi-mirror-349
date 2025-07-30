from setuptools import setup, find_packages

setup(
    name="sprite-sheet-animation",  # This is the name users will use with pip
    version="0.1.0",
    author="Jack Bennett",
    description="A simple Pygame-based sprite sheet animation class.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TheChainsawBoy/AnimationLibrary",  # Optional, if you have GitHub
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
    ],
    python_requires='>=3.6',
)
