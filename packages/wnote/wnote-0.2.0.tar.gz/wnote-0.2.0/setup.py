from setuptools import setup, find_packages

setup(
    name="wnote",
    version="0.2.0",
    description="Terminal Note Taking Application with beautiful UI",
    author="WNote Team",
    py_modules=["wnote", "wnote_sync", "__init__"],
    install_requires=[
        "click>=8.1.7",
        "rich>=13.7.0",
        "requests>=2.28.0",
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "wnote=wnote:cli",
        ],
    },
    python_requires=">=3.7",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
) 