from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        name="effspm._effspm",
        sources=[
            "effspm/_effspm.cpp",
            "effspm/freq_miner.cpp",
            "effspm/load_inst.cpp",
            "effspm/utility.cpp",
            # "effspm/build_mdd.cpp",  # ❌ REMOVE this line
            "effspm/btminer/src/freq_miner.cpp",
            "effspm/btminer/src/load_inst.cpp",
            "effspm/btminer/src/utility.cpp",
            "effspm/btminer/src/build_mdd.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
            "effspm",
            "effspm/btminer/src"
        ],
        language="c++",
        extra_compile_args=["-std=c++11"]
    )
]

setup(
    name="effspm",
    version="0.1.12",
    description="Efficient Sequential Pattern Mining Library",
    author="Yeswanth Vootla",
    packages=["effspm"],
    ext_modules=ext_modules,
    zip_safe=False,
    install_requires=["pybind11"]
)
