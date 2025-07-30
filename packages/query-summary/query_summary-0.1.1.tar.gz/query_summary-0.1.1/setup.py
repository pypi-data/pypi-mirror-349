from setuptools import setup, find_packages

setup(
    name="query_summary",  # Package name
    version="0.1.1",  # Initial version
    description="A Flask middleware to track MongoDB queries and provide query statistics.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="mstfsu",
    author_email="su.mustafa@hotmail.com",
    url="https://github.com/mstfsu/query_summary",  # Main project URL (GitHub repo)
    project_urls={  # Additional URLs
        "Bug Tracker": "https://github.com/mstfsu/query_summary/issues",
        "Documentation": "https://github.com/mstfsu/query_summary#readme",
        "Source Code": "https://github.com/mstfsu/query_summary",
    },
    packages=find_packages(),
    install_requires=[
        "Flask>=2.0",
        "pymongo>=4.0",
        "mongoengine>=0.24.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    include_package_data=True,
)