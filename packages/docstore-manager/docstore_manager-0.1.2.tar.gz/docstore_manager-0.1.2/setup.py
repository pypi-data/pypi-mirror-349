from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="docstore-manager",
    version="0.1.2",
    description="Command-line tools for managing document stores like Qdrant and Solr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Allen Day",
    author_email="allenday@example.com",  # Replace with correct email
    url="https://github.com/allenday/docstore-manager",
    packages=find_packages(),
    install_requires=[
        "qdrant-client>=1.7.0",
        "tqdm>=4.66.0",
        "pyyaml>=6.0",
        "appdirs>=1.4.4",
        "pysolr>=3.9.0",
    ],
    entry_points={
        "console_scripts": [
            "docstore-manager=docstore_manager.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
