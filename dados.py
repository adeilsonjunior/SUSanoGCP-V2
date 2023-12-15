# -*- coding: utf-8 -*-
"""
Created on Wed May  6 06:31:15 2020

@author: Osvaldo Carvalho
"""

import pandas as pd
import numpy as np
import os
import sys



from dash import html

from funcoes_de_apoio import f_perc, normatiza

# from google.cloud import storage

# def download_blob(bucket_name, source_blob_name, destination_file_name):
#     """Downloads a blob from the bucket."""
#     # https://cloud.google.com/storage/docs/downloading-objects#code-samples
#     # bucket_name = "your-bucket-name"
#     # source_blob_name = "storage-object-name"
#     # destination_file_name = "local/path/to/file"

#     storage_client = storage.Client()

#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(source_blob_name)
#     blob.download_to_filename(destination_file_name)

#     print(
#         "Blob {} downloaded to {}.".format(
#             source_blob_name, destination_file_name
#         )
#     )

print(f'Início {__name__=}')

ano_susano = sys.argv[1]

data_files_path = os.path.join('.','Dados', ano_susano)

print(f'{data_files_path=}')

tmp_path = os.path.join('/tmp')

# pkl_source = os.environ.get('PKL_BUCKET')
pkl_source = 'LOCAL'
# Mudar assim que aprender a usar variáveis de ambiente no windows
print(f'{pkl_source=}')

