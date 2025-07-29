# Matrix-based shape sensitivity analysis for linear strain energy of triangular thin shell elements
Source code of K. Hayashi and R. Mesnil, "Matrix-based shape sensitivity analysis for linear strain energy of triangular thin shell elements"

# Install
The module can be installed through PyPI using the following command on the command prompt window:
```
pip install dktshell
```

# How to use
```
algo = dktshell.DKTAnalysis()
displacement,internal_force,reaction = algo.RunStructuralAnalysis(vert,face_tri,dirichlet,load,thickness=0.25,elastic_modulus=4.32e8,poisson_ratio=0.0) # Use this input for Scordelis-Lo roof example
strain_energy,strain_energy_gradient = algo.StrainEnergy_with_Gradient(vert,face_tri,dirichlet,load,thickness=1,elastic_modulus=1,poisson_ratio=0.25)
```

For more detailed example, please find **example.py** in the GitHub repository.
The input structural models required to run **example.py** are stored in the **structural_models** folder.

# Note
If you run Python program in a directory and import this module for the first time, it will take several minutes for just-in-time (JIT) compilation using numba.
This JIT compilation requires only once, and you can smoothly import this module from the second time.
