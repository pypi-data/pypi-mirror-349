from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="miniwifi",
    version="1.2.0",
    author="MrFidal",
    author_email="mrfidal@proton.me",
    description="Python Wi-Fi security toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mr-fidal/miniwifi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pywifi",
    ],
    entry_points={
        'console_scripts': [
            'miniwifi-scan=miniwifi.cli:scan_cli',
            'miniwifi-crack=miniwifi.cli:crack_cli',
        ],
    },
    keywords="wifi security networking pentesting",
    project_urls={
        "Bug Reports": "https://github.com/mr-fidal/miniwifi/issues",
        "Source": "https://github.com/mr-fidal/miniwifi",
    },
    license="MIT",
)
