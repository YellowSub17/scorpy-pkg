

import cairo
import numpy as np
import h5py

import matplotlib.pyplot as plt





ny = 1062
nx = 1028


def fake_shot(fname):

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, ny, nx)
    ctx = cairo.Context(surface)

    ctx.scale(ny, nx)


    ctx.rectangle(0,0,1,1)
    ctx.set_source_rgba(0,0,0,1)
    ctx.fill()

    rs = [0.1, 0.11, 0.2, 0.22, 0.3, 0.4, 0.35]
    for _ in range(230):

        r = np.random.choice(rs)
        th0 = 2*np.pi*np.random.random()
        dth = (1/16)*(np.pi*r)*np.random.random()

        ctx.arc(0.5, 0.5, r, th0, th0+dth)

        ctx.set_source_rgba(1,1,1,1)

        ctx.set_line_width(0.005)
        ctx.stroke()

    ctx.rectangle(0.1, 0.1, 0.2, 0.2)
    ctx.stroke()

    # surface.write_to_png(fname)

    buf = surface.get_data()

    shot = np.ndarray(shape=(nx, ny), dtype=np.uint32, buffer=buf)

    shot = shot & 255

    return shot/255






def make_h5(nshots = 10):


    shots = np.zeros( (nshots, nx, ny))

    for i in range(10):
        shot = fake_shot(f'fake-shot{i}.png')

        shots[i,...] = shot


    f = h5py.File('x_x_20583_data_000002.h5', 'w')

    grp = f.create_group('entry')
    grp = grp.create_group('data')


    dset = grp.create_dataset('data', data = shots)

    f.close()


make_h5()





