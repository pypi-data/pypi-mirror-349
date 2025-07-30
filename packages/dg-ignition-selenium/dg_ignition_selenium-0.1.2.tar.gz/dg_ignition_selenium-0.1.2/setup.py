from setuptools import setup, find_packages

setup(
    name="dg-ignition-selenium",
    version="0.1.2",
    packages=find_packages(
        where="src",
        include=["ignition_automation_tools", "ignition_automation_tools.*"],
    ),
    package_dir={"": "src"},
    install_requires=[
        "selenium>=4.0.0",
    ],
    python_requires=">=3.8",
)
