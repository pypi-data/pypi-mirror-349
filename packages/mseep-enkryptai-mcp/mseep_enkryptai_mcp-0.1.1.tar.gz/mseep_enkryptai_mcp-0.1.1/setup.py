
from setuptools import setup, find_packages

setup(
    name="mseep-enkryptai-mcp",
    version="0.1.0",
    description="",
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
    install_requires=['enkryptai-sdk==1.0.4', 'httpx>=0.28.1', 'mcp[cli]>=1.6.0', 'pandas>=2.2.3', 'requests>=2.32.3', 'tabulate>=0.9.0'],
    keywords=["mseep"] + [],
)
