from setuptools import setup, find_packages

setup(
    name="myfastapiapp",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "pillow",
        "torch",
        "pandas",
        "requests",
        "yolov5"
    ],
    entry_points={
        'console_scripts': [
            'myfastapiapp=uvicorn:main',
        ],
    },
    author="Your Name",
    description="FastAPI app with YOLOv5 model inference",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
    ],
)
