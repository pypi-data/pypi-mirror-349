# setup.py
from setuptools import setup, find_packages

setup(
    name="terminal-chat-room",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["cli"],
    install_requires=[
        "python-socketio",
    ],
    entry_points={
        "console_scripts": [
            "room=cli:main",
        ],
    },
    author="Vishesh Jain",
    author_email="visheshj2005@example.com",
    description="A terminal-based chat client using Socket.IO",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/visheshj2005/text-chat-render",  # or your final repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
