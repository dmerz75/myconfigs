#!/bin/bash
# call_write_coords()
# compute_tension()
# compute_chi()
# compute_hsa()
# compute_contacts()
# compute_new_contacts()
# compute_bond_vector_angle()
# compute_csu()
# compute_proto()
# compute_mtcon()
# --------------------  THE TYPES  ------------------------------------------
# debug
# coords, tension, chi, hsa, contacts, new_contacts, bond_vector_angle, csu, proto, mtcon
# definitions:
RUN=./run_tch.py
load_sbd () {
    # contacts_map_new/pdbref.ent -> /home/dale/sop_dev/molecules/hsp70/pdb2khosbd_CA.ent
    PSF=/home/dale/ext/completed_sbd/gsop/sbd_gsop.psf
    DCD=/home/dale/ext/completed_sbd/gsop/11_ab180_nopep_2400/ab180_nopep__2khosbd__1/dcd/2khosbd_D30_pull.dcd
    SEL="resid 383:603"
    F1=0
    F2=10002
    STEP=10
    CHAINS=1
    CHAINS_IGNORE=0
    R1=383
    R2=603
    SEED=1
}
load_sbdpep () {
    # contacts_map_new/pdbref.ent -> /home/dale/sop_dev/molecules/hsp70/sbdpeptide/sbd_DH_calphaonly.pdb
    PSF=/home/dale/sop_dev/molecules/hsp70/sbdpeptide/psf/2khosbdpep.ref.pdb.psf
    DCD=/home/dale/ext/completed_sbd/gsop_pep/3_b135_158_a180/b135_158_a180_pep__2khosbdpep__139_4900601__08-16-2015_0101-0/dcd/2khosbdpep_D30_pull.dcd
    SEL="resid 1:7 and resid 389:604"
    F1=1
    F2=15002
    STEP=15
    CHAINS=2
    CHAINS_IGNORE=1
    R1=389
    R2=604
    SEED=0
}
run_echo () {
    echo $PSF
    echo $DCD
    echo selection $SEL
    echo start,stop,step $F1 $F2 $STEP
    echo chains,chains_ignore $CHAINS $CHAINS_IGNORE
    echo residues $R1 $R2
    echo seed $SEED
}
general () {
    $RUN -o $1 -seed $SEED -t sbd -p sbd -r1 $2 -r2 $3 \
         -f1 $F1 -f2 $F2 -c $CHAINS -i $CHAINS_IGNORE -step $STEP \
         -psf $PSF -dcd $DCD -sel $SEL
}
# <<<___start here___>>>
# hsa
# general hsa 389 604
# general hsa 389 502
# general hsa 510 604
# tension, contacts
# general tension 389 604
# general new_contacts 389 604
# going to perform, tension|costheta|contacts
# ./run_segment_contact nbd_ref.pdb nbd_1.pdb 1 0
# examples ^
# general hsa $R1 $R2
# load_sbdpep
load_sbd

run_echo

general new_contacts $R1 $R2










# test1
# hsa - pass1
# tension - pass1
# ./run_tch.py -o clean

# | 5.alpha158         |  153 | *   | *     | *v    |         |     |     | (1279)-1370   | 2240-(2260)-2280 | (4220)-4310-4395 | (5650)-5695-5730 |                |    |
# segments = [(383,398),(399,460),(461,501),(502,531),(532,597)] - new proposed, (598-603) excluded;


# new_contacts
# ./run_tch.py -o new_contacts -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 1 -f2 2000 -step 10 -psf $HOME/ext/completed_sbd/gsop/sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o new_contacts -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 1 -f2 2000 -step 10 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# cd $HOME/ext/completed_sbd/gsop/5_alpha158/
# cd $HOME/ext/completed_sbd/gsop/5_alpha158/sbd_a158__2khosbd__153_1635976__01-26-2015_1834
# ./run_tch.py -o debug -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 1 -f2 2000 -step 10 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd



# round7-----------------1
# test hsa
# ./run_tch.py -o hsa -seed 153 -t sbd -p sbd -r1 394 -r2 502 -f1 1400 -f2 1420 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o hsa -seed 153 -t sbd -p sbd -r1 394 -r2 502 -f1 1500 -f2 1520 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# hsa
# ./run_tch.py -seed 280 -t sopnucleo -p 2KHO -r1 1 -r2 338 -f1 2500 -f2 3500 -step 10
# ./run_tch.py -o clean
# ./run_tch.py -o hsa -seed 153 -t sbd -p sbd -r1 394 -r2 502 -f1 1200 -f2 1600 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o hsa -seed 153 -t sbd -p sbd -r1 522 -r2 600 -f1 2120 -f2 2520 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o hsa -seed 153 -t sbd -p sbd -r1 394 -r2 492 -f1 4143 -f2 4543 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o hsa -seed 153 -t sbd -p sbd -r1 394 -r2 461 -f1 5525 -f2 5925 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd

