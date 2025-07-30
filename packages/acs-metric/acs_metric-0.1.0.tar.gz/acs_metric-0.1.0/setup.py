from setuptools import setup, find_packages

setup(
    name="acs-metric",
    version="0.1.0",
    author="Afsal-CP",
    author_email="your.email@domain.com",
    description="Accessibility Comprehension Score (ACS) Metric for Text Evaluation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Afsal-CP/acs-metric",
    project_urls={
        "Bug Tracker": "https://github.com/Afsal-CP/acs-metric/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: General",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.2.0",
        "scikit-learn>=0.24.0",
        "scipy>=1.6.0",
    ],
)