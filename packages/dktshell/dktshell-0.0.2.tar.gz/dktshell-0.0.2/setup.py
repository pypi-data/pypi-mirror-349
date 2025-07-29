from setuptools import setup, find_packages

setup(    
     name="dktshell",     
     version="0.0.2",
     install_requires=[
         "numpy>=1.26",
         "scipy>=1.15",
         "numba>=0.61",
     ],
     python_requires=">=3.12", 
     author="Kazuki Hayashi and Romain Mesnil",
     description="Matrix-based structural analysis module for triangulated thin shells using discrete Kirchhoff triangle (DKT) elements.",
     packages=["dktshell"],
)