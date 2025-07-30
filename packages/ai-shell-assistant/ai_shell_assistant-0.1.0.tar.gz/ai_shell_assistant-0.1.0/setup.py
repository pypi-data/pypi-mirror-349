"""
Setup script for AI CLI package.
"""
import os
from setuptools import setup, find_packages

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Get version from package
def get_version():
    """Get version from ai_cli/__init__.py"""
    version_file = os.path.join(this_directory, 'ai_cli', '__init__.py')
    with open(version_file, encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    raise RuntimeError('Unable to find version string.')

setup(
    name="ai-shell-assistant",
    version=get_version(),
    author="PierrunoYT",
    author_email="pierrebruno@hotmail.ch",
    description="AI-powered command-line interface with extensible tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PierrunoYT/ai-shell-assistant",
    project_urls={
        "Bug Tracker": "https://github.com/PierrunoYT/ai-shell-assistant/issues",
        "Documentation": "https://github.com/PierrunoYT/ai-shell-assistant#readme",
        "Source Code": "https://github.com/PierrunoYT/ai-shell-assistant",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-cli=ai_cli.cli:main",
            "ai-shell=ai_cli.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "ai", "cli", "shell", "assistant", "openai", "gpt", "command-line", 
        "natural-language", "automation", "tools", "file-operations"
    ],
)
