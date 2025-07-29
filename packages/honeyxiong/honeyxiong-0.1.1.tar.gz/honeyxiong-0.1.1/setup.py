from setuptools import setup, find_packages

setup(
    name="honeyxiong",
    version="0.1.1",  # Новая версия
    packages=find_packages(),
    description="Генератор автомобильных марок и номеров",
    author="JM",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)