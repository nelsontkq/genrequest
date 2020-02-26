import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genrequest", # Replace with your own username
    version="1.0.0",
    author="Nelson Truran",
    author_email="nelson@truran.dev",
    description="A package for generating fake requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nelsontkq/genrequest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
