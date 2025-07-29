
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-data-wrangler",
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
    install_requires=['aiofiles>=24.1.0', 'mcp[cli]>=1.6.0', 'numpy>=2.2.4', 'polars>=1.26.0', 'pydantic>=2.11.1', 'pydantic-settings>=2.8.1', 'python-dotenv>=1.1.0', 'scikit-learn>=1.6.1'],
    keywords=["mseep"] + [],
)
