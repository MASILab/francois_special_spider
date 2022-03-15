#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fpdf import FPDF
import sys
import os
import imageio


def parse_report(filename):
    f = open(filename, "r")

    lines = f.readlines()
    final = []
    for i, line in enumerate(lines):
        if 'Run times' in line:
            tmp_1, tmp_2 = lines[i+2].split(' - ')
            tmp_1 = tmp_1.replace('<span id="workflow_start">', '')
            tmp_1 = tmp_1.replace('</span>', '').strip()
            tmp_2 = tmp_2.replace('<span id="workflow_complete">', '')
            tmp_2 = tmp_2.replace('</span>', '').strip()
            final.append(tmp_1)
            final.append(tmp_2)
        elif 'CPU-Hours' in line:
            tmp = lines[i+1].replace('<dd class="col-sm-9"><samp>', '')
            tmp = tmp.replace('</samp></dd>', '').strip()
            final.append(tmp+' hours')
        elif 'Nextflow command' in line:
            tmp = lines[i+1].replace('<dd><pre class="nfcommand"><code>', '')
            tmp = tmp.replace('</code></pre></dd>', '').strip()
            final.append(tmp)
        elif 'Workflow execution' in line:
            tmp = lines[i].strip().replace('</h4>', '')
            tmp = tmp.replace('<h4>', '')
            final.append(tmp)

    return final


class PDF(FPDF):
    def titles(self, title, width=210, pos_x=0, pos_y=0):
        self.set_xy(pos_x, pos_y)
        self.set_font('Arial', 'B', 16)
        self.multi_cell(w=width, h=20.0, align='C', txt=title,
                        border=0)

    def add_cell_left(self, title, text, size_y=10, width=200):
        self.set_xy(5.0, self.get_y() + 4)
        self.set_font('Arial', 'B', 12)
        self.multi_cell(width, 5, align='L', txt=title)
        self.set_xy(5.0, self.get_y())
        self.set_font('Arial', '', 10)
        self.multi_cell(width, size_y, align='L', txt=text, border=1)

    def init_pos(self, pos_x=None, pos_y=None):
        pos = [0, 0]
        pos[0] = pos_x if pos_x is not None else 10
        pos[1] = pos_y if pos_y is not None else self.get_y()+10
        return pos

    def add_image(self, title, filename, size_x=75, size_y=75,
                  pos_x=None, pos_y=None):
        pos = self.init_pos(pos_x, pos_y)
        self.set_xy(pos[0], pos[1])
        self.set_font('Arial', 'B', 12)
        self.multi_cell(size_x, 5, align='C', txt=title)
        self.image(filename, x=pos[0], y=pos[1]+5,
                   w=size_x, h=size_y, type='PNG')
        self.set_y(pos[1]+size_y+10)

    def add_mosaic(self, main_tile, titles, filenames, size_x=75, size_y=75,
                   row=1, col=1, pos_x=None, pos_y=None):
        pos = self.init_pos(pos_x, pos_y)
        self.set_xy(pos[0], pos[1])
        self.set_font('Arial', 'B', 12)
        self.multi_cell(size_x*col, 5, align='C', txt=main_tile)

        for i in range(row):
            for j in range(col):
                self.set_xy(pos[0]+size_x*j, pos[1]+5+size_y*i)
                self.set_font('Arial', '', 10)
                self.multi_cell(size_x, 5, align='C', txt=titles[j+col*i])
                self.image(filenames[j+col*i],
                           x=pos[0]+size_x*j, y=pos[1]+10+size_y*i,
                           w=size_x, h=size_y, type='PNG')
        self.set_y(pos[1]+(size_y*row)+10)


def estimate_size(filename):
    arr = imageio.imread(filename)
    ratio = arr.shape[0] / arr.shape[1]
    if ratio < 0.75:
        max_x = min(90 / ratio, 180)
        return max_x, max_x * ratio
    else:
        max_y = min(180 * ratio, 90)
        return max_y / ratio, max_y


html_info = parse_report('report.html')
METHODS = """RecobundlesX is a multi-atlas, multi-parameters version of Recobundles [1].
It is optimized for whole brain coverage using 39 major
well-known white matter pathways. The atlas is a customized population average
from 20 UKBioBank [2] and 20 Human Connectome Project [3] datasets co-registered
to MNI152 space.

This atlas was made to cover as much spatial extend as possible and explore as
much shape variability as possible. Recobundles is then run 27 times with
bundle-specific paramters and the results of each execution are used in
a majority-vote approach. This is inspired from the state-of-the-art in medical
images segmentation (before machine-learning) [4,5].

Then, a shape-based pruning is applied to each bundle to remove inconsistent or
spurious streamlines (outliers) [6].
"""

REFERENCES = """ [1] Garyfallidis, Eleftherios, et al. "Recognition of white matter bundles using local and global
    streamline-based registration and clustering." NeuroImage 170 (2018): 283-295.
[2] Sudlow, Cathie, et al. "UK biobank: an open access resource for identifying the causes of a wide range of complex
    diseases of middle and old age." Plos med 12.3 (2015): e1001779.
[3] Van Essen, David C., et al. "The WU-Minn human connectome project: an overview." Neuroimage 80 (2013): 62-79.
[4] Iglesias, Juan Eugenio, and Mert R. Sabuncu. "Multi-atlas segmentation of biomedical images: a survey."
    Medical image analysis 24.1 (2015): 205-219.
[5] Pipitone, Jon, et al. "Multi-atlas segmentation of the whole hippocampus and subfields using multiple automatically
    generated templates." Neuroimage 101 (2014): 494-512.
[6] Côté, Marc-Alexandre, et al. "Cleaning up the mess: tractography outlier removal using hierarchical QuickBundles
    clustering." 23rd ISMRM annual meeting. Toronto, Canada. 2015.
"""

pdf = PDF(unit='mm', format='A4')
pdf.add_page()
pdf.titles('RBx_flow_V1: {}'.format(sys.argv[1]))
pdf.add_cell_left('Status:', html_info[0], size_y=5)
pdf.add_cell_left('Started on:', html_info[1], size_y=5)
pdf.add_cell_left('Completed on:', html_info[2], size_y=5)
pdf.add_cell_left('Command:', html_info[3], size_y=5)
pdf.add_cell_left('Duration:', html_info[4], size_y=5)

pdf.add_cell_left('Methods:', METHODS, size_y=5)

pdf.add_page()
pdf.titles('RBx_flow_V1: {}'.format(sys.argv[1]))
pdf.add_cell_left('References:', REFERENCES, size_y=5)
tmp_x, tmp_y = estimate_size('left.png')
pdf.add_image('Left hemisphere', 'left.png',
              size_x=tmp_x, size_y=tmp_y, pos_x=10)

pdf.add_page()
pdf.titles('RBx_flow_V1: {}'.format(sys.argv[1]))
tmp_x, tmp_y = estimate_size('right.png')
pdf.add_image('Right hemisphere', 'right.png',
              size_x=tmp_x, size_y=tmp_y, pos_x=10)
tmp_x, tmp_y = estimate_size('comm.png')
pdf.add_image('Commisures++', 'comm.png', size_x=tmp_x, size_y=tmp_y, pos_x=10)

pdf.output('report.pdf', 'F')
