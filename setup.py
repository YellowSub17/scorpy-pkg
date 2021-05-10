import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scorpy-pkg-YellowSub17",
    version="0.0.1",
    author="Patrick Adams",
    author_email="s3826109@student.rmit.edu.au",
    description="Scattering Correlation for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YellowSub17/scorpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

    ],
    python_requires='>=3.6',
)
