import pandas as pd

from util.postgres.dao_util import DaoPostgresSQL


class DaoSIH(DaoPostgresSQL):

    def __init__(self):
        super(DaoSIH, self).__init__(arquivo_configuracao='../util/postgres/config.yml')

    def get_df_descricao_procedimento(self):
        """
        Retorna as descrições dos procedimentos, bem como dos seus grupos, subgrupos e formas.
        :return:
        """
        sql = 'select p."PROCREA_ID", p."GRUPO", g."GRUPO" as DSC_GRUPO, p."SUBGRUPO", s."SUBGRUPO" as DSC_SUBGRUPO, ' \
              'p."FORMA" as COD_FORMA, f."FORMA" as DSC_FORMA, pr."PROCEDIMENTO" as DSC_PROC ' \
              'from sih_rd.rdbr p ' \
              'join sih_rd.grupo g on p."GRUPO" = g."ID" ' \
              'join sih_rd.subgrupo s on p."SUBGRUPO" = s."ID" ' \
              'join sih_rd.forma f on p."FORMA" = f."ID" ' \
              'join sih_rd.procrea pr on p."PROCREA_ID" = pr."ID"'
        df = pd.read_sql(sql, self.conexao)
        return df

    def get_df_populacao(self):
        sql = 'SELECT m."ID" as COD_MUNICIPIO, m."MUNNOME" NM_MUNICIPIO, uf."SIGLA_UF", pop."POPULACAO", m."RSAUDCOD" ' \
              'from ibge.POPULACAO pop ' \
              'join sih_rd.ufzi m on m."ID" = pop."ID" ' \
              'join sih_rd.ufcod uf on uf."ID" = m."UFCOD_ID"'
        df = pd.read_sql(sql, self.conexao)
        return df

    def get_df_coordenadas(self):
        """
        Retorna as coordenadas de cada municípios.
        :return:
        """
        sql = 'select "ID", "LATITUDE", "LONGITUDE" from sih_rd.ufzi where "LATITUDE" <> 0 and "LONGITUDE" <> 0'
        df = pd.read_sql(sql, self.conexao)
        return df

    def get_df_procedimentos_realizados_por_municipio(self, ano):
        """
        Retorna os procedimentos realizados agrpados por município.
        :param ano: O ano de realização.
        :return:
        """
        sql = 'select "ANO_RD", "PROCREA_ID", "UFZI_ID", count(*) as "QTD_PROCEDIMENTO",  sum("VAL_TOT") as "VL_TOTAL" ' \
              'from sih_rd.rdbr ' \
              'where "ANO_RD" = ' + str(ano) + ' and "IDENT_ID" = \'1\' ' \
                                               'group by "ANO_RD", "PROCREA_ID", "UFZI_ID"'
        df = pd.read_sql(sql, self.conexao)
        return df
