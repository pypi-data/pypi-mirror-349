# === ПУТЬ К ФАЙЛУ: setup.py ===
from setuptools import setup, find_packages

setup(
    name="r7kit",
    version="0.2",
    description="Task/workflow toolkit for Temporal + Redis",
    author="Dmitry Lugin",
    author_email="",
    packages=find_packages(include=["r7kit", "r7kit.*"]),
    install_requires=[
        "temporalio>=1.0",
        "redis>=4.6",
        "pydantic>=2.0",
        "orjson>=3.9",
    ],
    python_requires=">=3.10",
)