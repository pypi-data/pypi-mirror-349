from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_danilo",
    version="0.0.1",
    author="Danilo",
    author_email="danilo.r.oliveira1@gmail.com",
    description="image Processing Package using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
#   url="my_github_repository_project_link"
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)