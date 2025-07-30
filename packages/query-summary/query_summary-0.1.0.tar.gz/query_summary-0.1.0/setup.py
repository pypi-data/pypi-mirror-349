from setuptools import setup, find_packages

setup(
    name="query_summary",
    version="0.1.0",
    description="A Flask middleware to track MongoDB queries and display summaries.",
    author="mstfsu",
    author_email="su.mustafa@hotmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pymongo>=4.0",
        "flask>=2.0",
        "mongoengine>=0.24.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)