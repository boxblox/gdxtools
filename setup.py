import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gdxtools",
    version="0.1.72",
    author="Adam Christensen",
    author_email="adam.christensen@gmail.com",
    description="A helper package to read and write GAMS GDX files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boxblox/gdxtools",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['gams'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