key_path = os.path.join('.', 'susano-dash-da48ac20ddee.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

all_files = []

dtypes_EMA = {'CNES':str,
             'IBGE_Res':str,
             'IBGE_Estab': str,
             'IBGE_CAPITAL': str,
             'CO_GRUPO': str,
             'CO_GRUPO_SUBGRUPO': str}

def read_df(df_name):
    zip_file = df_name + '.zip'
    # local_path = os.path.join(data_files_path, pkl_file)
    local_path =  os.path.join(data_files_path, zip_file)
    print(f'{local_path=}')
    gc_path = os.path.join(tmp_path, zip_file)
    if pkl_source == 'LOCAL':
        df = pd.read_csv(local_path, dtype=dtypes_EMA)
        # df = pd.read_pickle(local_path)
    else:
        # download_blob(pkl_source, 'Dados/' + zip_file, gc_path)
        df = pd.read_csv(gc_path)
        os.remove(gc_path)
    all_files.append(zip_file)
    return df

class dados_globais:
    
    def __init__(self):
        
        self.ano_em_foco = int(ano_susano)
        
        self.df_capitais = read_df('df_capitais')
        self.UF_to_ibge_capital = self.df_capitais.set_index(['UF'])['IBGE_CAPITAL']
        self.UF_to_nome_UF = self.df_capitais.set_index(['UF'])['NOME_UF']
        
        self.df_EMA = read_df('df_EMA')
        # df_EMA contém os totais anuais para cada (Estabelecimento, Município, Alvo)
    
        self.df_EMA_mês = read_df('df_EMA_mes')
        # df_EMA_mês contém os valores mensais para cada (Estabelecimento, Município, Alvo, mês)
        
#        self.EMA_mês_to_qtd = self.df_EMA_mês.set_index(['CNES', 'IBGE_Res', 'Cod_Alvo', 'Mês'])['Qtd_EMA_mês']
#        self.dict_EMA_mês = self.df_EMA_mês.set_index(['CNES', 'IBGE_Res', 'Cod_Alvo', 'Mês']).T.to_dict('list')
#        Por algum motivo, a criação do dicionário está demorando muito

        self.df_M = read_df('df_M')
        self.dict_M = self.df_M.set_index(['IBGE_Res']).T.to_dict('list')
        # [NOME_MUN, SIGLA_UF, POP_MUN, POP_MUN_SUS, LAT, LONG, Qtd, Valor, Excesso] = dict_M[IBGE6_MUN]

        self.df_E = read_df('df_E')
        self.CNES_to_Nome_Estab = self.df_E.set_index(['CNES'])['Nome_Estab']
        self.dict_E = self.df_E.set_index(['CNES']).T.to_dict('list')
        # [uf_estab, ibge_estab, nome_estab, abrev_estab, qtd_estab, valor_estab, excesso_estab]=dict_E['2077396']
        
        self.df_A = read_df('df_A')
        print(f'{self.df_A.columns=}')
        self.dict_A = self.df_A.set_index(['Cod_Alvo']).T.to_dict('list')
        # [nome_alvo, qtd, valor, excesso, abrev_alvo] = dict_A[cod_alvo]
        self.Cod_Alvo_to_Alvo = self.df_A.set_index(['Cod_Alvo'])['Alvo']
        
        self.df_MA = read_df('df_MA')
        print(f'******** df_MA.columns = {self.df_MA.columns}')
        self.MA_to_excesso = self.df_MA.set_index(['IBGE_Res', 'Cod_Alvo'])['Excesso_MA']
        self.MA_to_valor = self.df_MA.set_index(['IBGE_Res', 'Cod_Alvo'])['Valor_MA']
        self.MA_to_qtd = self.df_MA.set_index(['IBGE_Res', 'Cod_Alvo'])['Qtd_MA']
        
        self.df_EMA_g_A = read_df('df_EMA_g_A')
        # self.df_EMA_g_A = self.df_EMA.groupby(['Cod_Alvo']).sum().reset_index()
        # self.df_EMA_g_A['Valor_Médio'] = self.df_EMA_g_A['Valor_EMA'] / self.df_EMA_g_A['Qtd_EMA']
        # self.df_EMA_g_A['Registro'] = self.df_EMA_g_A['Cod_Alvo'].str.slice(start=7)
        # self.df_EMA_g_A['Alvo'] = [self.Cod_Alvo_to_Alvo[cod_alvo] for cod_alvo in self.df_EMA_g_A['Cod_Alvo']]
        
        self.df_alvo_mês_limiar = read_df('df_alvo_mes_limiar')
        self.A_mês_to_limiar = self.df_alvo_mês_limiar.set_index(['Cod_Alvo', 'Mês'])['Limiar']
    
        self.df_grupos = read_df('df_grupos')
        self.dict_grupos = self.df_grupos.set_index(['CO_GRUPO']).T.to_dict('list')
        # [nome_grupo] = dict_grupos['04']
        
        self.df_subgrupos = read_df('df_subgrupos')
        self.dict_subgrupos = self.df_subgrupos.set_index(['CO_GRUPO_SUBGRUPO']).T.to_dict('list')
        # [nomesubgrupo] = dict_subgrupos['0214']
        
        self.df_pop_UF = read_df('df_pop_UF')
        self.dict_pop_UF = self.df_pop_UF.set_index(['SIGLA_UF']).T.to_dict('list')
        
        self.pop_Br = self.df_M['POP'].sum()
        self.pop_SUS_Br = self.df_M['POP_SUS'].sum()
        
        print(f'\n{all_files=}\n')
        
   
    def limiares_mensais_A(self, A):
        limiares_mensais = []
        for mês in range(1, 13):
            try:
                limiares_mensais.append(self.A_mês_to_limiar[(A, mês)])
            except:
                limiares_mensais.append(0)
        return np.array(limiares_mensais)

# Criação dos dados globais, feita na inicialização do aplicativo
dg = dados_globais()



def qtds_mensais(df_registros_mensais, campo_qtd):
    df_registros_mensais_g_mês = df_registros_mensais.groupby(['Mês']).sum().reset_index()
    dict_qtd_mês = df_registros_mensais_g_mês.set_index(['Mês'])[campo_qtd]
    qtds = []
    for mês in range(1, 13):
        try:
            qtds.append(dict_qtd_mês[mês])
        except:
            qtds.append(0)
    return np.array(qtds)
    

class dados_sessão:
    
    
    def __init__(self, dg, CNES_em_foco, IBGE_Res_em_foco, Cod_Alvo_em_foco):
        
        self.CNES_em_foco = CNES_em_foco
        self.IBGE_Res_em_foco = IBGE_Res_em_foco
        self.IBGE_UF_em_foco = IBGE_Res_em_foco[:2]
        self.Cod_Alvo_em_foco = Cod_Alvo_em_foco

        [self.UF_E_em_foco, self.IBGE_E_em_foco, self.M_E_em_foco, self.E_em_foco, 
         self.qtd_total_E_em_foco, self.valor_total_E_em_foco, self.valor_Excesso_Estab,
         self.excesso_total_E_em_foco, self.abrev_E_em_foco] = dg.dict_E[self.CNES_em_foco]
        
        # Dados do município do estabelecimento em foco
        [self.UF_E_em_foco, self.Nome_UF_E_em_foco, self.M_E_em_foco,  
         self.pop_M_E_em_foco, self.pop_SUS_M_E_em_foco,
         self.qtd_anual_M_E_em_foco, self.valor_total_M_E_em_foco, 
         self.valor_excesso_estab_em_foco,
         self.excesso_total_M_E_em_foco] = dg.dict_M[self.IBGE_E_em_foco]
        
        
        # Dados do município de residência em foco
        [ self.UF_M_Res_em_foco, self.Nome_UF_Res_em_foco, self.M_Res_em_foco, 
         self.pop_M_Res_em_foco, self.pop_SUS_M_Res_em_foco,
         self.qtd_anual_M_em_foco, self.valor_total_M_em_foco, 
         self.valor_excesso_M_em_foco,
         self.excesso_total_M_em_foco] = dg.dict_M[self.IBGE_Res_em_foco]
        self.excesso_MA_em_foco = dg.MA_to_excesso[self.IBGE_Res_em_foco,
                                                    self.Cod_Alvo_em_foco]
        self.qtd_MA_em_foco = dg.MA_to_qtd[self.IBGE_Res_em_foco,
                                                    self.Cod_Alvo_em_foco]
        
        # Dados da capital do município de residência em foco
        self.IBGE_Capital_em_foco = dg.UF_to_ibge_capital[self.UF_M_Res_em_foco]
        [ self.UF_Capital_em_foco, self.nome_UF_Capital_em_foco, self.Capital_em_foco, 
         self.pop_Capital_em_foco, self.pop_SUS_Capital_em_foco,
         self.qtd_anual_Capital_em_foco, self.valor_total_Capital_em_foco, 
         self.valor_excesso_Capital_em_foco,
         self.excesso_total_Capital_em_foco] = dg.dict_M[self.IBGE_Capital_em_foco]  
        
        # Nome, população e população SUS da UF em foco
        self.nome_UF_Res_em_foco = dg.UF_to_nome_UF[self.UF_M_Res_em_foco]
        [self.NOME_UF, self.pop_UF_Res_em_foco,  self.pop_SUS_UF_Res_em_foco,
         self.QTD_UF_EM_FOCO, self.VALOR_UF_EM_FOCO,
         self.VALOR_EXCESSO_EM_FOCO, self.VALOR_EXCESSO_ESTAB_MIN_UF_EM_FOCO] = dg.dict_pop_UF[self.UF_M_Res_em_foco]


        # Dados do alvo em foco
        [self.A_em_foco, self.qtd_anual_A_em_foco, 
         self.valor_anual_A_em_foco, self.VALOR_EXCESSO_A_EM_FOCO, self.excesso_anual_A_em_foco, 
         self.abrev_A_em_foco] = dg.dict_A[self.Cod_Alvo_em_foco]
        
        self.valor_medio_A_Br = self.valor_anual_A_em_foco / self.qtd_anual_A_em_foco
        self.taxa_anual_Br = self.qtd_anual_A_em_foco/dg.pop_SUS_Br
   
        self.registro_A_em_foco = 'SIH' if self.Cod_Alvo_em_foco[-1] == 'H' else 'SIA'
        self.Cod_grupo_A_em_foco = self.Cod_Alvo_em_foco[0:2]
        [self.grupo_A_em_foco] = dg.dict_grupos[self.Cod_grupo_A_em_foco]
        self.Cod_subgrupo_A_em_foco = self.Cod_Alvo_em_foco[0:4]
        [self.subgrupo_A_em_foco] = dg.dict_subgrupos[self.Cod_subgrupo_A_em_foco]
        self.Cod_forma_A_em_foco = self.Cod_Alvo_em_foco[4:]
    
        self.df_EMA_mês_f_A = dg.df_EMA_mês[dg.df_EMA_mês['Cod_Alvo'] == Cod_Alvo_em_foco]
        # df_EMA_mês_f_A contém os registros mensais (Estabelecimento, Município, mês) relativos ao alvo em foco
        self.qtds_mensais_Br = qtds_mensais(self.df_EMA_mês_f_A, 'Qtd_EMA_mês')
        self.taxas_mensais_Br = self.qtds_mensais_Br / dg.pop_SUS_Br
        self.expec_taxas_Br = self.taxas_mensais_Br * self.pop_SUS_M_Res_em_foco
 
        self.df_EMA_mês_f_A_UF = self.df_EMA_mês_f_A[self.df_EMA_mês_f_A['IBGE_Res'].str.startswith(self.IBGE_UF_em_foco)]
        # df_EMA_mês_f_A_UF contém os registros mensais para a UF em foco relativos ao alvo em foco
        self.qtds_mensais_UF = qtds_mensais(self.df_EMA_mês_f_A_UF, 'Qtd_EMA_mês')
        self.taxas_mensais_UF = self.qtds_mensais_UF / self.pop_SUS_UF_Res_em_foco
        self.expec_taxas_UF = self.taxas_mensais_UF * self.pop_SUS_M_Res_em_foco
        
        
        self.df_EMA_mês_f_MA = self.df_EMA_mês_f_A[self.df_EMA_mês_f_A['IBGE_Res'] == IBGE_Res_em_foco]
        # df_EMA_mês_f_MA contém os registros mensais para o município em foco relativos ao alvo em foco
        self.qtds_mensais_MA = qtds_mensais(self.df_EMA_mês_f_MA, 'Qtd_EMA_mês')

        self.df_EMA_mês_f_Capital_A = self.df_EMA_mês_f_A[self.df_EMA_mês_f_A['IBGE_Res'] == self.IBGE_Capital_em_foco]
        # df_EMA_mês_f_Capital_A contém os registros mensais para a capital em foco relativos ao alvo em foco
        self.qtds_mensais_Capital = qtds_mensais(self.df_EMA_mês_f_Capital_A, 'Qtd_EMA_mês')
        self.taxas_mensais_Capital = self.qtds_mensais_Capital / self.pop_SUS_Capital_em_foco
        self.expec_taxas_Capital = self.taxas_mensais_Capital * self.pop_SUS_M_Res_em_foco
        
        self.df_EMA_mês_f_EMA = self.df_EMA_mês_f_MA[self.df_EMA_mês_f_MA['CNES'] == CNES_em_foco]
        self.qtds_mensais_EMA = qtds_mensais(self.df_EMA_mês_f_EMA, 'Qtd_EMA_mês')
        self.valor_anual_EMA = self.df_EMA_mês_f_EMA['Valor_EMA_mês'].sum()
        self.excesso_anual_EMA = self.df_EMA_mês_f_EMA['Excesso_EMA_mês'].sum()
        self.qtd_anual_EMA = self.df_EMA_mês_f_EMA['Qtd_EMA_mês'].sum()
        self.valor_médio_anual_EMA = self.valor_anual_EMA / self.qtd_anual_EMA
        
        
        self.df_EMA_f_A = dg.df_EMA[dg.df_EMA['Cod_Alvo'] == Cod_Alvo_em_foco]
        # df_EMA_f_A contém os valores anuais por (Estabelecimento, Município), relativos ao alvo em foco
        
        self.n_municípios_com_produção_no_alvo = len(self.df_EMA_f_A['IBGE_Estab'].unique())
        self.n_UFs_com_produção_no_alvo = len(self.df_EMA_f_A['UF_Estab'].unique())
        self.n_E_com_produção_no_alvo = len(self.df_EMA_f_A['CNES'].unique())
        
        self.df_EMA_f_AE = self.df_EMA_f_A[self.df_EMA_f_A['CNES'] == CNES_em_foco]
        # df_EMA_f_AE contém os valores anuais por (Município), relativos ao alvo em foco 
        # e ao estabelecimento em foco
        
        self.qtd_total_AE = self.df_EMA_f_AE['Qtd_EMA'].sum()
        self.n_municípios_atendidos_AE = len(self.df_EMA_f_AE['IBGE_Res'].unique())
        self.n_UFs_atendidas_AE = len(self.df_EMA_f_AE['UF_Res'].unique())
        
        self.df_EMA_f_A_g_M = self.df_EMA_f_A.groupby(['IBGE_Res']).sum()
        # df_EMA_f_A_g_M contém os valores anuais por (Município) relativos ao alvo em foco
        # somente para municípios com pelo menos um registro em df_EMA
        
        self.df_M_Alvo_em_foco = dg.df_M.merge(self.df_EMA_f_A_g_M, 
                                               on='IBGE_Res', 
                                               how='left').fillna(0)
        self.df_M_Alvo_em_foco.rename(columns={'UF_Res_x': 'UF_Res'})
        print(f'****** df_M_Alvo_em_foco.columns = {self.df_M_Alvo_em_foco.columns}')
        # df_M_Alvo_em_foco contém os valores anuais por (Município) relativos ao alvo em foco
        # para *todos* os municípios do Brasil
        
        # self.df_M_Alvo_em_foco.drop(['LAT', 'LONG', 'Qtd_M', 
        #                               'Valor_M', 'Excesso_M'], 
        #                             axis=1, inplace=True)
        
        # self.df_M_Alvo_em_foco.drop(['Qtd_EMA', 
        #                               'Valor_EMA', 'Excesso_'], 
        #                             axis=1, inplace=True)
        self.df_M_Alvo_em_foco = self.df_M_Alvo_em_foco.astype({"Qtd_EMA": int}) # Não sei por qual motivo isso se tornou necessário
        self.df_M_Alvo_em_foco['Taxa_por_hab_SUS'] = self.df_M_Alvo_em_foco['Qtd_EMA']/self.df_M_Alvo_em_foco['POP_SUS']
        self.df_M_Alvo_em_foco.sort_values(by=['Taxa_por_hab_SUS', 'POP_SUS'], inplace=True)
        print(f'df_M_Alvo_em_foco.columns = {self.df_M_Alvo_em_foco.columns}')
        self.df_maiores_taxas_no_alvo = self.df_M_Alvo_em_foco.nlargest(5, ['Taxa_por_hab_SUS'])
        self.IBGE_to_Qtd_Alvo_em_foco = self.df_M_Alvo_em_foco.set_index(['IBGE_Res'])['Qtd_EMA']
        self.IBGE_to_Valor_Alvo_em_foco = self.df_M_Alvo_em_foco.set_index(['IBGE_Res'])['Valor_EMA']
        
        self.qtd_anual_M_Res_em_foco = self.IBGE_to_Qtd_Alvo_em_foco[self.IBGE_Res_em_foco]
        self.taxa_anual_M_Res = self.qtd_anual_M_Res_em_foco / self.pop_SUS_M_Res_em_foco
        self.valor_anual_M_Res = self.IBGE_to_Valor_Alvo_em_foco[self.IBGE_Res_em_foco]
        self.valor_médio_M_Res = self.valor_anual_M_Res / self.qtd_anual_M_Res_em_foco
          
        self.qtd_anual_Capital_em_foco = self.IBGE_to_Qtd_Alvo_em_foco[self.IBGE_Capital_em_foco]
        self.taxa_anual_Capital = self.qtd_anual_Capital_em_foco / self.pop_SUS_Capital_em_foco
    
    
        self.df_EMA_f_A_g_UF = self.df_EMA_f_A.groupby(['UF_Res']).sum()
        # df_EMA_f_A_g_UF contém os valores anuais por UF relativos ao alvo em foco
        # Para obter o número de atendimentos na UF 'AP' (p. ex.), use df_EMA_f_A_g_UF.loc['AP']['Qtd_EMA']
    
        self.qtd_anual_UF = self.df_EMA_f_A_g_UF.loc[self.UF_M_Res_em_foco]['Qtd_EMA']
        self.taxa_anual_UF = self.qtd_anual_UF / self.pop_SUS_UF_Res_em_foco
        
        limiares_mensais = dg.limiares_mensais_A(Cod_Alvo_em_foco)
        self.expec_limiares_mensais = limiares_mensais * self.pop_SUS_M_Res_em_foco
        
        self.df_EMA_f_AM = self.df_EMA_f_A[self.df_EMA_f_A['IBGE_Res'] == IBGE_Res_em_foco]
        # df_EMA_f_AM contém os valores anuais por (Estabelecimento) para o alvo e município em foco
        self.df_atendimento_AM = self.df_EMA_f_AM[['CNES', 'Qtd_EMA']].sort_values(by='Qtd_EMA', ascending=False)
        self.df_atendimento_AM['Estabelecimento'] = [dg.CNES_to_Nome_Estab[cnes] for cnes in self.df_atendimento_AM['CNES']]
        self.df_atendimento_AM['Perc'] = [f_perc((q / self.qtd_anual_M_Res_em_foco) * 100) for q in self.df_atendimento_AM['Qtd_EMA']]
        self.df_atendimento_AM = self.df_atendimento_AM[['CNES', 'Estabelecimento', 'Qtd_EMA', 'Perc']]
        self.df_atendimento_AM.columns = ['CNES', 'Estabelecimento', 'Qtd', 'Perc']
        
        
        self.taxa_anual_limiar = limiares_mensais.sum()
        
        self.taxa_anual_mínima = min([t for t in [self.taxa_anual_Br, 
                                            self.taxa_anual_UF,
                                            self.taxa_anual_Capital,
                                            self.taxa_anual_M_Res,
                                            self.taxa_anual_limiar] if t > 0])
        self.denominador_populacional = normatiza(self.taxa_anual_mínima)
        
        self.alvo_completo = f"Grupo: {self.Cod_grupo_A_em_foco} {self.grupo_A_em_foco} " + \
                f"Subgrupo: {self.Cod_subgrupo_A_em_foco} {self.subgrupo_A_em_foco}" + \
                f'<br>Forma: {self.Cod_forma_A_em_foco} <b>{self.A_em_foco}</b>'
        
        self.div_alvo_completo = html.Div([
                f"Grupo: {self.Cod_grupo_A_em_foco} {self.grupo_A_em_foco}",
                html.Br(),
                f"Subgrupo: {self.Cod_subgrupo_A_em_foco} {self.subgrupo_A_em_foco}",
                html.Br(),
                f"Forma: {self.Cod_forma_A_em_foco} {self.A_em_foco}",
                html.Hr()
                ])

print(f'Término {__name__=}')
        