# chi & tension---------------------------------------------
# test tension
# ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 100 -f2 220 -step 20 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# round7-----------------4
# tension - all residues. i.e. 383-603
# for frame in 5500 5600 5700 5800 5900 6000
# do
#     frame2=$(($frame + 100))
#     for option in tension chi
#     do
#         ./run_tch.py -o $option -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 1 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
#     done
# done
# # round7-----------------3
# # tension - all residues. i.e. 383-603
# for frame in 4000 4100 4200 4300 4400 4500
# do
#     frame2=$(($frame + 100))
#     for option in tension chi
#     do
#         ./run_tch.py -o $option -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 1 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
#     done
# done
# # round7-----------------2
# # tension - all residues. i.e. 383-603
# for frame in 2000 2100 2200 2300 2400 2500
# do
#     frame2=$(($frame + 100))
#     for option in tension chi
#     do
#         ./run_tch.py -o $option -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 1 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
#     done
# done
# round7-----------------1
# tension - all residues. i.e. 383-603
# for frame in 800 1000 1200 1400 1600
# do
#     frame2=$(($frame + 200))
#     for option in tension chi
#     do
#         ./run_tch.py -o $option -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
#     done
# done
# chi & tension---------------------------------------------



# # tension7--------------------------------------
# # round7-----------------4
# # tension - all residues. i.e. 383-603
# for frame in 5500 5600 5700 5800 5900 6000
# do
#     frame2=$(($frame + 100))
#     ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 1 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# done

# # round7-----------------3
# # tension - all residues. i.e. 383-603
# for frame in 4000 4100 4200 4300 4400 4500
# do
#     frame2=$(($frame + 100))
#     ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 1 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# done

# # round7-----------------2
# # tension - all residues. i.e. 383-603
# for frame in 2000 2100 2200 2300 2400 2500
# do
#     frame2=$(($frame + 100))
#     ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 1 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# done

# # round7-----------------1
# # tension - all residues. i.e. 383-603
# for frame in 800 1000 1200 1400 1600
#              # 1000 1100 1200 1300 1400
# do
#     frame2=$(($frame + 200))
#     ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# done
# # tension7--------------------------------------




# round6----------------- ! may work!
# tension - all residues. i.e. 383-603
# for frame in 900 1000 1100 1200 1300 1400
#              # 1000 1100 1200 1300 1400
# do
#     frame2=$(($frame + 100))
#     ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 1 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# done


# round3-----------------
# tension - all residues. i.e. 383-603
# for frame in 900 1000 1200 1400
# do
#     frame2=$(($frame + 200))
#     ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 $frame -f2 $frame2 -step 2 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# done


# ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 1100 -f2 1500 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 2100 -f2 2400 -step 3 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 4100 -f2 4500 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 5500 -f2 5900 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd


# # hsa - residue segments
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 1100 -f2 1500 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 2100 -f2 2400 -step 3 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 4100 -f2 4500 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 5500 -f2 5900 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# # chi - residue segments??
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 1100 -f2 1500 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 2100 -f2 2400 -step 3 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 4100 -f2 4500 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o chi -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 5500 -f2 5900 -step 4 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd





# unfolding2 use 1000,10
# ./run_hsa.py
# ./run_hsa.py -seed 280 -t sopnucleo -p 2KHO -r1 1 -r2 338 -f1 2500 -f2 3500 -step 10
# ./run_hsa.py -seed 280 -t sopnucleo -p 2KHO -r1 188 -r2 225 -f1 6700 -f2 7800 -step 10
# ./run_hsa.py -seed 280 -t sopnucleo -p 2KHO -r1 1 -r2 168 -f1 8500 -f2 9500 -step 10
# ./run_hsa.py -seed 280 -t sopnucleo -p 2KHO -r1 68 -r2 168 -f1 9900 -f2 10700 -step 10
# ./run_hsa.py -seed 280 -t sopnucleo -p 2KHO -r1 113 -r2 168 -f1 11200 -f2 12200 -step 10
# ./run_hsa.py -seed 280 -t sopnucleo -p 2KHO -r1 136 -r2 168 -f1 13800 -f2 15000 -step 10
# chi_gsop_frames_2700_2800_resids_1_39.dat
# chi_gsop_frames_2700_2800_resids_40_115.dat
# chi_gsop_frames_2700_2800_resids_116_169.dat
# chi_gsop_frames_2700_2800_resids_170_187.dat
# chi_gsop_frames_2700_2800_resids_188_340.dat
# chi_gsop_frames_2700_2800_resids_341_382.dat



# round2-----------------
# for option in tension chi
# do
#     ./run_tch.py -o $option -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 1000 -f2 1500 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
#     ./run_tch.py -o $option -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 1500 -f2 2000 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
#     ./run_tch.py -o $option -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 2000 -f2 2500 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
#     ./run_tch.py -o $option -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 2500 -f2 3000 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# done
# ./run_tch.py -o hsa -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 1000 -f2 1500 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o hsa -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 1500 -f2 2000 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o hsa -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 2000 -f2 2500 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o hsa -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 2500 -f2 3000 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd



# round1-----------------
# tension
# ./run_tch.py -o clean
# ./run_tch.py -o tension -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 1000 -f2 1500 -step 100 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 2000 -f2 2500 -step 75 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# ./run_tch.py -o tension -seed 153 -t sbd -p sbd -r1 383 -r2 603 -f1 2600 -f2 2900 -step 50 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# chi
# ./run_tch.py -o chi -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 1000 -f2 1500 -step 100 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
# hsa
# ./run_tch.py -o tension -seed 153 -t sbd --pdb sbd -r1 383 -r2 603 -f1 1000 -f2 1500 -step 100 -psf ../../sbd_gsop.psf -dcd dcd/2khosbd_D30_pull.dcd
