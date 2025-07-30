import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vscodedebugvisualizer",
    version="v0.2.1",
    author="Franz Ehrlich",
    author_email="fehrlichd@gmail.com",
    description="vscode-debug-visualizer extension for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fehrlich/vscode-debug-visualizer-py",
    packages=setuptools.find_packages(exclude=["tests", "example"]),
    test_suite="tests",
    install_requires=["numpy", "plotly"],
    tests_require=["pytest"],
    include_package_data=True,
    # package_data={"phases": ["generate-template/*", "generate-template/**/*", "static-template/*", "static-template/**/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
