from setuptools import setup

setup(
    name="ndtiler",
    version="0.1.0",
    description="Lightweight package for iterative tiling over N-dimensional arrays",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ryan 'RyanIRL' Peters",
    author_email="RyanIRL@icloud.com",
    url="https://github.com/ryanirl/ndtiler",
    py_modules=["ndtiler"],  # Single file
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    keywords="array, tiling, numpy, image processing, deep learning",
    project_urls={
        "Bug Reports": "https://github.com/ryanirl/ndtiler/issues",
        "Source": "https://github.com/ryanirl/ndtiler",
    },
)