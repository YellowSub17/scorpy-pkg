import scorpy






sphv1 = scorpy.SphericalVol(20, 18, 36, 1)



grid = sphv1.get_q_grid(0)
lats, lons = sphv1.get_angle_sampling()
