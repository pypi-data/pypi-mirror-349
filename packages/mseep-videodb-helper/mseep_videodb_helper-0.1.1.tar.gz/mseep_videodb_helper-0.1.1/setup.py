
from setuptools import setup, find_packages

setup(
    name="mseep-videodb_helper",
    version="0.1.0",
    description="Add your description here",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['boto3>=1.37.3', 'firecrawl-py>=1.14.1', 'gitignore-parser>=0.1.11', 'google-genai>=1.4.0', 'matplotlib>=3.9.4', 'myst-parser>=3.0.1', 'nbconvert>=7.16.6', 'numpy>=2.0.2', 'openai>=1.63.2', 'python-dotenv>=1.0.1', 'pyyaml>=6.0.2', 'rich>=13.9.4', 'sphinx>=7.4.7', 'sphinx-markdown-builder>=0.6.8', 'tiktoken>=0.9.0', 'tree-sitter-python>=0.23.0'],
    keywords=["mseep"] + [],
)
