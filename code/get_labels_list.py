#!/usr/bin/env python

import sys

import numpy as np
import nibabel as nib
from scilpy.io.image import get_data_as_label

img_labels = nib.load(sys.argv[1])
data_labels = get_data_as_label(img_labels)
real_labels = np.unique(data_labels)[1:]
np.savetxt(sys.argv[2], real_labels, fmt='%i')