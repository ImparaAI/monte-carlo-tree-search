import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imparaai-montecarlo",
    version="1.2.0",
    license='MIT',
    author="ImparaAI",
    author_email="author@example.com",
    description="Library for running a Monte Carlo tree search either traditionally or with expert policies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ImparaAI/monte-carlo-tree-search",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)