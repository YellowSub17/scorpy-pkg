
import scorpy
import shutil
import os





# sample = 'u-chalco'

# samples = ['u-chalco', 'garnet', 'bfbtpp-ni', 'bbceap-ag', 'tbcampmamp']
samples = ['agno3-d05', 'agno3-d03']



for sample in samples:

#open atomic cif
    cif = scorpy.CifData(f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif', atomic=True)
#fill from the structure factors from vesta (.vhkl)
    cif.fill_from_vhkl(f'{scorpy.DATADIR}/xtal/{sample}/{sample}.vhkl', fill_peaks=False)
#save the strcutre factor cif file
    cif.save(f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif')
    print(f'{sample} qmax:', cif.qmax)



    shutil.copyfile(f'{scorpy.DATADIR}/xtal/{sample}/{sample}.vins', f'{scorpy.DATADIR}/xtal/{sample}/{sample}.ins')


    os.system(f"sed -i 's/L\\.S\\. 5/L\\.S\\. 20/' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/FMAP/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/PLAN/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/WPDB/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/^H[1234567890]/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/BOND/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/CONF/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/TEMP/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")
    os.system(f"sed -i '/SIZE/d' {scorpy.DATADIR}/xtal/{sample}/{sample}.ins ")








