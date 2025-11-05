"""
Setup script for AI Character Toolkit
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding='utf-8').strip().split('\n')
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('#')]

setup(
    name="ai-character-toolkit",
    version="0.1.0",
    author="AI Agent Team",
    author_email="contact@ai-agent.com",
    description="Dynamic AI Character Generation Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ai-agent/ai-character-toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "enhanced": [
            "tiktoken>=0.5.0",
            "textstat>=0.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-toolkit=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_toolkit": [
            "templates/*.j2",
            "templates/*.yaml",
        ],
    },
    zip_safe=False,
    keywords="ai, characters, chatgpt, claude, creative, exploration, validation",
    project_urls={
        "Bug Reports": "https://github.com/ai-agent/ai-character-toolkit/issues",
        "Source": "https://github.com/ai-agent/ai-character-toolkit",
        "Documentation": "https://ai-character-toolkit.readthedocs.io/",
    },
)