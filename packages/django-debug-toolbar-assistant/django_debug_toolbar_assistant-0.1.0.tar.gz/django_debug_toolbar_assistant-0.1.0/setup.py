from setuptools import setup, find_packages

setup(
    name="django-debug-toolbar-assistant",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=3.2",
        "django-debug-toolbar>=4.0",
        "google-cloud-aiplatform>=1.40",
        "markdown",
    ],
    description="A Django Debug Toolbar panel for AI-assisted debugging using Gemini.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Will Meyers",
    author_email="mail@willmeye.rs",
    url="https://github.com/willmeyers/django-debug-toolbar-assistant",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)