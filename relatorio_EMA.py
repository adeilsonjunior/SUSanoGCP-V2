from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output, State

from dash_app import app

from funcoes_de_apoio import f_int, f_float

EMPTY_REPORT = html.P('Sem dados para exibir. Por favor, use a aba "Escolha" para selecionar uma tripla (Estabelecimento, Município, Alvo)')


def descrição_alvo(dg, ds):
    table_header = [
            html.Thead(html.Tr([html.Th(ds.Cod_Alvo_em_foco + ' - ' + ds.A_em_foco.upper(), 
                                        style={'textAlign': 'center'})]))
    ]

    rows = []
    rows.append(html.Tr([html.Td("Grupo"), html.Td(ds.grupo_A_em_foco)]))
    rows.append(html.Tr([html.Td("Subgrupo"), html.Td(ds.subgrupo_A_em_foco)]))
    rows.append(html.Tr([html.Td("Estabelecimentos com produção"),
                         html.Td(f_int(ds.n_E_com_produção_no_alvo),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td("Municípios com produção"),
                         html.Td(f_int(ds.n_municípios_com_produção_no_alvo),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td("Estados com produção"),
                         html.Td(ds.n_UFs_com_produção_no_alvo,
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Atendimentos em {dg.ano_em_foco} (Brasil)"),
                         html.Td(f_int(ds.qtd_anual_A_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Valor total em {dg.ano_em_foco}"),
                         html.Td("R$ " + f_float(ds.valor_anual_A_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td("Valor médio (Brasil)"),
                         html.Td("R$ " + f_float(ds.valor_medio_A_Br),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Valor médio em {ds.M_Res_em_foco}"),
                         html.Td("R$ " + f_float(ds.valor_médio_M_Res),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f'Valor médio em {ds.M_Res_em_foco} por {ds.E_em_foco}'),
                         html.Td("R$ " + f_float(ds.valor_médio_anual_EMA),
                                 style={'textAlign': 'right'})]))
    table_body = [html.Tbody(rows)]
    return dbc.Col(html.Div([dbc.Table(table_header + table_body, size='sm')]),
                   width={"size": 8,
                          "offset": 2},
                   )
    
help_relatório_alvo = html.Div([
        "Dados do alvo escolhido.",
        html.Em("Excesso"), " é o produto do número de atendimentos que nosso ",
        "tratamento estatístico considerou excessivos, pelo valor médio ",
        "do atendimento. Para mais detalhes, veja a seção ",
        html.Em("Metodologia"), " na aba ", html.Em("SUSano.")
        ])

def descrição_estabelecimento(dg, ds):
    table_header = [html.Thead(html.Tr([
            html.Th(f'{ds.E_em_foco.upper()}, CNES {ds.CNES_em_foco}', style={'textAlign': 'center'})
            ])
        )]
    
    rows = []
    rows.append(html.Tr([html.Td("Localização"), html.Td(ds.M_E_em_foco + ', ' + ds.UF_E_em_foco)]))
    rows.append(html.Tr([html.Td(f"Atendimentos em {dg.ano_em_foco} (todos os alvos e municípios)"),
                         html.Td(f_int(ds.qtd_total_E_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Valor em {dg.ano_em_foco} (todos os alvos e municípios)"),
                         html.Td("R$ " + f_float(ds.valor_total_E_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Excesso em {dg.ano_em_foco} (todos os alvos e municípios)"),
                         html.Td("R$ " + f_float(ds.excesso_total_E_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Atendimentos no alvo {ds.Cod_Alvo_em_foco} (todos os municípios)"),
                         html.Td(f_int(ds.qtd_total_AE),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Municípios atendidos no alvo {ds.Cod_Alvo_em_foco}"),
                         html.Td(f_int(ds.n_municípios_atendidos_AE),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"UFs atendidas no alvo {ds.Cod_Alvo_em_foco}"),
                         html.Td(ds.n_UFs_atendidas_AE,
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f'Atendimentos em {ds.Cod_Alvo_em_foco} para residentes em {ds.M_Res_em_foco}'),
                         html.Td(ds.qtd_anual_EMA,
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f'Valor dos atendimentos em {ds.Cod_Alvo_em_foco} para residentes em {ds.M_Res_em_foco}'),
                         html.Td("R$ " + f_float(ds.valor_anual_EMA),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f'Excesso nos atendimentos em {ds.Cod_Alvo_em_foco} para residentes em {ds.M_Res_em_foco}'),
                         html.Td("R$ " + f_float(ds.excesso_anual_EMA),
                                 style={'textAlign': 'right'})]))
    
    table_body = [html.Tbody(rows)]
    return dbc.Col(html.Div([dbc.Table(table_header + table_body, size='sm')]),
                   width={"size": 8, "offset": 2}
                   )    
    
def descrição_município(dg, ds):
    table_header = [
            html.Thead(html.Tr([html.Th(f"Município de Residência: {ds.M_Res_em_foco.upper() + ', ' + ds.UF_M_Res_em_foco} - {ds.IBGE_Res_em_foco}", 
                                        style={'textAlign': 'center'})]))
    ]

    rows = []

    rows.append(html.Tr([html.Td("População"), html.Td(f_int(ds.pop_M_Res_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td("População SUS"), html.Td(f_int(ds.pop_SUS_M_Res_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td("Atendimentos (todos os alvos)"), 
                         html.Td(f_int(ds.qtd_anual_M_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td("Valor (todos os alvos)"),
                         html.Td("R$ " + f_float(ds.valor_total_M_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td("Excesso (todos os alvos)"),
                         html.Td("R$ " + f_float(ds.excesso_total_M_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Excesso em {ds.Cod_Alvo_em_foco}"),
                         html.Td("R$ " + f_float(ds.excesso_MA_em_foco),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f"Atendimentos em {ds.Cod_Alvo_em_foco}"),
                         html.Td(f_int(ds.qtd_MA_em_foco),
                                 style={'textAlign': 'right'})]))    
    rows.append(html.Tr([html.Td(f'Atendimentos em {ds.Cod_Alvo_em_foco} por {ds.E_em_foco}'),
                         html.Td(f_int(ds.qtd_anual_EMA),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f'Valor total dos atendimentos em {ds.Cod_Alvo_em_foco} '),
                         html.Td("R$ " + f_float(dg.MA_to_valor[ds.IBGE_Res_em_foco, ds.Cod_Alvo_em_foco]),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f'Valor dos atendimentos em {ds.Cod_Alvo_em_foco} por {ds.E_em_foco}'),
                         html.Td("R$ " + f_float(ds.valor_anual_EMA),
                                 style={'textAlign': 'right'})]))
    rows.append(html.Tr([html.Td(f'Excesso nos atendimentos em {ds.Cod_Alvo_em_foco} por {ds.E_em_foco}'),
                         html.Td("R$ " + f_float(ds.excesso_anual_EMA),
                                 style={'textAlign': 'right'})]))    

    table_body = [html.Tbody(rows)]
    return dbc.Col(html.Div([dbc.Table(table_header + table_body, size='sm')]),
                   width={"size": 6, "offset": 3}
                   )
    
help_relatório_estabelecimento = html.Div([
        "Dados do estabelecimento escolhido.",
        html.Em("Excesso"), " é o produto do número de atendimentos que nosso ",
        "tratamento estatístico considerou excessivos, pelo valor médio ",
        "do atendimento. Para mais detalhes, veja a seção ",
        html.Em("Metodologia"), " na aba SUSano."
        ])

help_relatório_município = html.Div([
        "Dados do município de residência escolhido",
        html.Em("Excesso"), " é o produto do número de atendimentos que nosso ",
        "tratamento estatístico considerou excessivos, pelo valor médio ",
        "do atendimento. Para mais detalhes, veja a seção ",
        html.Em("Metodologia"), " na aba SUSano."
        ])

def descrição_distribuição(dg, ds):
    
    explicação = f'Em {dg.ano_em_foco} residentes em {ds.M_Res_em_foco} receberam {ds.qtd_anual_M_Res_em_foco} atendimentos em {ds.A_em_foco}, distribuídos da seguinte forma:'
    
    return dbc.Col(html.Div([html.P(explicação),
                             dbc.Table.from_dataframe(ds.df_atendimento_AM,
                                                      size='sm')]),
                    width={"size": 8, "offset": 2}
                    )

help_relatório_distribuição = html.Div([
        "Distribuição entre prestadores do atendimento ao município escolhido, ",
        "no alvo escolhido."])

def descrição_maiores_taxas(dg, ds):
    explicação = 'Municípios do Brasil com as maiores taxas de atendimento'
    
    return dbc.Col(html.Div([html.P(explicação),
                            dbc.Table.from_dataframe(ds.df_maiores_taxas_no_alvo,
                                                     size='sm')]
                            ),
                   width={"size": 8, "offset": 2}
                   )

help_relatório_maiores_taxas = html.Div([
        "Municípios com as maiores taxas de atendimento ",
        "no alvo escolhido."])
        

        
def descrição_comparação_de_taxas(dg, ds):
    table_header = [
            html.Thead(html.Tr([html.Th("Local"), html.Th("População",
                                 style={'textAlign': 'right'}), 
                                html.Th("Pop SUS",
                                 style={'textAlign': 'right'}), 
                                html.Th("Qtd",
                                 style={'textAlign': 'right'}), 
                                html.Th(f"Qtd / {f_int(ds.denominador_populacional)} hab-SUS",
                                 style={'textAlign': 'right'})
                                ]))
        ]
            
    rows = [] 
    
    taxa_normalizada_M_Res = ds.taxa_anual_M_Res * ds.denominador_populacional
    rows.append(html.Tr([html.Td(ds.M_Res_em_foco), 
                         html.Td(f_int(ds.pop_M_Res_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(ds.pop_SUS_M_Res_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(ds.qtd_anual_M_Res_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_float(taxa_normalizada_M_Res),
                                 style={'textAlign': 'right'})
                         ]))
    
    taxa_normalizada_Capital = ds.taxa_anual_Capital * ds.denominador_populacional        
    rows.append(html.Tr([html.Td(ds.Capital_em_foco), 
                         html.Td(f_int(ds.pop_Capital_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(ds.pop_SUS_Capital_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(ds.qtd_anual_Capital_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_float(taxa_normalizada_Capital),
                                 style={'textAlign': 'right'})
                         ]))    
            
    taxa_normalizada_UF = ds.taxa_anual_UF * ds.denominador_populacional
    rows.append(html.Tr([html.Td(ds.nome_UF_Res_em_foco), 
                         html.Td(f_int(ds.pop_UF_Res_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(ds.pop_SUS_UF_Res_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(ds.qtd_anual_UF),
                                 style={'textAlign': 'right'}),
                         html.Td(f_float(taxa_normalizada_UF),
                                 style={'textAlign': 'right'})
                         ]))
            
    taxa_normalizada_Br = ds.taxa_anual_Br * ds.denominador_populacional
    rows.append(html.Tr([html.Td("Brasil"), 
                         html.Td(f_int(dg.pop_Br),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(dg.pop_SUS_Br),
                                 style={'textAlign': 'right'}),
                         html.Td(f_int(ds.qtd_anual_A_em_foco),
                                 style={'textAlign': 'right'}),
                         html.Td(f_float(taxa_normalizada_Br),
                                 style={'textAlign': 'right'})
                         ], className="tableTr"))    
            
    table_body = [html.Tbody(rows)]
    
    comentários = html.Div([
            html.P(f"Em {dg.ano_em_foco}, a taxa de atendimentos por habitante-SUS em {ds.M_Res_em_foco} foi:"),
            html.Ul([
                    html.Li(f"{f_float(ds.taxa_anual_M_Res/ds.taxa_anual_Capital)} vezes a taxa da capital {ds.Capital_em_foco}"),
                    html.Li(f"{f_float(ds.taxa_anual_M_Res/ds.taxa_anual_UF)} vezes a taxa da UF {ds.nome_UF_Res_em_foco}"),
                    html.Li(f"{f_float(ds.taxa_anual_M_Res/ds.taxa_anual_Br)} vezes a taxa do Brasil")
                    ])
            ])
            
    return dbc.Col(html.Div([ds.div_alvo_completo,
                             dbc.Table(table_header + table_body, size='sm'),
                             comentários]),
                   width={"size": 8,
                           "offset": 2}
                  )
            
help_relatório_comparação_de_taxas = html.Div([
        "Comparação entre taxas de atendimento por habitante-SUS no alvo escolhido, verificadas ",
        "no município de residência escolhido, na UF desse município e em sua capital, ",
        "e no Brasil"])

seleção = dcc.Dropdown(
                       id = "relatório-o-que-mostrar",
                       options=[
                               {"label": "Estabelecimento", "value": "estabelecimento"},
                               {"label": "Município", "value": "município"},
                               {"label": "Alvo", "value": "alvo"},
                               {"label": "Distribuição do atendimento", "value": "distribuição"},
                               {"label": "Comparação de taxas de atendimento por habitante SUS",
                                "value": "comparação-de-taxas"},
                               {"label": "Maiores taxas de atendimento", "value": "maiores-taxas"}
                               ],
                       value="comparação-de-taxas"
                       )

conteúdo = html.Div(id="conteúdo")

help_relatórios_EMA = {}
help_relatórios_EMA["estabelecimento"] = help_relatório_estabelecimento
help_relatórios_EMA["município"] = help_relatório_município
help_relatórios_EMA["alvo"] = help_relatório_alvo
help_relatórios_EMA["distribuição"] = help_relatório_distribuição
help_relatórios_EMA["comparação-de-taxas"] = help_relatório_comparação_de_taxas
help_relatórios_EMA["maiores-taxas"] = help_relatório_maiores_taxas
    
def gera_relatório_EMA(dg, ds):
    return {"estabelecimento": descrição_estabelecimento(dg, ds),
            "alvo": descrição_alvo(dg, ds),
            "município": descrição_município(dg, ds),
            "distribuição": descrição_distribuição(dg, ds),
            "comparação-de-taxas": descrição_comparação_de_taxas(dg, ds),
            "maiores-taxas": descrição_maiores_taxas(dg, ds)
            }
    

#relatório_EMA = html.Div(id='relatório-EMA', children=[])

@app.callback([Output('conteúdo', 'children'),
               Output('help-relatórios-EMA', 'data')],
              [Input('relatório-o-que-mostrar', 'value')],
              [State('store-análise', 'data')])
def mostra_relatório(o_que_mostrar, store_análise):
    if store_análise is None:
        return html.P('mostra_relatório: store_análise is None!!'), \
               html.P('Help Relatórios')
    try:
        return store_análise['Relatório_EMA'][o_que_mostrar], \
               help_relatórios_EMA[o_que_mostrar]
    except:
        return [html.P(str(store_análise['Relatório_EMA'])),
                html.P(o_que_mostrar)], \
               help_relatórios_EMA[o_que_mostrar]



def Relatório_EMA():
    return html.Div([seleção,
                     conteúdo])
