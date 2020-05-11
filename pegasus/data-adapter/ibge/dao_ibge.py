from util.postgres.dao_util import DaoPostgresSQL
import pandas as pd


class DaoIBGE(DaoPostgresSQL):
    def __init__(self):
        super(DaoIBGE, self).__init__(arquivo_configuracao='../util/postgres/config.yml')

    def get_df_populacao_municipios(self):
        """
        Retorna a população (estimada) de cada município.
        :return:
        """
        sql = 'SELECT m."ID" as COD_MUNICIPIO, m."MUNNOME" NM_MUNICIPIO, uf."SIGLA_UF", pop."POPULACAO", m."RSAUDCOD" ' \
              'from ibge.populacao_municipio pop ' \
              'join sih_rd.ufzi m on m."ID" = pop."ID" ' \
              'join sih_rd.ufcod uf on uf."ID" = m."UFCOD_ID"'
        df = pd.read_sql(sql, self.conexao)
        return df

    def get_df_populacao_ufs(self):
        """
        Retorna a população (estimada) de cada unidade da federação.
        :return:
        """
        sql = 'SELECT * FROM ibge.populacao_uf'
        df = pd.read_sql(sql, self.conexao)
        return df


if __name__ == '__main__':
    dao = DaoIBGE()

    df = dao.get_df_populacao_municipios()
    print(df.head())

    df = dao.get_df_populacao_ufs()
    print(df.head())
