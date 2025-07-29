from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='ascii_mp4_video_player_exp',
    version='0.16',
    author='paul',
    author_email='paul@kfsoft.info',
    description='ASCII mp4 video player experimental',
    packages=['ascii_mp4_video_player_exp'],  
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'opencv-python',
        'numpy',
        'windows-curses ; platform_system == "Windows"'
    ],
)
