from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="flipkart-project",
    version="0.4",
    author="Swatej Wagh",
    description="Flipkart Product Recommendation Chatbot",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.10,<3.13",
)