from setuptools import setup, find_packages
import os
setup(
    name="chatgpt-selenium",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "selenium>=4.0.0",
    ],
    author="AnhVTH",
    author_email="anhvth.226@gmail.com",
    description="A package for interacting with ChatGPT using Selenium",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chatgpt-selenium",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'collect_data=chatgpt_selenium.scripts.collect_data:main',
            'submit_reqs=chatgpt_selenium.scripts.submit_reqs:main',
        ],
    }
)
