from setuptools import setup, find_packages

setup(
    name="django_backend_utils",  # Unique package name
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.1.2"
    ],
    author="Dennis Kamau",
    author_email="kamadennis05@gmail.com",
    description="A django Backend Utils For Laxnit Tech projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://link.com",  # Your repository
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)