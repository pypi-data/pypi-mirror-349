from setuptools import setup, find_packages

setup(
    name="fastapi-cli-starter",
    version="0.1.0",
    description="CLI tool to bootstrap FastAPI apps like create-react-app",
    author="Your Name",
    author_email="you@example.com",
    license="MIT",
    packages=find_packages(),
    py_modules=["cli"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "create-fastapi-app = cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
