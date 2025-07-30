import numpy as np
import numpy.linalg as la
from numpy.typing import ArrayLike


def gen_lorentzian_spectrum(energies: list[float], fwhm: float | list[float],
                            areas: float | list[float], e_range: list[float]):
    """
    Generates infrared spectrum as sum of Lorentzian functions, each
    peaked at a given energy and with a given area

    Parameters
    ----------
    energies: list[float]
        Vibrational energies (frequencies, wavenumber, ...)
    fwhm: float | list[float]
        Either a fixed  Full Width at Half-Maximum used for all Lorentzians,
        or a list of FWHM values for each lorentzian
    areas: float | list[float]
        Either a fixed area used for all Lorentzians, or a list of
        area values for each lorentzian
    e_range: list[float]
        List of energies at which the spectrum is calculated

    Returns
    -------
    list[float]
        Sum of all Lorentzian functions at each value in e_range
    """

    n_funcs = len(energies)

    if isinstance(fwhm, float):
        fwhm = np.array([fwhm] * n_funcs)
    else:
        fwhm = np.asarray(fwhm)

    if isinstance(areas, float):
        areas = np.array([areas] * n_funcs)
    else:
        areas = np.asarray(areas)

    spectrum = np.sum(
        [
            lorentzian(e_range, fw, energy, area)
            for energy, fw, area in zip(energies, fwhm, areas)
        ],
        axis=0
    )

    return spectrum


def lorentzian(x, fwhm, x0, area):
    """
    Lotenztian L(x) with given peak position (b), fwhm, and area

    L(x) = (0.5*area*fwhm/pi) * 1/((x-x0)**2 + (0.5*fwhm)**2)

    Parameters
    ----------
    x : list[float]
        Continuous variable
    fwhm: float
        Full Width at Half-Maximum
    x0 : float
        Peak position
    area : float
        Area of Lorentzian function

    Return
    ------
    list[float]
        L(x) at each value of x
    """

    lor = 0.5*fwhm/np.pi
    lor *= 1./((x-x0)**2 + (0.5*fwhm)**2)

    lor *= area

    return lor


def gen_gaussian_spectrum(energies: list[float], fwhm: float | list[float],
                          areas: float | list[float], e_range: list[float]):
    """
    Generates infrared spectrum as sum of Gaussian functions, each
    peaked at a given energy and with a given area

    Parameters
    ----------
    energies: list[float]
        Vibrational energies (frequencies, wavenumber, ...)
    fwhm: float | list[float]
        Either a fixed  Full Width at Half-Maximum used for all Gaussians,
        or a list of FWHM values for each Gaussian
    areas: float | list[float]
        Either a fixed area used for all Gaussians, or a list of
        area values for each Gaussian
    e_range: list[float]
        List of energies at which the spectrum is calculated

    Returns
    -------
    list[float]
        Sum of all Gaussian functions at each value in e_range
    """

    n_funcs = len(energies)

    if isinstance(fwhm, float):
        fwhm = np.array([fwhm] * n_funcs)
    else:
        fwhm = np.asarray(fwhm)

    if isinstance(areas, float):
        areas = np.array([areas] * n_funcs)
    else:
        areas = np.asarray(areas)

    spectrum = np.sum(
        [
            gaussian(e_range, fw, energy, area)
            for energy, fw, area in zip(energies, fwhm, areas)
        ],
        axis=0
    )

    return spectrum


def gaussian(x: list[float], fwhm: float, b: float, area: float):
    """
    Gaussian g(x) with given peak position (b), fwhm, and area

    g(x) = area/(c*sqrt(2pi)) * exp(-(x-b)**2/(2c**2))

    c = fwhm/(2*np.sqrt(2*np.log(2)))

    Parameters
    ----------
    x : list[float]
        Continuous variable
    fwhm: float
        Full Width at Half-Maximum
    b : float
        Peak position
    area : float
        Area of gaussian function

    Return
    ------
    list[float]
        g(x) at each value of x
    """

    c = fwhm/(2*np.sqrt(2*np.log(2)))

    a = 1./(c*np.sqrt(2*np.pi))

    gaus = a*np.exp(-(x-b)**2/(2*c**2))

    gaus *= area

    return gaus


def calc_ir_intensities(red_masses: list[float], disp_vecs: ArrayLike,
                        dip_deriv_pa: ArrayLike):
    """
    Calculates infrared intensities using the same approach as Gassian
    these intensities are in fact napierian integrated absorption coefficents
    and should be used as the AREA of a given absorption peak

    Parameters
    ----------
    red_masses: list[float]
        Reduced masses in atomic mass units (u)
    disp_vecs: np.array
        Displacement vectors arranged [3NAtoms, 3NAtoms-6] in Angstrom amu^-1/2
    dip_deriv_pa: np.array
        Dipole derivatives array [3NAtoms, 3] in same order as Gaussian
        writes to fchk file in electron per Angstrom

    Returns
    -------
    list[float]
        Intensity of each mode in km mol-1
    """

    # Dimensions of disp_vecs are [3NAtoms, 3NAtoms-6]
    # Dimensions of dip_deriv_pa are [3NAtoms, 3]

    # Remove sqrt(reduced_mass) weighting from each displacement vector
    disp_vecs /= np.sqrt(red_masses)

    dip_deriv_modes = np.einsum('ji, jk->ki', dip_deriv_pa, disp_vecs)
    # Convert to km^1/2 mol-1/2
    dip_deriv_modes *= 31.2231

    # Intensity in km mol-1 defined as norm squared of dipole derivative
    # vector for a given mode, where dipole derivative vector is
    # [dmu_x/dQ, dmu_y/dQ_y, dmu_z/dQ]
    intensities = la.norm(dip_deriv_modes, axis=1) ** 2

    return intensities
