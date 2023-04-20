import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlalchemy
from datetime import date


class ETL:

    def __init__(self, plaza_id, sql_credential, sql_table_name):
        self.plaza_id = plaza_id
        self.credential = sql_credential
        self.sql_table_name = sql_table_name
        self.url = f'https://tis.nhai.gov.in/TollInformation.aspx?TollPlazaID={self.plaza_id}'
        self.soup = ''
        self.df_info = pd.DataFrame

    def extract(self):
        r = requests.get(self.url)
        self.soup = BeautifulSoup(r.text, 'html.parser')
        if self.soup.find(class_='PA15'):
            return True
        return False

    def transform(self):
        plaza_name = self.soup.find(class_='PA15').find_all('p')[0].find('lable')
        table_html = str(self.soup.find_all('table', class_='tollinfotbl')[0])
        df_info = pd.read_html(table_html)[0].dropna(axis=0, how='all')
        cols = df_info.columns.tolist()
        cols.insert(0, 'Date_Scrapped')
        cols.insert(1, 'Plaza_Name')
        cols.insert(2, 'toll_plaza_id')
        df_info['Plaza_Name'] = plaza_name.text
        df_info['Date_Scrapped'] = date.today()
        self.df_info = df_info[cols]
        print(self.df_info)

    def load(self):
        db = sqlalchemy.create_engine(self.sql_credential)
        conn = db.connect()
        self.df_info.to_sql(self.sql_table_name, conn, if_exists='append', index=False)

    def run_etl(self):
        if self.extract():
            self.transform()
            self.load()
            print(f'Done with of plaza_id{self.plaza_id}')
        else:
            print(f'Skipped plaza_id {self.plaza_id}')
