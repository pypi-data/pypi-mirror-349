from setuptools import setup, find_packages

setup(
    name="rohith",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "questionary",
        "rich",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "rohith=rohith.cli:main"
        ]
    },
    author="Rohit Gowda R",
    description="A terminal-based CLI card to showcase Rohit Gowda's profile and quick contact tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rohithgowdax/cli-card",  # Optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
