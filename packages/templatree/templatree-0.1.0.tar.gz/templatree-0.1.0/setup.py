from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="templatree",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "templatree = templatree.cli:main",
        ],
    },
    package_data={
        "templatree": ["templates/**/*"],
    },
    author="Önder Ertan",
    author_email="onderertan@protonmail.com",
    license="MIT",
    description="Templatree directory and file structure with predefined templates.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.6",
)
