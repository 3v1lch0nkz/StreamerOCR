from setuptools import setup, find_packages

setup(
    name="streamer-ocr",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'PyQt5==5.15.9',
        'pytesseract==0.3.10',
        'keyboard==0.13.5',
        'Pillow==9.5.0',
        'mss==9.0.1',
        'pyttsx3==2.90',
    ],
    entry_points={
        'console_scripts': [
            'streamer-ocr=src.main:main',
        ],
    },
    package_data={
        'streamer_ocr': ['resources/*'],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight desktop utility for OCR and TTS processing of screen regions",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    keywords="ocr, tts, screen-capture, streaming",
    url="https://github.com/yourusername/streamer-ocr",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.11',
) 