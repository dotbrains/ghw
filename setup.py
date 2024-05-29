from setuptools import setup, find_packages

setup(
    name="ghw",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "ghw=ghw:main",
        ],
    },
    install_requires=[],
    test_suite="tests",
)
