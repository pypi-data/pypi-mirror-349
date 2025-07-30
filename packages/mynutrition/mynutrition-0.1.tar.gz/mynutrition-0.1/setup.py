from setuptools import setup, find_packages

setup(
    name='mynutrition',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'requests',
        'pandas',
        'numpy',
        'matplotlib'
    ],
    description='Nutrition tools and API integration for dietary analysis',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/mynutrition',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)