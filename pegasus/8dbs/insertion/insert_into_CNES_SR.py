############################################################################################################################################################################
#  CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR CNES_SR #
############################################################################################################################################################################

import time

import numpy as np
import pandas as pd

from .data_wrangling.prepare_CNES_SR import *

############################################################################################################################################################################
#  pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas #
############################################################################################################################################################################
############################################################################################################################################################################
# AUXILIARY TABLES * AUXILIARY TABLES * AUXILIARY TABLES * AUXILIARY TABLES * AUXILIARY TABLES * AUXILIARY TABLES * AUXILIARY TABLES * AUXILIARY TABLES * AUXILIARY TABLES #
############################################################################################################################################################################

# Função que utiliza para a inserção de dados não principais o pandas.to_sql + SQLAlchemy
def insert_most_CNES_SR_tables_pandas(path, device, child_db):
    # Inserção dos dados das tabelas não principais no banco de dados
    label1 = 'append'
    label2 = 'ID'

    # Chama funções definidas no módulo "prepare_CNES_SR" do package "data_wrangling"
    df_CADGERBR = get_CADGERBR_treated(path)
    df_CADGERBR.to_sql('cnes', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_TABUF = get_TABUF_treated()
    df_TABUF.to_sql('ufcod', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_CADMUN = get_CADMUN_treated()
    df_CADMUN.to_sql('codufmun', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_SERVICO = get_SERVICO_treated()
    df_SERVICO.to_sql('servesp', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_CLASSSR = get_CLASSSR_treated()
    df_CLASSSR.to_sql('classsr', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_SERVICO = get_SERVICO_treated()
    df_SERVICO.to_sql('srvunico', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_TPGESTAO = get_TPGESTAO_treated()
    df_TPGESTAO.to_sql('tpgestao', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_TP_PFPJ = get_TP_PFPJ_treated()
    df_TP_PFPJ.to_sql('pfpj', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_NIVELDEP = get_NIVELDEP_treated()
    df_NIVELDEP.to_sql('nivdep', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_EsferAdm = get_EsferAdm_treated()
    df_EsferAdm.to_sql('esferaa', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_Ativ_Ens = get_Ativ_Ens_treated()
    df_Ativ_Ens.to_sql('atividad', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_RETENCAO = get_RETENCAO_treated()
    df_RETENCAO.to_sql('retencao', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_NATUREZA = get_NATUREZA_treated()
    df_NATUREZA.to_sql('natureza', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_Flux_Cli = get_Flux_Cli_treated()
    df_Flux_Cli.to_sql('clientel', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_TP_ESTAB = get_TP_ESTAB_treated()
    df_TP_ESTAB.to_sql('tpunid', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_TurnosAt = get_TurnosAt_treated()
    df_TurnosAt.to_sql('turnoat', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_NIV_HIER = get_NIV_HIER_treated()
    df_NIV_HIER.to_sql('nivhier', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_Srv_Caract = get_Srv_Caract_treated()
    df_Srv_Caract.to_sql('caracter', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)

    df_NATJUR = get_NATJUR_treated()
    df_NATJUR.to_sql('natjur', con=device, schema=child_db, if_exists=label1, index=False, index_label=label2)


###########################################################################################################################################################################
# pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas pandas #
###########################################################################################################################################################################
###########################################################################################################################################################################
#  MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE * MAIN TABLE #
###########################################################################################################################################################################

# Função que utiliza para a inserção de dados principais da "child_db" o pandas.to_sql + SQLAlchemy
def insert_main_table_e_file_info_pandas(file_name, directory, date_ftp, device, child_db, parent_db):
    start = time.time()
    counting_rows = pd.read_sql('''SELECT COUNT('NOME') FROM %s.arquivos''' % (child_db), con=device)
    qtd_files_pg = counting_rows.iloc[0]['count']
    print(f'A quantidade de arquivos principais de dados do {child_db} já carregada no {parent_db}/PostgreSQL é {qtd_files_pg}.')

    # Tratamento de dados principais do CNES_SR
    state = file_name[2:4]
    year = file_name[4:6]
    month = file_name[6:8]
    main_table = 'srbr'
    counting_rows = pd.read_sql('''SELECT COUNT(*) from %s.%s''' % (child_db, main_table), con=device)
    n_rows = counting_rows.iloc[0]['count']
    print(f'\nIniciando a lida com o arquivo SR{state}{year}{month}...')
    # Chama a função "get_SRXXaamm_treated" do módulo "prepare_CNES_SR" do package "data_wrangling"
    df = get_SRXXaamm_treated(state, year, month)
    # Inserção das colunas UF_SR, ANO_SR e MES_SR no objeto pandas DataFrame "df"
    df.insert(1, 'UF_SR', [state]*df.shape[0])
    df.insert(2, 'ANO_SR', [int('20' + year)]*df.shape[0])
    df.insert(3, 'MES_SR', [month]*df.shape[0])
    df['CONTAGEM'] = np.arange(n_rows + 1, n_rows + 1 + df.shape[0])
    # Inserção dos dados da tabela principal no banco de dados "child_db"
    df.to_sql(main_table, con=device, schema=child_db, if_exists='append', index=False)
    print(f'Terminou de inserir os dados do arquivo SR{state}{year}{month} na tabela {main_table} do banco de dados {child_db}.')

    # Cria um objeto pandas DataFrame com apenas uma linha de dados, a qual contém informações sobre o arquivo de dados principal carregado
    file_data = pd.DataFrame(data=[[file_name, directory, date_ftp, datetime.today(), int(df.shape[0])]],
                             columns= ['NOME', 'DIRETORIO', 'DATA_INSERCAO_FTP', 'DATA_HORA_CARGA', 'QTD_REGISTROS'],
                             index=None
                             )
    # Inserção de informações do arquivo principal de dados no banco de dados "child_db"
    file_data.to_sql('arquivos', con=device, schema=child_db, if_exists='append', index=False)
    print(f'Terminou de inserir os metadados do arquivo SR{state}{year}{month} na tabela arquivos do banco de dados {child_db}.')
    end = time.time()
    print(f'Demorou {round((end - start)/60, 1)} minutos para essas duas inserções no {parent_db}/PostgreSQL pelo pandas!')
