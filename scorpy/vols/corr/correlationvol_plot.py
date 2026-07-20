
from ...utils.baseplot import BasePlot
import matplotlib.pyplot as plt
import numpy as np


class CorrelationVolPlot(BasePlot):
    """
    Mixin class providing plotting functionality for CorrelationVol.

    Inherits all plotting behavior directly from ``BasePlot`` without
    modification.
    """

    def plot_char_c(self, c):
        plt.plot(self.psipts, c/(2*np.sin(self.psipts/2)))

