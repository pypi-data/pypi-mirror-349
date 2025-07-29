from setuptools import setup, find_packages

setup(
    name="linkgenfx",
    version="0.1.5",
    packages=find_packages(),  # It will auto-detect the 'linkgenfx' package
    install_requires=[],
    entry_points={
        'console_scripts': [
            'linkgenfx = linkgenfx.app:main',
        ],
    },
    author="EFXTv",
    description="SSH reverse tunnel CLI via serveo",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
