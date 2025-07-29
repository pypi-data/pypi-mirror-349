from setuptools import setup, find_packages

setup(
    name='linkgenfx',
    version='0.1.4',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'linkgenfx = linkgenfx.app:main',
        ],
    },
    python_requires='>=3.6',
    install_requires=[],
)

