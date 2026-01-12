"""
Setup script for matrix-coder-agent package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="matrix-coder-agent",
    version="0.2.0",
    author="Mirror12k",
    description="Autonomous development agent using AWS Bedrock and Strands SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mirror12k/matrix-coder-agent",
    project_urls={
        "Bug Tracker": "https://github.com/mirror12k/matrix-coder-agent/issues",
        "Documentation": "https://github.com/mirror12k/matrix-coder-agent#readme",
        "Source Code": "https://github.com/mirror12k/matrix-coder-agent",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "strands-agents>=0.1.0",
        "strands-agents-tools>=0.1.0",
        "boto3>=1.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "matrix-coder-agent=matrix_coder_agent.cli:main",
        ],
    },
    keywords="ai agent aws bedrock strands autonomous development llm",
    license="MIT",
    include_package_data=True,
)
