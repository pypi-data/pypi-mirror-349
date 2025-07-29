from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fastapi-ratelimit-middleware",
    version="0.1.0",
    author="Shahzaiby",
    author_email="shahzaibshah0028@gmail.com",
    description="Rate limiting middleware for FastAPI applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zaibe_.x/fastapi-rate-limit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "fastapi>=0.68.0",
        "redis>=4.0.0",
        "pydantic>=1.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.15.0",
            "pytest-cov>=2.12.0",
            "pytest-mock>=3.6.0",
            "black>=21.5b2",
            "isort>=5.9.0",
            "mypy>=0.910",
        ],
    },
)
# This setup.py file is for a FastAPI Rate Limit package. It includes metadata about the package, such as its name, version, author, and description. It also specifies the required dependencies and Python version compatibility.
#
# The `find_packages()` function automatically discovers all packages and subpackages in the directory. The `long_description` is read from a README file, which provides a detailed description of the package.
