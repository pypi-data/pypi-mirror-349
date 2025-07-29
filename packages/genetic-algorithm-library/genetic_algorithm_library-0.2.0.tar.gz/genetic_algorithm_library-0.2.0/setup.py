from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="genetic_algorithm_library",
    version="0.2.0",
    author="Julian Lara, Johan Rojas",
    author_email="johansebastianrojasramirez7@gmail.com",
    description="Librería avanzada de algoritmos genéticos adaptativos para problemas de optimización",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zaxazgames1/genetic-algorithm-library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "matplotlib>=3.3.0",
        "pandas>=1.1.0",
        "scipy>=1.5.0",
    ],
    keywords="genetic algorithm, optimization, evolutionary computation, adaptive algorithms, multi-objective optimization, TSP, permutation",
    project_urls={
        "Bug Tracker": "https://github.com/Zaxazgames1/genetic-algorithm-library/issues",
        "Documentation": "https://github.com/Zaxazgames1/genetic-algorithm-library/wiki",
        "Source Code": "https://github.com/Zaxazgames1/genetic-algorithm-library",
    },
    include_package_data=True,
    package_data={
        "genetic_algorithm": ["examples/*.py"],
    },
)