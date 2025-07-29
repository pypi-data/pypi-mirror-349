
from setuptools import setup, find_packages

setup(
    name="mseep-employee",
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
    install_requires=['beeai-framework>=0.1.4', 'mcp[cli]>=1.3.0', 'requests>=2.32.3'],
    keywords=["mseep"] + [],
)
