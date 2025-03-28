from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="real-estate-analysis",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive system for analyzing real estate markets using multiple data sources and advanced analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/real-estate-analysis",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "real-estate-analysis=real_estate_analysis.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "real_estate_analysis": ["py.typed"],
    },
    zip_safe=False,
) 