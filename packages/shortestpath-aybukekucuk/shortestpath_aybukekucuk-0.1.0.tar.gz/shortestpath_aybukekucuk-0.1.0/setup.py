from setuptools import setup, find_packages

setup(
    name='shortestpath_aybukekucuk',  # TİRE değil ALT ÇİZGİ kullan! İki tire kullanma!
    version='0.1.0',
    description='En kısa yol hesaplama modülü',
    author='Aybuke Kucuk',
    author_email='aybuke@example.com',
    url='https://github.com/aaybukekucuk/shortestpath',
    packages=find_packages(),
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)