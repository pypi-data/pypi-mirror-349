from setuptools import find_packages, setup

setup(
    name="clipkly",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "tqdm", "openpyxl"],
    entry_points={
        "console_scripts": [
            "clipkly=clipkly.cli:main"
        ]
    },
    author="Julian Dario Luna Patiño",
    author_email="judlup@trycatch.tv",
    description="Corta automáticamente clips de video a partir de subtítulos o timecodes definidos en un JSON.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/judlup/clipkly",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
