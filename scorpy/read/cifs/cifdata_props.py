import numpy as np


class CifDataProperties:
    """Properties container managing direct and reciprocal crystal lattice information."""

    @property
    def a(self):
        """Direct lattice vector a.

        Returns
        -------
        ndarray
            Vector elements as a float array of shape (3,).
        """
        return self._a

    @property
    def b(self):
        """Direct lattice vector b.

        Returns
        -------
        ndarray
            Vector elements as a float array of shape (3,).
        """
        return self._b

    @property
    def c(self):
        """Direct lattice vector c.

        Returns
        -------
        ndarray
            Vector elements as a float array of shape (3,).
        """
        return self._c

    @property
    def inten_loc(self):
        """Indices where the scattering reflection profiles possess intensities above zero.

        Returns
        -------
        tuple of ndarray
            Tuple containing the index positions matching the criteria.
        """
        return np.where(self.scat_bragg[:, -1] > 0)

    @property
    def a_mag(self):
        """Magnitude/length of direct lattice vector a.

        Returns
        -------
        float
            Length of the side 'a'.
        """
        return self._a_mag

    @property
    def b_mag(self):
        """Magnitude/length of direct lattice vector b.

        Returns
        -------
        float
            Length of the side 'b'.
        """
        return self._b_mag

    @property
    def c_mag(self):
        """Magnitude/length of direct lattice vector c.

        Returns
        -------
        float
            Length of the side 'c'.
        """
        return self._c_mag

    @property
    def ast_mag(self):
        """Magnitude/length of reciprocal lattice vector a*.

        Returns
        -------
        float
            Reciprocal space side length magnitude.
        """
        return self._ast_mag

    @property
    def bst_mag(self):
        """Magnitude/length of reciprocal lattice vector b*.

        Returns
        -------
        float
            Reciprocal space side length magnitude.
        """
        return self._bst_mag

    @property
    def cst_mag(self):
        """Magnitude/length of reciprocal lattice vector c*.

        Returns
        -------
        float
            Reciprocal space side length magnitude.
        """
        return self._cst_mag

    @property
    def alpha(self):
        """Angle between direct lattice vectors b and c in radians.

        Returns
        -------
        float
            Lattice alpha angle.
        """
        return self._alpha

    @property
    def beta(self):
        """Angle between direct lattice vectors a and c in radians.

        Returns
        -------
        float
            Lattice beta angle.
        """
        return self._beta

    @property
    def gamma(self):
        """Angle between direct lattice vectors a and b in radians.

        Returns
        -------
        float
            Lattice gamma angle.
        """
        return self._gamma

    @property
    def ast(self):
        """Reciprocal lattice vector a*.

        Returns
        -------
        ndarray
            Reciprocal vector elements as a float array of shape (3,).
        """
        return self._ast

    @property
    def bst(self):
        """Reciprocal lattice vector b*.

        Returns
        -------
        ndarray
            Reciprocal vector elements as a float array of shape (3,).
        """
        return self._bst

    @property
    def cst(self):
        """Reciprocal lattice vector c*.

        Returns
        -------
        ndarray
            Reciprocal vector elements as a float array of shape (3,).
        """
        return self._cst

    @property
    def cif(self):
        """Dictionary representation of the processed CIF source file details.

        Returns
        -------
        dict
            CIF structural details mapping dictionary.
        """
        return self._cif

    @property
    def spg(self):
        """Space group designation of the crystal structure.

        Returns
        -------
        str
            Hermann-Mauguin space group identifier format string.
        """
        return self._spg

    @property
    def scat_bragg(self):
        """Array of Bragg scattering information.

        Returns
        -------
        ndarray
            An (N, 4) shaped array where columns denote h, k, l, and intensity.
        """
        return self._scat_bragg

    @property
    def scat_rect(self):
        """Array of rectilinear Cartesian mapping scattering details.

        Returns
        -------
        ndarray
            An (N, 4) shaped array with columns corresponding to qx, qy, qz, and intensity.
        """
        return self._scat_rect

    @property
    def scat_sph(self):
        """Array of spherical vector coordinates formatting data.

        Returns
        -------
        ndarray
            An (N, 4) shaped array with columns tracking q magnitude, polar theta [-pi/2, pi/2],
            azimuthal phi [0, 2pi], and diffraction intensity metrics.
        """
        return self._scat_sph

    @property
    def qmax(self):
        """Maximum scattering vector distance restriction limit bounds.

        Returns
        -------
        float
            Resolution limit boundary threshold.
        """
        return self._qmax
