from setuptools import setup, find_packages

setup(
    name="dbdev",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "dbdev=dbdev.cli:app",
        ],
    },
    install_requires=[
        "docker",
        "python-dotenv",
        "typer"
    ],
)
