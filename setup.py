import setuptools

with open("README.md", "r") as description:
    long_description = description.read()

setuptools.setup(
    name="discogs-marketplace-scraper",
    version="0.0.1",
    author="Romanas Grigorjevas",
    author_email="romanas@grigorjevas.com",
    description="Discogs marketplace scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Intependent"
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6"
)
