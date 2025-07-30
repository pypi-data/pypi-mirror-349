from setuptools import setup, find_packages

setup(
    name="colerminal",
    version="0.1.1",
    license="MIT",
    description="A simple color printing libary. Read README.md for usage.",
    author="Amaan Syed",
    author_email="amaancal3@gmail.com",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)