from setuptools import setup, find_packages

setup(
    name="mypuma",  # Your library name
    version="0.0.0",  # Version number
    author="puma",
    author_email="puma.info@gmail.com",
    description="A helper library with useful functions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/myhelper",  # GitHub URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
