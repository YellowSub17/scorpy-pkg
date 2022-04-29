#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')








a = scorpy.AlgoHandler('agno3-random-starts')
a.save_rfs('a', verbose=99)

a = scorpy.AlgoHandler('agno3-nl180')
a.save_rfs('a', verbose=99)


# sub_tags = ['ER120', 'HIO10ER10', 'HIO20ER20', 'HIO30ER30', 'HIO60ER60', 'HIO120', 'HIO120beta']
# counts = [i for i in range(121)]



# for sub_tag in sub_tags:

    # a.run_shelx(sub_tag)
    # a.run_shelx(sub_tag, count='targ')

    # for count in counts:
        # print(sub_tag, count)
        # a.run_shelx(sub_tag, count=count)




# for sub_tag in sub_tags:

    # a.save_rfs(sub_tag, verbose=99)





