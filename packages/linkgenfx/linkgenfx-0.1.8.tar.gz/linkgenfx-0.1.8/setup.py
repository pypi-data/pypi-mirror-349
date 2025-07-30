from setuptools import setup, find_packages
import os

# Read README.md safely
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="linkgenfx",
    version="0.1.8",  # Increment this on every upload
    author="EFXTv",
    description="CLI tool to create SSH reverse tunnel via serveo.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/efxtv/linkgenfx",  # Replace with actual repo if public
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'linkgenfx = linkgenfx.app:main',
        ],
    },
    include_package_data=True,
)

