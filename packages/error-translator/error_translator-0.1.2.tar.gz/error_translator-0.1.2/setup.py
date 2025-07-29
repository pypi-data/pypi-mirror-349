from setuptools import setup, find_packages

setup(
    name="error_translator",
    version="0.1.2",
    description="Translate Python errors into AI-explained suggestions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Romas Laužadis",
    author_email="rromikas@gmail.com",
    url="https://github.com/rromikas/error_translator",
    packages=find_packages(),
    install_requires=[
        "rich",
        "python-dotenv",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
