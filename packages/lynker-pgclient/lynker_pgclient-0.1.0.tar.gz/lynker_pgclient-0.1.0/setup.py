from setuptools import setup, find_packages

setup(
    name="lynker-pgclient",
    version="0.1.0",
    description="Postgres client utilities for Lynker",
    author="Naveed",
    author_email="m.naveedashfaq@gmail.com",
    packages=find_packages(),    # or a hard-coded list
    install_requires=[
        # e.g. "psycopg2>=2.9",
    ],
)
