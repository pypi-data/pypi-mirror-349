from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Py2ExeLite",
    version="1.0.0",
    author="Poyraz (PozStudio)",
    author_email="pozstudio.dev@gmail.com",
    description="Lightweight tool to convert Python scripts into .exe files with style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PozStudio/Py2ExeLite",
    project_urls={
        "Bug Tracker": "https://github.com/PozStudio/Py2ExeLite/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "py2exelite=py2exelite.__main__:main"
        ]
    },
)
