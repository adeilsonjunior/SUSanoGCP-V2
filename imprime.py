# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 17:08:25 2023

@author: Osvaldo
"""
from reportlab.platypus import Frame
from reportlab.lib.pagesizes import A4, landscape

padding = dict(
  leftPadding=72, 
  rightPadding=72,
  topPadding=72,
  bottomPadding=18)

portrait_frame = Frame(0, 0, *A4, **padding)

def on_page(canvas, doc, pagesize=A4):
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(pagesize[0]/2, 50, str(page_num))
    canvas.drawImage('https://www.python.org/static/community_logos/python-logo.png', 0, 0)

def on_page_landscape(canvas, doc):
  return on_page(canvas, doc, pagesize=landscape(A4))

from reportlab.platypus import PageTemplate

portrait_template = PageTemplate(
  id='portrait', 
  frames=portrait_frame,
  onPage=on_page, 
  pagesize=A4)

from reportlab.platypus import BaseDocTemplate

doc = BaseDocTemplate(
  'report.pdf',
  pageTemplates=[
    portrait_template
  ]
)

from dados import dg, dados_sessão
from relatorio_EMA import gera_relatório_EMA
from graficos_EMA import gera_gráficos_EMA
from plotly.io import write_image

import io

CNES = '6817866'; IBGE = '160030'; forma = '040505-A'

ds = dados_sessão(dg, CNES, IBGE, forma)

relatórios = gera_relatório_EMA(dg, ds)

gráficos = gera_gráficos_EMA(dg, ds)

print(type(relatórios['alvo']))
print(type(gráficos['evolução']))


from reportlab.platypus import Image
from reportlab.lib.units import inch
def fig2image(f):
    buf = io.BytesIO()
    gráficos['evolução'].write_image(buf, format='png',width=1000, height=350)
    # x, y = f.get_size_inches()
    return Image(buf, 300, 200)

from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()
from reportlab.platypus import Table, Paragraph
from reportlab.lib import colors
story = [
  Paragraph('SUSano', styles['Heading1']),
  Paragraph('Evolução mensal', styles['Heading2']),
  fig2image(gráficos['evolução']),
  Paragraph('Pairwise Correlation', styles['Heading2']),
]

doc.build(story)