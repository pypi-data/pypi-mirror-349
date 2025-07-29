
from setuptools import setup, find_packages

setup(
    name="mseep-playwrightdebugger",
    version="0.3.0",
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
    install_requires=['mcp[cli]>=1.5.0', 'playwright>=1.40.0'],
    keywords=["mseep"] + [],
)
