from setuptools import setup, find_packages

setup(
    name="phenotyping_segmentation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "opencv-python",
        "torch",
        "segmentation-models-pytorch",
    ],
    author="Lin Wang",
    author_email="wanglin9926@gmail.com",
    description="A pipeline for segmentation and root phenotyping.",
    long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    url="https://https://github.com/Salk-Harnessing-Plants-Initiative/phenotyping-segmentation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
