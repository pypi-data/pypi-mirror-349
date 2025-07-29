
from setuptools import setup, find_packages

setup(
    name="mseep-postgres-mcp",
    version="0.3.0",
    description="PostgreSQL Tuning and Analysis Tool",
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
    install_requires=['mcp[cli]>=1.5.0', 'psycopg[binary]>=3.2.6', 'humanize>=4.8.0', 'pglast==7.2.0', 'attrs>=25.3.0', 'psycopg-pool>=3.2.6', 'instructor>=1.7.9'],
    keywords=["mseep"] + [],
)
