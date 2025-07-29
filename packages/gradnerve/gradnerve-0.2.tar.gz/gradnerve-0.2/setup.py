from setuptools import setup, find_packages

setup(
    name='gradnerve',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy'
    ],
    python_requires='>=3.6',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/gradnerve',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT'
)