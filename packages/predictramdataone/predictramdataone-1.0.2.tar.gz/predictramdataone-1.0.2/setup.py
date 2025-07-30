from setuptools import setup, find_packages

setup(
    name="predictramdataone",
    version="1.0.2",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'predictramdataone': ['data/*.json'],
    },
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="API for accessing PredictRam stock data",
    long_description="A Python package for accessing PredictRam stock data through API calls",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/predictramdataone",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)