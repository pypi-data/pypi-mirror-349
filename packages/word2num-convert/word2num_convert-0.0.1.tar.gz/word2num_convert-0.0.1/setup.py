from setuptools import setup, find_packages

setup(
    name="word2num_convert",
    version="0.0.1",
    author="Chandan Singh",
    author_email="chandan21082000@gmail.com",
    description="Convert words to numbers in English, Hindi, and Marathi",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/singhchandann/word2num_converter",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: Hindi",
        "Natural Language :: Marathi",
        "Natural Language :: English",
    ],
    python_requires='>=3.6',
)
