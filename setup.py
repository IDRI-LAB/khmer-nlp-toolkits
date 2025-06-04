from setuptools import setup, find_packages

setup(
    name='khmer_nlptk',
    version='0.1.0',
    author='Sopagna HEANG',
    author_email='sopagna.heang@gmail.com',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo',  # Optional, your project repo URL
    # packages=find_packages(where='khmer_nlptk'),  # Find packages under src/
    package_dir={'khmer_nlptk': 'khmer_nlptk'},               # Root package dir is src/
    classifiers=[
        'Programming Language :: Python :: 3',
        # 'License :: OSI Approved :: MIT License',  # Change if not MIT
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        # List your runtime dependencies here, e.g. 'requests', 'numpy'
    ],
    # entry_points={
    #     'console_scripts': [
    #         # 'cli-name=module:function', e.g. 'mytool=module1.main:main'
    #     ],
    # },
)
