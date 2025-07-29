from setuptools import setup, find_packages

setup(
    name="catbench",
    version='0.1.31',
    author="JinukMoon",
    author_email="jumoon@snu.ac.kr",
    packages=find_packages(),
    description="CatBench: Benchmark Framework of Machine Learning Interatomic Potentials for Adsorption Energy Predictions in Heterogeneous Catalysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JinukMoon/catbench",
    license="MIT",
    install_requires=[
        "ase>=3.22.1",
        "xlsxwriter>=3.2.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="MLIP benchmark for catalysis",
    python_requires=">=3.8",
)