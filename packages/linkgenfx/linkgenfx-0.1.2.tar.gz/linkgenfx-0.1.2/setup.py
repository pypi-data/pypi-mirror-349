from setuptools import setup, find_packages

setup(
    name="linkgenfx",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "linkgen = linkgen.app:main",
        ],
    },
    python_requires='>=3.6',
)

