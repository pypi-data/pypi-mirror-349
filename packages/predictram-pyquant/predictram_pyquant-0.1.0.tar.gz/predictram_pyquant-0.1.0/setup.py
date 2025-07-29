from setuptools import setup, find_packages

setup(
    name="predictram-pyquant",
    version="0.1.0",
    description="Stock data querying and visualization API",
    author="Your Name",
    author_email="you@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "matplotlib",
        "openpyxl"
    ],
    package_data={
        "predictram_pyquant": ["data/*.json"]
    },
    entry_points={
        "console_scripts": [
            "predictram=predictram_pyquant.core:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
