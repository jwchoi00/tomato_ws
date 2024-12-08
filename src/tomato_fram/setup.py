from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'tomato_fram'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name,'launch'), glob('launch/*.launch.py')),
        (os.path.join('share',package_name,'urdf'), glob('urdf/*.xacro')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='g1',
    maintainer_email='jwchoi0017@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'tomato_gui = tomato_fram.tomato_gui:main',
            'tomato_gui_tb1 = tomato_fram.tomato_gui_tb1:main',
            'tomato_gui_tb2 = tomato_fram.tomato_gui_tb2:main',
            'diff_driver = tomato_fram.diff_driver:main',
            'tomato_object_detect = tomato_fram.tomato_object_detect:main',
            'tomato_object_detect_tb1 = tomato_fram.tomato_object_detect_tb1:main',
            'tomato_object_detect_tb2 = tomato_fram.tomato_object_detect_tb2:main',
        ],
    },
)
