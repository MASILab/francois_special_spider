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
METHODS = """Connectoflow [1] is Nextflow [2] pipeline to generate Connectomics [3,4] matrices from tractography data.
The key steps in this version of Connectoflow are:
- Decompose: This step performs the parcel-to-parcel decomposition of the tractogram. It includes streamline-cutting
    operations to ensure streamlines have terminations in the provided atlas. Moreover, connection-wise cleaning processes
    that remove loops, discard spurious streamlines and discard incoherent curvatures are used to remove as many false
    positives as possible [5].
- COMMIT: To further decrease the number of invalid streamlines and assign a quantitative weight to each streamline,
    Convex Optimization Modeling for Micro-structure Informed Tractography (COMMIT) [6,7] is used. This not only allows the
    removal of aberrant or spurious streamlines, but it was shown to increase reproducibility of connectivity measures by
    being more robust to various tractography biases. 
- AFD: Apparent Fiber Density (AFD) [8,9] is subsequently computed connection-wise using streamline orientations
    (fixel), which can be computationally burdensome if done on every pairwise connection of the connectome a posteriori.
    This step will provide a AFD-weighted connectivity matrix.
"""

REFERENCES = """[1] Rheault, Francois, et al. "Connectoflow: A cutting-edge Nextflow pipeline for structural connectomics",
    ISMRM 2021 Proceedings, #710.
[2] Di Tommaso, Paolo, et al. "Nextflow enables reproducible computational workflows.", Nature biotechnology 35.4 (2017): 316-319.
[3] Sotiropoulos, Stamatios N., and Andrew Zalesky. "Building connectomes using diffusion MRI: why, how and but.",
    NMR in Biomedicine 32.4 (2019): e3752.
[4] Yeh, Chun-Hung, et al. "Mapping structural connectivity using diffusion MRI: challenges and opportunities.",
    Journal of Magnetic Resonance Imaging (2020).
[5] Zhang, Zhengwu, et al. "Mapping population-based structural connectomes.", NeuroImage 172 (2018): 130-145.
[6] Daducci, Alessandro, et al. "COMMIT: convex optimization modeling for microstructure informed tractography.",
    IEEE transactions on medical imaging 34.1 (2014): 246-257.
[7] Schiavi, Simona, et al. "A new method for accurate in vivo mapping of human brain connections using microstructural,
    and anatomical information." Science advances 6.31 (2020): eaba8245.
[8] Raffelt, David A., et al. "Investigating white matter fibre density and morphology using fixel-based analysis.",
    Neuroimage 144 (2017): 58-73.
[9] Dhollander, Thijs, et al. "Fixel-based Analysis of Diffusion MRI: Methods, Applications, Challenges and
    Opportunities." (2020).
"""

pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.titles('Connectoflow_V1: {}'.format(sys.argv[1]))
pdf.add_cell_left('Status:', html_info[0], size_y=5)
pdf.add_cell_left('Started on:', html_info[1], size_y=5)
pdf.add_cell_left('Completed on:', html_info[2], size_y=5)
pdf.add_cell_left('Command:', html_info[3], size_y=5)
pdf.add_cell_left('Duration:', html_info[4], size_y=5)

pdf.add_cell_left('Methods:', METHODS, size_y=5)
pdf.add_cell_left('References:', REFERENCES, size_y=5)

pdf.add_page()
pdf.titles('Connectoflow_V1: {}'.format(sys.argv[1]))
pdf.add_mosaic('Matrices',
               ['streamlines count weighted', 'volume weighted'],
               ['results_conn/{}/Visualize_Connectivity/sc_matrix.png'.format(sys.argv[1]),
                'results_conn/{}/Visualize_Connectivity/vol_matrix.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=65, size_y=65)
pdf.add_mosaic('',
               ['length weighted', 'FA weighted'],
               ['results_conn/{}/Visualize_Connectivity/len_matrix.png'.format(sys.argv[1]),
                'results_conn/{}/Visualize_Connectivity/fa_matrix.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=65, size_y=65)
pdf.add_mosaic('',
               ['COMMIT weighted', 'AFD weighted'],
               ['results_conn/{}/Visualize_Connectivity/commit2_weights_matrix.png'.format(sys.argv[1]),
                'results_conn/{}/Visualize_Connectivity/afd_fixel_matrix.png'.format(sys.argv[1])],
               col=2, pos_x=20, size_x=65, size_y=65)
pdf.output('report.pdf', 'F')
