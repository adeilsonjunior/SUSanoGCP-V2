import plotly.graph_objs as go
from dash import html
import numpy as np

help_gr_gini_alvo = html.Div([
        "Este gráfico mostra para o alvo escolhido percentuais acumulados de atendimentos ",
        "versus percentuais acumulados da população SUS do Brasil. "
    ])

def interpola(X, Y, P):
    #print(f'X.shape = {X.shape}, X.min() = {X.min()}, X.max() = {X.max()}')
    #print(f'Y.shape = {Y.shape}, Y.min() = {Y.min()}, Y.max() = {Y.max()}\n')
    yP = []
    for p in P:
        xa = max(X[X<=p])
        ia = np.where(X == xa)[0][0]
        ya = Y[ia]
        #print(f'xa = {xa}, ia = {ia}, ya = {ya}')
        xb = min(X[X>=p])
        ib = np.where(X == xb)[0][0]
        yb = Y[ib]
        #print(f'xb = {xb}, ib = {ib}, yb = {yb}\n')
        if xb == xa:
            yp = ya
        else:
            yp = ya + (yb - ya) * (p - xa) / (xb - xa)
        print(f'yp = {yp}\n')
        yP.append(yp)
    return yP

def gera_gr_gini_alvo(dg, ds):
    Qtd_total = ds.df_M_Alvo_em_foco['Qtd_EMA'].sum()
    Pop_SUS_total = ds.df_M_Alvo_em_foco['POP_SUS'].sum()
    Qtd_Acumulada = np.array(ds.df_M_Alvo_em_foco['Qtd_EMA'].cumsum())
    Pop_SUS_Acumulada = np.array(ds.df_M_Alvo_em_foco['POP_SUS'].cumsum())
    Qtd_Acumulada_Perc = (Qtd_Acumulada / Qtd_total) * 100
    Pop_SUS_Acumulada_Perc = (Pop_SUS_Acumulada / Pop_SUS_total) * 100

    #for i in range(1618, 1621):
    #    print(f'Qtd_Acumulada_Perc[{i}]     = {Qtd_Acumulada_Perc[i]}')
    #    print(f'Pop_SUS_Acumulada_Perc[{i}] = {Pop_SUS_Acumulada_Perc[i]}')

    gini_trace = go.Scatter(
        x=Pop_SUS_Acumulada_Perc,
        y=Qtd_Acumulada_Perc,
        name=f'Acesso verificado',
        mode='lines'
        )

    ideal_trace = go.Scatter(
        x=[0, 100],
        y=[0, 100],
        name='Acesso ideal',
        mode='lines',
        line=dict(color='black', dash='dot')
        )

    percentis = [10, 50, 90]
    ypercentis = interpola(Pop_SUS_Acumulada_Perc, Qtd_Acumulada_Perc, percentis)

    percentis_trace = go.Scatter(
        x=percentis,
        y=ypercentis,
        mode='markers',
        name='Percentis',
        marker=dict(size=12,
                    line=dict(width=2,
                              color='DarkSlateGrey'))
        )

    data=[gini_trace, ideal_trace, percentis_trace]

    layout = go.Layout(
        title={
            'text': f'Acesso em {dg.ano_em_foco} ao alvo <br>{ds.alvo_completo}',
            'x':0.5,
            'xanchor': 'center'
            },
        font=dict(size=10),
        xaxis={'title':f"Percentual da população SUS"},
        yaxis={'title': 'Percentual dos atendimentos'},
        )
    
    
    return go.Figure(data=data, layout=layout)