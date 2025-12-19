from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="agentix-cli",  # Changed from just "agentix" to avoid conflicts
    version="0.1.0",
    author="najafali14",
    author_email="najafali32304@gmail.com",  # Update this
    description="AI-powered CLI agent that converts natural language to shell commands",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/najafali14/Agentix",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai-agents>=0.6.4",
        "nest-asyncio>=1.6.0",
        "pydantic>=2.5.0",
        "prompt-toolkit>=3.0.0",
        "rich>=13.0.0",
        "openai>=2.14.0",
    ],
    entry_points={
        "console_scripts": [
            "agentix=agentix.main:main",  # Entry point
        ],
    },
    keywords="cli, shell, ai, automation, command-line",
    project_urls={
        "Bug Reports": "https://github.com/najafali14/Agentix/issues",
        "Source": "https://github.com/najafali14/Agentix",
    },
)
