from setuptools import setup, find_packages
import os

this_dir = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_dir, "README.md")

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="song-runner",
    version="0.1.0",
    author="Vishesh Jain",
    author_email="visheshj2005@example.com",
    description="A simple CLI tool to play YouTube songs from the terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "yt-dlp",
        "ffpyplayer",
        "youtube-search-python"
    ],
    entry_points={
        "console_scripts": [
            "song=song.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
