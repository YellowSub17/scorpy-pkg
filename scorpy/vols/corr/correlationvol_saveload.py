
class CorrelationVolSaveLoad:
    """
    Mixin class providing save/load extensions for CorrelationVol.

    Adds a ``[corr]`` section to the config file written/read by the
    parent ``BaseVol`` save/load routines, capturing the correlation-
    specific attributes.
    """

    def _save_extra(self, f):
        """
        Write CorrelationVol-specific attributes to a config file.

        Parameters
        ----------
        f : file object
            Open, writable file object to append the ``[corr]`` config
            section to.

        Returns
        -------
        None
        """
        f.write('[corr]\n')
        f.write(f'qmax = {self.qmax}\n')
        f.write(f'qmin = {self.qmin}\n')
        f.write(f'nq = {self.nq}\n')
        f.write(f'npsi = {self.npsi}\n')
        f.write(f'dq = {self.dq}\n')
        f.write(f'dpsi = {self.dpsi}\n')
        f.write(f'cos_sample = {self.cos_sample}\n')

    def _load_extra(self, config):
        """
        Load CorrelationVol-specific attributes from a config parser.

        Parameters
        ----------
        config : configparser.ConfigParser
            Parsed config object containing a ``[corr]`` section with a
            ``cos_sample`` boolean field.

        Returns
        -------
        None
            Sets ``self._cos_sample`` in place.
        """
        self._cos_sample = config.getboolean('corr', 'cos_sample')
