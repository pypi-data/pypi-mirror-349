from setuptools import setup, find_packages

setup(
    name='autopr-cli',
    version='0.2.1',
    py_modules=['run_cli'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aipr=run_cli:main',
        ],
    },
    install_requires=[],
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI tool to automate PR creation and listing.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/leaopedro/autopr',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)