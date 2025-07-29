from setuptools import setup, find_packages

setup(
    name="google-places-scraper",
    version="0.1.2",
    description="A wrapper to scrape Google Places API with logging and export support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Muhammad Arsalan",
    author_email="arsalan.9798@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "pyyaml",
        "geopy",
    ],
    entry_points={
        "console_scripts": [
            "google-places-scraper=google_places_scraper.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
