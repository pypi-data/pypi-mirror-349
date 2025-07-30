
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="tic_watch",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "opentelemetry-api",
        "opentelemetry-sdk",
        "opentelemetry-instrumentation-fastapi",
        "opentelemetry-instrumentation-asgi",
        "azure-monitor-opentelemetry-exporter"
    ],
    author="TIC",
    author_email="Andrews.Rajkumar@dexian.com",
    description="TIC Watch package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # optional
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
