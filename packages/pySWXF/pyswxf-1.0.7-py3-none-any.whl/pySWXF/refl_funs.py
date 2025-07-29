import numpy as np
import scipy.constants as scc
from lmfit import Model
import pySWXF.refl_funs as refl_funs


def simple_surface(theta, I0, rho1, d1, d2, sig1, sig2):
    """
    Calculates the x-ray reflectivity from a hydrocarbon monolayer on a water surface
    supported on a silicon substrate with oxide layers.

    The sample consists of the following stack (top to bottom):
        - H2O (fixed density)
        - CH2 layer with variable density (rho1), thickness (d1), and roughness (sig1)
        - SiO2 layer with fixed density (2.30 g/cm³), variable thickness (d2), and roughness (sig2)
        - SiO layer (fixed thickness and density)
        - Si substrate (semi-infinite)

    Parameters
    ----------
    theta : array_like
        Incident angles in degrees.

    I0 : float
        Incident beam intensity in photons.

    rho1 : float
        Density of the CH2 layer (in g/cm³).

    d1 : float
        Thickness of the CH2 layer (in Ångströms).

    d2 : float
        Thickness of the SiO2 layer (in Ångströms).

    sig1 : float
        Roughness between CH2 and SiO2 (in Ångströms).

    sig2 : float
        Roughness between SiO2 and SiO (in Ångströms).

    Returns
    -------
    y : ndarray
        Reflected intensity at each incident angle (same shape as theta).
    """

    E0 = 17400  # Photon energy in eV (hardwired for now; could be promoted to a fit parameter)

    # Fixed thickness of SiO layer (in Å)
    d_sio = 1.5

    # Define layer stack: (material_name, density [g/cm³], thickness [Å], roughness [Å])
    layers = [
        ('H2O', 1.0, 0, 0),
        ('CH2', rho1, d1, sig1),
        ('SiO2', 2.30, d2, sig2),
        ('SiO', 1.86, d_sio, 1),
        ('Si', 2.34, 0, 1)
    ]

    # Run reflectivity calculation using reflection_matrix
    _, refl, _, _ = refl_funs.reflection_matrix(theta * scc.degree, E0, layers)

    # Return intensity scaled by incident flux I0
    return I0 * np.abs(refl[:, 0])**2


# Create lmfit model
simple_surface_model = Model(simple_surface)

