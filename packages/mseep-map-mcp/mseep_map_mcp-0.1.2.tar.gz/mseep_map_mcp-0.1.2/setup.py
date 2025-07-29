
from setuptools import setup, find_packages

setup(
    name="mseep-map-mcp",
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
    install_requires=['folium>=0.19.4', 'mcp[cli]===1.2.0rc1', 'requests>=2.32.3', 'selenium>=4.27.1'],
    keywords=["mseep"] + [],
)
