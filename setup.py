from setuptools import setup
from setuptools import find_packages

setup(
    name="krixik",
    version="1.1.14",
    description="Easily assemble and serverlessly consume modular AI pipelines through secure Python APIs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jeremy Watt",
    email="jeremy@krixik.com",
    url="https://github.com/krixik-ai/krixik-cli",
    packages=find_packages(include=["krixik*"]),
    python_requires=">=3.8",
    install_requires=[
        "boto3",
        "ffmpeg-python",
        "moviepy",
        "nltk",
        "numpy",
        "pillow",
        "pyaml",
        "pydub",
        "pypdf",
        "pytest",
        "pytest-subtests",
        "python-docx",
        "python-dotenv",
        "python-pptx",
        "requests",
    ],
    extras_require={
        "linting": [
            "ruff",
        ],
        "testing": [
            "pytest",
            "pytest-xdist",
        ],
    },
)