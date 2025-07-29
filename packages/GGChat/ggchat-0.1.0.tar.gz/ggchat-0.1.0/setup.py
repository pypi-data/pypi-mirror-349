
from setuptools import setup, find_packages

setup(
    name="GGChat",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Твоё имя",
    author_email="oubstudios@gmail.com",
    description="Графический LLM-чат на Tkinter от OUBStudios.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
