
from setuptools import setup, find_packages

setup(
    name="mseep-pymcpautogui",
    version="0.1.1",
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
    install_requires=['mcp[cli]>=1.6.0', 'pyautogui>=0.9.54', 'pygetwindow>=0.0.9'],
    keywords=["mseep"] + [],
)
