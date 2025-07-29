from setuptools import setup, find_packages

setup(
    name="genetic_algorithm_library",
    version="0.1.0",
    author="Julian Lara, Johan Rojas",
    author_email="johansebastianrojasramirez7@gmail.com",
    description="Librería de algoritmos genéticos adaptativos para problemas de optimización",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zaxazgames1/genetic-algorithm-library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "pandas>=1.1.0",
    ],
)   