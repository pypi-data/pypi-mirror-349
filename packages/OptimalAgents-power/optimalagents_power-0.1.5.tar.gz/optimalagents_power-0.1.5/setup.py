from setuptools import setup, find_packages

setup(
    name='OptimalAgents-power',
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'flask',
        'requests',
        'uvicorn'
    ],
    entry_points={
        'console_scripts': [
            'create-superpower=optimalagents.cli:create_project'
        ],
    },
    author='Sandilya Kishlay',
    author_email='sandilyakishlay@gmail.com',
    description='A project generator for web superheroes using FastAPI, Flask, or REST.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sandilyaKishlay',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.11',
)