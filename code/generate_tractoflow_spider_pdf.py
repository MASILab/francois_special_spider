#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fpdf import FPDF
import sys
import os
import nibabel as nib


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
                self.set_font('Arial', '', 8)
                self.multi_cell(size_x, 5, align='C', txt=titles[j+col*i])
                self.image(filenames[j+col*i],
                           x=pos[0]+size_x*j, y=pos[1]+10+size_y*i,
                           w=size_x, h=size_y, type='PNG')
        self.set_y(pos[1]+(size_y*row)+10)


html_info = parse_report('report.html')
METHODS = """TractoFlow [1] pipeline is developed by the Sherbrooke Connectivity Imaging Lab (SCIL) in order to process
diffusion MRI dataset from the raw data to the tractography. The pipeline is based on Nextflow [2].

This pipeline is optimized for healthy human adults.

TractoFlow pipeline consist of 23 different steps : 14 steps for the diffusion weighted image (DWI) processing and 8
steps for the T1 weighted image processing.
See https://tractoflow-documentation.readthedocs.io/en/latest/index.html and [1] for more details.
"""

REFERENCES = """[1] Theaud, G., Houde, J.-C., Boré, A., Rheault, F., Morency, F., Descoteaux, M.,
    "TractoFlow: A robust, efficient and reproducible diffusion MRI pipeline leveraging Nextflow & Singularity",
    NeuroImage (2020).
[2] Paolo Di Tommaso, et al. "Nextflow enables reproducible computational workflows.", Nature Biotechnology 35, 316-319
    (2017)
[3] Garyfallidis, E., Brett, M., Amirbekian, B., Rokem, A., Van Der Walt, S., Descoteaux, M., Nimmo-Smith, I.,
    "Dipy, a library for the analysis of diffusion mri data.", Frontiers in neuroinformatics (2014) 8, 8.
[4] Tournier, J. D., Smith, R. E., Raffelt, D. A., Tabbara, R., Dhollander, T., Pietsch, M., & Connelly, A.,
    "MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation.",
    Neuroimage (2020).
[5] Avants, B.B., Tustison, N., Song, G., "Advanced normalization tools (ants)." Insight J (2009) 2, 1-35.
[6] Jenkinson, M., Beckmann, C.F., Behrens, T.E., Woolrich, M.W., Smith, S.M., "Fsl." Neuroimage 62 (2012), 782-790.
"""

pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.titles('Tractoflow_V1: {}'.format(sys.argv[1]))
pdf.add_cell_left('Status:', html_info[0], size_y=5)
pdf.add_cell_left('Started on:', html_info[1], size_y=5)
pdf.add_cell_left('Completed on:', html_info[2], size_y=5)
pdf.add_cell_left('Command:', html_info[3], size_y=5)
pdf.add_cell_left('Duration:', html_info[4], size_y=5)

pdf.add_cell_left('Methods:', METHODS, size_y=5)
pdf.add_cell_left('References:', REFERENCES, size_y=5)

if (os.path.isfile('local.png') and os.path.isfile('pft.png')) or \
        (os.path.isfile('axial.png') and os.path.isfile('coronal.png')):
    pdf.add_page()
    pdf.titles('Tractoflow_V1: {}'.format(sys.argv[1]))
    if os.path.isfile('local.png') and os.path.isfile('pft.png'):
        in_local = nib.streamlines.load(
            '{}__local.trk'.format(sys.argv[1]), lazy_load=True)
        in_pft = nib.streamlines.load(
            '{}__pft.trk'.format(sys.argv[1]), lazy_load=True)
        pdf.add_mosaic('Whole Brain Tractography',
                       ['Local Tracking: {}'.format(in_local.header['nb_streamlines']),
                        'PFT Tracking: {}'.format(in_pft.header['nb_streamlines'])],
                       ['local.png', 'pft.png'],
                       size_x=40, size_y=220, row=1, col=2, pos_x=10, pos_y=40)
    if os.path.isfile('axial.png') and os.path.isfile('coronal.png'):
        pdf.add_image('FODF axial', 'axial.png', size_x=100, size_y=100,
                      pos_x=100, pos_y=40)
        pdf.add_image('FODF coronal', 'coronal.png', size_x=100, size_y=100,
                      pos_x=100, pos_y=150)
pdf.output('report.pdf', 'F')
