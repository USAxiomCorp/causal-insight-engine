"""
═══════════════════════════════════════════════════════════════════════════════
SETUP — CAUSAL INSIGHT ENGINE
═══════════════════════════════════════════════════════════════════════════════
"""

from setuptools import setup, find_packages
import os

# Read the README
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements
requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
with open(requirements_path, "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="causal-insight-engine",
    version="1.0.0",
    author="Your Name",
    author_email="your@email.com",
    description="WAD-grounded causal reasoning for pharmaceutical applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/causal-insight-engine",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science AI",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "causal-api=src.causal_insight.api.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
