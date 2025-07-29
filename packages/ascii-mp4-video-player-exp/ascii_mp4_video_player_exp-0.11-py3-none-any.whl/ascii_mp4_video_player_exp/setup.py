from setuptools import setup

setup(
    name='ascii_mp4_video_player_exp',
    version='0.11',
    author='paul',
    author_email='paul@kfsoft.info',
    description='ASCII mp4 video player experimental',
    packages=['ascii_mp4_video_player_exp'],  
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
