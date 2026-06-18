import numpy as np
import scipy.signal as signal


class BaseVolProc:
    """Signal processing and geometric transformations for 3D array data pools."""

    def make_mask(self):
        """Binarize the volume by converting all non-zero array elements into 1."""
        loc = np.where(self.vol != 0)
        self.vol[loc] = 1

    def normalize_01(self):
        """Rescale the active volume data linearly to the range [0, 1]."""
        self.vol -= self.vol.min()
        self.vol *= 1 / self.vol.max()

    def normalize_sum(self):
        """Normalize the volume elements so that their global total sums to 1."""
        self.vol *= 1 / self.vol.sum()

    def zmean_subtraction(self):
        """Subtract the global mean profile taken over the z-slices.

        Transposes data alignment tracking vectors temporarily to extract mean configurations.
        """
        vol_aligned = np.swapaxes(self.vol, 0, 2)
        print(vol_aligned.shape)

        zmean = np.mean(vol_aligned, axis=0)
        vol_aligned -= zmean

        self.vol = np.swapaxes(vol_aligned, 0, 2)

    def convolve(self, kern_L: int = 2, kern_n: int = 5, std_x: float = 1.0, std_y: float = 1.0, std_z: float = 1.0) -> np.ndarray:
        """Convolve the 3D volume with a Gaussian kernel using an FFT approach.

        Replaces internal tracking datasets directly with computed blur metrics.
        Trims bounding elements to reduce computational window artifact edges.

        Parameters
        ----------
        kern_L : int, default 2
            Symmetric spatial bounds configuration limit covering kernel reach (+/- bounds).
        kern_n : int, default 5
            Resolution footprint grid pixel count across kernel matrix dimensions.
        std_x : float, default 1.0
            Standard deviation spread parameter tracking Gaussian along x-axis.
        std_y : float, default 1.0
            Standard deviation spread parameter tracking Gaussian along y-axis.
        std_z : float, default 1.0
            Standard deviation spread parameter tracking Gaussian along z-axis.

        Returns
        -------
        kern : np.ndarray
            The generated 3D Gaussian kernel array block.
        """
        x_space = np.linspace(-kern_L, kern_L, kern_n)
        y_space = np.linspace(-kern_L, kern_L, kern_n)
        z_space = np.linspace(-kern_L, kern_L, kern_n)

        x_mesh, y_mesh, z_mesh = np.meshgrid(x_space, y_space, z_space)

        kern = np.exp(- (x_mesh**2 / (2 * std_x**2) + y_mesh**2 / (2 * std_y**2) + z_mesh**2 / (2 * std_z**2)))
        blur = signal.fftconvolve(self.vol, kern)

        kern_n_half = int((kern_n - 1) / 2)
        blur = blur[kern_n_half:-kern_n_half, kern_n_half:-kern_n_half, kern_n_half:-kern_n_half]
        self.vol = blur
        return kern

    def convolve_tophat(self, kern_L: int = 2, kern_n: int = 5, lim_x: float = 1.0, lim_y: float = 1.0, lim_z: float = 1.0) -> np.ndarray:
        """Convolve the volume using a structural Top-Hat filter box template.

        Replaces internal tracking data arrays directly.

        Parameters
        ----------
        kern_L : int, default 2
            Symmetric spatial bounds footprint tracking boundary coordinates (+/- limits).
        kern_n : int, default 5
            Footprint spatial length pixel dimension within matrix configuration arrays.
        lim_x : float, default 1.0
            Physical size limit boundary of window cutoffs on x dimensions.
        lim_y : float, default 1.0
            Physical size limit boundary of window cutoffs on y dimensions.
        lim_z : float, default 1.0
            Physical size limit boundary of window cutoffs on z dimensions.

        Returns
        -------
        kern : np.ndarray
            The structural 3D box binary filtering kernel.
        """
        x_space = np.linspace(-kern_L, kern_L, kern_n)
        y_space = np.linspace(-kern_L, kern_L, kern_n)
        z_space = np.linspace(-kern_L, kern_L, kern_n)

        x_mesh, y_mesh, z_mesh = np.meshgrid(x_space, y_space, z_space)

        x_cond = np.abs(x_mesh) <= lim_x
        y_cond = np.abs(y_mesh) <= lim_y
        z_cond = np.abs(z_mesh) <= lim_z

        xy_cond = np.logical_and(x_cond, y_cond)
        xyz_cond = np.logical_and(xy_cond, z_cond)

        kern = np.zeros((kern_n, kern_n, kern_n))
        kern[np.where(xyz_cond)] = 1

        blur = signal.fftconvolve(self.vol, kern)

        kern_n_half = int((kern_n - 1) / 2)
        blur = blur[kern_n_half:-kern_n_half, kern_n_half:-kern_n_half, kern_n_half:-kern_n_half]
        self.vol = blur
        return kern

    def convolve2D(self, kern_L: int = 2, kern_n: int = 5, std_y: float = 1.0, std_z: float = 1.0):
        """Apply a 2D Gaussian filter slicing slice-by-slice along the first dimension.

        Parameters
        ----------
        kern_L : int, default 2
            Kernel coordinate span dimension limits (+/- reach scale parameters).
        kern_n : int, default 5
            Kernel grid pixel allocation dimensions along y and z.
        std_y : float, default 1.0
            Gaussian deviation filter width mapping across y dimension lines.
        std_z : float, default 1.0
            Gaussian deviation filter width mapping across z dimension lines.
        """
        y_space = np.linspace(-kern_L, kern_L, kern_n)
        z_space = np.linspace(-kern_L, kern_L, kern_n)

        y_mesh, z_mesh = np.meshgrid(y_space, z_space)

        kern = np.exp(- (y_mesh**2 / (2 * std_y**2) + z_mesh**2 / (2 * std_z**2)))
        kern_n_half = int((kern_n - 1) / 2)
        blur = np.zeros(self.vol.shape)
        for i, yz in enumerate(self.vol):
            blur2D = signal.fftconvolve(yz, kern)
            blur[i] = blur2D[kern_n_half:-kern_n_half, kern_n_half:-kern_n_half]

        self.vol = blur

    def get_line(self, axis: int, ind1: int, ind2: int, ind1_d: int = 0, ind2_d: int = 0) -> np.ndarray:
        """Extract a 1D line profile by integrating sub-volumes across specific boundaries.

        Parameters
        ----------
        axis : int
            The axis index along which the 1D line should run (0, 1, or 2).
        ind1 : int
            Starting index offset bounds for the first transverse axis.
        ind2 : int
            Starting index offset bounds for the second transverse axis.
        ind1_d : int, default 0
            The thickness (index delta) to integrate over for the first transverse axis.
        ind2_d : int, default 0
            The thickness (index delta) to integrate over for the second transverse axis.

        Returns
        -------
        lin : np.ndarray
            1D array tracking values mapping across target lines.
        """
        if axis % 3 == 0:
            lin = self.vol[:, ind1:ind1+ind1_d+1, ind2:ind2+ind2_d+1].sum(axis=(1, 2))
        elif axis % 3 == 1:
            lin = self.vol[ind1:ind1+ind1_d+1, :, ind2:ind2+ind2_d+1].sum(axis=(0, 2))
        else:
            lin = self.vol[ind1:ind1+ind1_d+1, ind2:ind2+ind2_d+1, :].sum(axis=(0, 1))

        return lin
