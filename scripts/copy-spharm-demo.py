




import scorpy
import numpy as np
np.random.seed(1)

# First we make a spherical intensity space...
iv = scorpy.SphInten(100,2**5, 1)
# ...and fill it with random values.
iv.ivol = np.random.randn(*iv.ivol.shape)



# Next we create a sphharmhandler object...
sph = scorpy.SphHarmHandler(100, 11, 1)
# ...and fill it with values from the random spherical intensity space
sph.fill_from_ivol(iv)


# We can make copies of both objects.
sph2 = sph.copy()
iv2 = iv.copy()

# To show they are different objects:
print('\n\nTo show copied objects are different:')
print(f'sph=\t{sph}')
print(f'sph2=\t{sph2}')
print(f'iv=\t{iv}')
print(f'iv2=\t{iv2}')


# When we apply methods to these objects, they return modify self and return self.
u = np.abs(np.random.randn(sph.nq, sph.nq, sph.nl))
l = np.abs(np.random.randn(sph.nq, sph.nl))


print('\n\nTo show method modifies self:')
print(f'sph[0][0] value before method: {sph.vals_lnm[0][0]}')
# Applying method
sph3 = sph.calc_klmn(u)
print(f'sph[0][0] value after method: {sph.vals_lnm[0][0]}')

print('\n\nTo show method returned self:')
print(f'sph=\t{sph}')
print(f'sph3=\t{sph3}')


# Because methods modify self, they don't need a varible defined to them.
# Because methods return self, they can be chained in sequence.

#same data, different objects
Idatasph = sph2.copy()
Ifiltsph = sph2.copy()

#chaining methods, modifying self
Idatasph.calc_klmn(u).calc_kprime(l).calc_Ilm_p(u)
Ifiltsph.calc_klmn(u).calc_Ilm_p(u)


#copy method can also be chained! Useful for probing inbetween steps.
Idatakprime = sph2.copy().calc_klmn(u).calc_kprime(l)

# ...probe Idatakprime values...

# Continue method chain
Idatakprime.calc_Ilm_p(u)

print('\n\nTo show chained methods and probed methods give the same result:')
print(f'chained[0][0]=\t{Idatasph.vals_lnm[0][0]}')
print(f'probed=\t\t{Idatakprime.vals_lnm[0][0]}')
















