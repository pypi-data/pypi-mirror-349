from setuptools import setup, find_packages

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Helper to read requirements.txt
def get_requirements(file_path: str) -> list[str]:
    with open(file_path, "r") as file_obj:
        requirements = [line.strip() for line in file_obj if line.strip() and line.strip() != "-e ."]
    return requirements

# Metadata
__version__ = "0.1.0"
REPO_NAME = "GunSan-Strength-Index"
AUTHOR_USER_NAME = "santosh3110"
SRC_REPO = "gunsan_strength"
AUTHOR_EMAIL = "santoshkumarguntupalli@gmail.com"
LIST_OF_REQUIREMENTS = get_requirements("requirements.txt")

# Setup
setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="GunSan Strength Index (GSI) – A proprietary leading and lagging indicator for measuring technical strength of a scrip.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=LIST_OF_REQUIREMENTS,
    classifiers=[
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ],

    python_requires=">=3.7",
    include_package_data=True,
)
