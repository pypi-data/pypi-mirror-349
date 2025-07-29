from setuptools import setup, find_packages

setup(
    name="pamphlet_detector",
    version="1.0.0",
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
            'pamphlet_detector=uvicorn:main',
        ],
    },
    author="Bhargo Innovations",
    description="FastAPI app with YOLOv5 model inference",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: FastAPI",
    ],
)
