"""
# Description

Common constants and default inertia values used in the QRotor subpackage.

Bond lengths and angles were obtained from MAPbI3, see
[K. Drużbicki *et al*., Crystal Growth & Design 24, 391–404 (2024)](https://doi.org/10.1021/acs.cgd.3c01112).

---
"""


import numpy as np
import aton.phys as phys


# Distance between Carbon and Hydrogen atoms (measured from MAPbI3)
distance_CH = 1.09285   # Angstroms
"""Distance of the C-H bond, in Angstroms."""
distance_NH = 1.040263  # Angstroms
"""Distance of the N-H bond, in Angstroms."""

# Angles between atoms:  C-C-H  or  N-C-H  etc (from MAPbI3)
angle_CH_external = 108.7223
"""External angle of the X-C-H bond, in degrees."""
angle_NH_external = 111.29016
"""External angle of the X-N-H bond, in degrees."""
angle_CH = 180 - angle_CH_external
"""Internal angle of the X-C-H bond, in degrees."""
angle_NH = 180 - angle_NH_external
"""Internal angle of the X-N-H bond, in degrees."""

# Rotation radius (calculated from distance and angle)
r_CH = distance_CH * np.sin(np.deg2rad(angle_CH)) * phys.AA_to_m
"""Rotation radius of the methyl group, in meters."""
r_NH = distance_NH * np.sin(np.deg2rad(angle_NH)) * phys.AA_to_m
"""Rotation radius of the amine group, in meters."""

# Inertia, SI units
I_CH3 = 3 * (phys.atoms['H'].mass * phys.amu_to_kg * r_CH**2)
"""Inertia of CH3, in kg·m^2."""
I_CD3 = 3 * (phys.atoms['H'].isotope[2].mass * phys.amu_to_kg * r_CH**2)
"""Inertia of CD3, in kg·m^2."""
I_NH3 = 3 * (phys.atoms['H'].mass * phys.amu_to_kg * r_NH**2)
"""Inertia of NH3, in kg·m^2."""
I_ND3 = 3 * (phys.atoms['H'].isotope[2].mass * phys.amu_to_kg * r_NH**2)
"""Inertia of ND3, in kg·m^2."""

# Rotational energy.
B_CH3 = ((phys.hbar**2) / (2 * I_CH3)) * phys.J_to_meV
"""Rotational energy of CH3, in meV·s/kg·m^2."""
B_CD3 = ((phys.hbar**2) / (2 * I_CD3)) * phys.J_to_meV
"""Rotational energy of CD3, in meV·s/kg·m^2."""
B_NH3 = ((phys.hbar**2) / (2 * I_NH3)) * phys.J_to_meV
"""Rotational energy of NH3, in meV·s/kg·m^2."""
B_ND3 = ((phys.hbar**2) / (2 * I_ND3)) * phys.J_to_meV
"""Rotational energy of ND3, in meV·s/kg·m^2."""

# Potential constants from titov2023 [C1, C2, C3, C4, C5]
constants_titov2023 = [
    [2.7860, 0.0130,-1.5284,-0.0037,-1.2791],  # ZIF-8
    [2.6507, 0.0158,-1.4111,-0.0007,-1.2547],  # ZIF-8 + Ar-1
    [2.1852, 0.0164,-1.0017, 0.0003,-1.2061],  # ZIF-8 + Ar-{1,2}
    [5.9109, 0.0258,-7.0152,-0.0168, 1.0213],  # ZIF-8 + Ar-{1,2,3}
    [1.4526, 0.0134,-0.3196, 0.0005,-1.1461],  # ZIF-8 + Ar-{1,2,4}
    ]
"""Potential constants from
[K. Titov et al., Phys. Rev. Mater. 7, 073402 (2023)](https://link.aps.org/doi/10.1103/PhysRevMaterials.7.073402)
for the `aton.qrotor.potential.titov2023` potential.
In meV units.
"""

