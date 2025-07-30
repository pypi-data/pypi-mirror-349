from setuptools import setup, find_packages

setup(
    name='Annchih',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[],
    author='Annchih',
    author_email='you@example.com',
    description='Утилита для извлечения ключевых слов и краткого резюме из текста',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/Annchih',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
