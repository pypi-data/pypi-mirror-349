from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        'my_ctools.core',
        [
            'cal_std_mean.cpp',
            'cal_cpr.cpp',
            'cal_all_largest_indicators.cpp',
            'cal_all_longest_indicators.cpp',
            'cal_longest_dd_recover.cpp',
            'cal_max_dd.cpp',
            'cal_rolling_gain_loss.cpp',
        ],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++17', '-O3'],
    ),
]

setup(
    name='my-ctools',
    version='0.1.2',
    author='KevinCJM',
    description='Fast column-wise std calculator using C++ thread pool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['my_ctools'],
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires='>=3.6',
)
