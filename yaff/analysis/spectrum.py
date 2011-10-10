# YAFF is yet another force-field code
# Copyright (C) 2008 - 2011 Toon Verstraelen <Toon.Verstraelen@UGent.be>, Center
# for Molecular Modeling (CMM), Ghent University, Ghent, Belgium; all rights
# reserved unless otherwise stated.
#
# This file is part of YAFF.
#
# YAFF is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# YAFF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --


import numpy as np

from molmod.constants import lightspeed
from molmod.units import centimeter
from yaff.log import log
from yaff.analysis.utils import get_hdf5_file, get_slice



__all__ = ['Spectrum']


class Spectrum(object):
    def __init__(self, fn_hdf5, start=0, end=-1, step=1, bsize=4096, path='trajectory/vel'):
        self.f, self.do_close = get_hdf5_file(fn_hdf5)
        self.start, self.end, self.step = get_slice(self.f, start, end, step=step)
        self.bsize = bsize
        self.path = path
        self.online = self.f is None or path not in self.f
        if not self.online:
            self.compute_offline()
            if self.do_close:
                self.f.close()

    def compute_offline(self):
        current = self.start
        stride = self.step*self.bsize
        work = np.zeros(self.bsize, float)
        ssize = self.bsize/2+1
        self.amps = np.zeros(ssize, float)
        ds = self.f[self.path]
        while current < self.end - stride:
            for indexes in np.ndindex(ds.shape[1:]):
                ds.read_direct(work, (slice(current, current+stride, self.step),) + indexes)
                self.amps += abs(np.fft.rfft(work))**2
            current += stride
        timestep = self.f['trajectory/time'][self.step] - self.f['trajectory/time'][0]
        self.freqs = np.arange(ssize)/(timestep*ssize)
        self.ac = np.fft.irfft(self.amps)[:ssize]
        self.time = np.arange(ssize)*timestep

    def plot(self, fn_png='spectrum.png', do_wavenum=True):
        import matplotlib.pyplot as pt
        if do_wavenum:
            xunit = lightspeed/centimeter
            xlabel = 'Wavenumber [1/cm]'
        else:
            xunit = 1/log.time
            xlabel = 'Frequency [1/%s]' % log.unitsys.time[1]
        pt.clf()
        pt.plot(self.freqs/xunit, self.amps)
        pt.xlim(0, self.freqs[-1]/xunit)
        pt.xlabel(xlabel)
        pt.ylabel('Amplitude')
        pt.savefig(fn_png)

    def plot_ac(self, fn_png='ac.png'):
        import matplotlib.pyplot as pt
        pt.clf()
        pt.plot(self.time/log.time, self.ac/self.ac[0])
        pt.xlabel('Time [%s]' % log.unitsys.time[1])
        pt.ylabel('Autocorrelation')
        pt.savefig(fn_png)
