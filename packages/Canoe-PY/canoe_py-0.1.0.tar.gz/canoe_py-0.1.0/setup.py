from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Canoe_PY",
    version="0.1.0",
    author="Subhashsingh Rajpurohit",
    author_email="rajpurohits001@example.com",
    description="A custom library for interacting with Vector CANoe",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Canoe_PY",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/Canoe_PY/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Testing",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "pywin32",
    ],
)

