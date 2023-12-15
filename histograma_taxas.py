# import dash_bootstrap_components as dbc
# from dash import dcc
from dash import html
# from dash.dependencies import Input, Output#, State

import numpy as np

from funcoes_de_apoio import wrap, f_int

import plotly.graph_objs as go

from scipy.stats import lognorm

# from dash_app import app

help_histograma_taxas = html.Div([
        "Este gráfico mostra o número de municípios brasileiros com taxas de atendimento ",
        "por habitante-SUS correspondente ao valor no eixo dos x. ",
        "As linhas verticais marcam as posições das taxas do município escolhido, ",
        "da capital e do estado, e também do Brasil. ",
        html.Br(),
        "A curva ", html.Em("Lognormal"), " (para vê-la é preciso clicar sobre a legenda) e a linha ", html.Em("Limiar log-normal "),
        "se referem à modelagem da distribuição de atendimentos e à taxa a partir da qual consideramos ter havido atendimentos em excesso. ",
        "Você pode ignorar essas informações mas se tiver interesse, veja a explicação na aba ",
        html.Em("SUSano"),
        ", seção ",
        html.Em("Metodologia"),
        "."
        ])

def remove_outliers(V):
    Q1 = np.quantile(V, 0.25)
    Q3 = np.quantile(V, 0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return [v for v in V if (v > lower) and (v < upper)]

def gera_histograma_taxas(dg, ds):
    
    # taxa_municipal_máxima_no_alvo = ds.df_M_Alvo_em_foco['Taxa_por_hab_SUS'].max()
    
    xmax = max([ds.taxa_anual_M_Res * ds.denominador_populacional,
                ds.taxa_anual_Br * ds.denominador_populacional,
                ds.taxa_anual_Capital * ds.denominador_populacional,
                ds.taxa_anual_UF * ds.denominador_populacional,
                ds.taxa_anual_limiar * ds.denominador_populacional])
    margin = xmax * 3/100
    
    df_M_Alvo_em_foco_qtd_maior_que_zero = ds.df_M_Alvo_em_foco[ds.df_M_Alvo_em_foco['Qtd_EMA'] >= 0]
    # Isso pode ser eliminado. Tal como está, é desnecessária a criação desse df
    
    taxas = df_M_Alvo_em_foco_qtd_maior_que_zero['Taxa_por_hab_SUS'].values * ds.denominador_populacional
    taxas_limpas = remove_outliers(taxas)
    
    N_BINS=400
    hist, bin_edges = np.histogram(taxas, bins=N_BINS)
    bin_width = (bin_edges[-1] - bin_edges[0]) / (len(bin_edges) - 1)
    
    xbins_dict = dict(start=str(bin_edges[0]), end=str(bin_edges[-1]), 
                      size=bin_width)
    
    try:
        shape, loc, scale = lognorm.fit(taxas_limpas)
    except Exception as error:
        print(f'>>>>>>>> Erro na lognorm.fit: {error}')
    valores_x = np.linspace(0, xmax + margin, 400)
    pdf_trace = go.Scatter(x=valores_x,
                           y=lognorm.pdf(valores_x, shape, loc, scale) * sum(hist) * bin_width,
                           name='Lognormal (escala histograma)',
                           mode='lines',
                           line=dict(color='black'),
                           visible='legendonly')
    
    max_count = max(hist)
    
    taxa_município_em_foco_trace = \
           go.Scatter(x=[ds.taxa_anual_M_Res * ds.denominador_populacional]*2,
                      y=[0, max_count],
                      name=wrap(f'Taxa em {ds.M_Res_em_foco}', 30),
                      mode='lines',
                      line = dict(width=2, dash='dashdot'),
                      hoverinfo='skip',
                      opacity=0.9)  
    
    taxa_BR_trace = go.Scatter(x = [ds.taxa_anual_Br * ds.denominador_populacional]*2,
                               y = [0, max_count],
                               name=wrap('Taxa Brasil', 30),
                               mode='lines',
                               line = dict(width=2, dash='dashdot'),
                               hoverinfo='skip',
                               opacity=0.9)
    
    taxa_capital_trace = go.Scatter(x = [ds.taxa_anual_Capital * ds.denominador_populacional]*2,
                           y = [0, max_count],
                           name=wrap(f'Taxa {ds.Capital_em_foco}', 30),
                           mode='lines',
                           line = dict(width=2, dash='dashdot'),
                           hoverinfo='skip',
                           opacity=0.9)
    
    taxa_UF_trace = go.Scatter(x = [ds.taxa_anual_UF * ds.denominador_populacional]*2,
                           y = [0, max_count],
                           name=wrap(f'Taxa {ds.UF_M_Res_em_foco}', 30),
                           mode='lines',
                           line = dict(width=2, dash='dashdot'),
                           hoverinfo='skip',
                           opacity=0.9)
    
    taxa_limiar_trace = go.Scatter(x=[ds.taxa_anual_limiar * ds.denominador_populacional]*2,
                      y=[0, max_count],
                      name=wrap('Limiar log-normal', 30),
                      mode='lines',
                      line = dict(width=2, dash='dashdot'),
                      hoverinfo='skip',
                      opacity=0.9)
    

    
    
    data = [go.Histogram(x=taxas,
                         name='Número de municípios',
                         xbins=xbins_dict),
            taxa_BR_trace,
            taxa_UF_trace,
            taxa_capital_trace,
            taxa_limiar_trace,
            taxa_município_em_foco_trace,
            pdf_trace
           ]
    
    layout = go.Layout(title={
            "text":f'Histograma de taxas de Atendimentos em {dg.ano_em_foco} no alvo <br>{ds.alvo_completo}',
            'x':0.5,
            'xanchor': 'center'},
                       font=dict(size=10),
                       yaxis={'title':"Número de municípios"},
                       xaxis={'title': f'Atendimentos / {f_int(ds.denominador_populacional)} Habitantes SUS',
                              'range': [0, xmax + margin]
                              },
                        )
    
    return go.Figure(data=data, layout=layout)

# body = dbc.Container([dbc.Row([dbc.Col([dcc.Graph(id='histograma-taxas')
#                                        ], md=12)
#                               ])
#                      ])
    
# #botão_histograma_taxas = dbc.Button('HISTOGRAMA', id='botão-histograma-taxas', 
# #                                      n_clicks=0, color='success')

# @app.callback(Output('histograma-taxas', 'figure'),
# #              [Input('botão-histograma-taxas', 'n_clicks')],
#               [Input('store-análise', 'data')])
# def mostra_histograma_taxas(store_análise):
#     if store_análise is None:
#         return go.Figure(data=[], layout=go.Layout(title='Sem dados para exibição'))
#     return store_análise['Histograma_Taxas']
    
# def Histograma_Taxas():
#     layout = html.Div([ #botão_histograma_taxas,
#                         body
#                      ])
#     return layout