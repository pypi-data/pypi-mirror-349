from setuptools import setup

setup(
    name="runcx",
    version="0.1",
    packages=["runcx"],
    entry_points={
        "console_scripts": [
            "runc = runc.runc:main"
        ]
    },
    author="Cansila",
    description="Simple CLI tool to run binaries globally",
    python_requires=">=3.6",
)
