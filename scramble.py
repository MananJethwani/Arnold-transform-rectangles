#!/usr/bin/env python3

import numpy as np
import math, time, sys, random
from PIL import Image
from arnold import Arnold

def main(argv):
    image_name = "madara-modified.gif"
    image_path = "images/" + image_name

    # Arnold Transform Parameters
    a = 6
    b = 40
    rounds = 33

    # Open the images
    madara = np.array(Image.open(image_path).convert("L"))

    print(" ~~~~~~  * PARAMETERS *  ~~~~~~ ")
    arnold = Arnold(a, b, rounds)
    print("\ta:\t", a)
    print("\tb:\t", b)
    print("\trounds:\t", rounds)

    print("\n ~~~~~~  *  RESULTS   *  ~~~~~~ ")
    
    n,m = madara.shape
    cpy = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            cpy[i][j] = madara[i][j]

    len = m
    # setting regions where first 2 regions are already decided
    size = random.randrange(3, 10)
    regions = np.zeros((size, 3))
    regions[0] = [0, 0, len]
    regions[1] = [n-m, 0, len]
    for i in range(2, size):
        L = int(random.randrange(1, len-10))
        regions[i] = [int(random.randrange(0, n-L)), int(random.randrange(0, m-L)), L]

    for i in range(size-1, -1, -1):
        x, y, L = regions[i].astype(int)
        arr = np.zeros((L,L))
        for i in range(L):
            for j in range(L):
                arr[i,j] = madara[x+i,y+j]
    
        scrambled = arnold.applyTransformTo(arr)

        for i in range(L):
            for j in range(L):
                madara[x+i,y+j] = scrambled[i,j]

    im = Image.fromarray(madara).convert("L")
    im.save("madara-scrambled.tif", format="TIFF")

    x1 = 500
    y1 = 500

    for i in range(100, x1):
        for j in range(100, y1):
            madara[i,j] = 0

    im = Image.fromarray(madara).convert("L")
    im.save("madara-shear.tif", format="TIFF")
    # re-construct
    
    for i in range(size):
        x, y, L = regions[i].astype(int)
        arr = np.zeros((L,L))

        for i in range(L):
            for j in range(L):
                arr[i,j] = madara[x+i,y+j]
        
        scrambled = arnold.applyInverseTransformTo(arr)

        for i in range(L):
            for j in range(L):
                madara[x+i,y+j] = scrambled[i,j]


    im = Image.fromarray(madara).convert("L")
    im.save("reconstructed.tif", format="TIFF")

    print("\n percentage of sheer cut-out: ", (x1-100)*(y1-100)/(1.0*n*m)*100,"%")

if __name__ == "__main__":
    main(sys.argv[1:])