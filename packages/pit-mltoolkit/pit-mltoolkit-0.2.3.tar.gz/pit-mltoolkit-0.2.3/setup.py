# setup.py
from setuptools import setup, find_packages
from pathlib import Path

# read requirements.txt, ignore blank lines and comments
base_dir = Path(__file__).parent
reqs = base_dir.joinpath("requirements.txt").read_text().splitlines()
install_requires = [r for r in reqs if r and not r.strip().startswith("#")]

setup(
    name="pit-mltoolkit",
    version="0.2.3",  # bump on each release
    author="PepkorIT MLE",
    author_email="neilslab@pepkorit.com",
    description="Tools and functions for machine learning engineering and data science",
    long_description=(base_dir / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pit-mle/mltoolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
