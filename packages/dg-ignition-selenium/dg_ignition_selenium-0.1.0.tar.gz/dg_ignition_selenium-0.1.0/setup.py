from setuptools import setup, find_packages

setup(
    name="dg-ignition-selenium",
    version="0.1.0",
    packages=find_packages(
        include=["ignition-automation-tools", "ignition-automation-tools.*"]
    ),
    install_requires=[
        "selenium>=4.0.0",
    ],
    python_requires=">=3.8",
)
