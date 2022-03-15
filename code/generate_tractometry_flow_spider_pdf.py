#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fpdf import FPDF
import sys
import os


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


html_info = parse_report('report.html')
METHODS = """This pipeline allows you to extract tractometry information by combining subjects' 
WM bundles and diffusion MRI metrics. There is two way the tractometry informatin is computed:
- Average metric inside of a WM bundle volume (voxels occupied by at least one streamline)
- Average metric inside of a subsection of WM bundle volume (voxels occupied by at least one streamline)

The second method 'cut' the bundle in section so variation can be observed along the length. The exact steps are described in [1]. This approach is similar to what is presented in [1,2].
All reported metrics are weighted by streamline density, this way the values of the core/center of bundles are more represented than spurious streamlines and outliers.

Bundle_Metrics_Stats_In_Endpoints/ contains maps for each bundle where the average value along a streamlines are projected to the last points for cortical projection visualisation or statistics.

To fully QA the data, we recommand to download the labels map TRK file and inspect them in MI-Brain (https://www.imeka.ca/mi-brain/) 
"""

REFERENCES = """[1] Cousineau, Martin, et al. "A test-retest study on Parkinson's PPMI dataset yields statistically significant white matter fascicles. "NeuroImage: Clinical 16, 222-233 (2017) doi:10.1016/j.nicl.2017.07.020
[2] Yeatman, Jason D., et al. "Tract profiles of white matter properties: automating fiber-tract quantification." PloS one 7.11 (2012): e49790.
[3] Chandio, Bramsh Qamar, et al. "Bundle analytics, a computational framework for investigating the shapes and profiles of brain pathways across populations." Scientific reports 10.1 (2020): 1-18.
"""

pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.titles('Tractometry_Flow_V1: {}'.format(sys.argv[1]))
pdf.add_cell_left('Status:', html_info[0], size_y=5)
pdf.add_cell_left('Started on:', html_info[1], size_y=5)
pdf.add_cell_left('Completed on:', html_info[2], size_y=5)
pdf.add_cell_left('Command:', html_info[3], size_y=5)
pdf.add_cell_left('Duration:', html_info[4], size_y=5)

pdf.add_cell_left('Methods:', METHODS, size_y=5)
pdf.add_cell_left('References:', REFERENCES, size_y=5)

pdf.add_page()
pdf.titles('Tractometry_Flow_V1: {}'.format(sys.argv[1]))
pdf.add_mosaic('FA plot along bundle ({})'.format(sys.argv[2]),
               ['', ''],
               ['tmp_dict/CC_Fr_2_fa_metric.png'.format(sys.argv[1]),
                'tmp_dict/CC_Pr_Po_fa_metric.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=80, size_y=70)
pdf.add_mosaic('FA plot along bundle ({})'.format(sys.argv[2]),
               ['', ''],
               ['tmp_dict/AF_L_fa_metric.png'.format(sys.argv[1]),
                'tmp_dict/AF_R_fa_metric.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=80, size_y=70)
pdf.add_mosaic('FA plot along bundle ({})'.format(sys.argv[2]),
               ['', ''],
               ['tmp_dict/PYT_L_fa_metric.png'.format(sys.argv[1]),
                'tmp_dict/PYT_R_fa_metric.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=80, size_y=70)

pdf.add_page()
pdf.titles('Tractometry_Flow_V1: {}'.format(sys.argv[1]))
pdf.add_mosaic('Labels map ({})'.format(sys.argv[2]),
               ['CC_Fr_2, coronal', 'CC_Pr_Po, coronal'],
               ['CC_Fr_2/coronal_3d.png'.format(sys.argv[1]),
                'CC_Pr_Po/coronal_3d.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=80, size_y=55)
pdf.add_mosaic('Labels map ({})'.format(sys.argv[2]),
               ['AF_L, sagittal', 'AF_R, sagittal'],
               ['AF_L/sagittal_3d.png'.format(sys.argv[1]),
                'AF_R/sagittal_3d.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=80, size_y=55)
pdf.add_mosaic('Labels map ({})'.format(sys.argv[2]),
               ['PYT_L, sagittal', 'PYT_R, sagittal'],
               ['PYT_L/coronal_3d.png'.format(sys.argv[1]),
                'PYT_R/coronal_3d.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=80, size_y=55)
pdf.output('report.pdf', 'F')
