from setuptools import setup, find_packages

setup(
    name="ensure-json",
    version="0.1.1",
    description="A <3kB, dependency-free toolkit to repair 'almost-JSON' text from LLMs and return a valid Python object—or raise JsonFixError.",
    author="",
    license="MIT",
    packages=find_packages(),
    py_modules=["ensure_json", "cli"],
    install_requires=[],
    extras_require={
        "schema": ["pydantic>=1.10.0"]
    },
    entry_points={
        "console_scripts": [
            "ensure-json = cli:main"
        ]
    },
    python_requires=">=3.7",
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
