from etl import ETL
from feach_plaza_ids import get_all_plaza_ids
from datetime import date
import concurrent.futures
from functools import partial


def create_etl_object_and_run(plaza_id, db_credential, db_table_name):
    plaza_etl = ETL(plaza_id, db_credential, db_table_name)
    plaza_etl.run_etl()


if __name__ =="__main__":
    db_credential = "postgresql://postgres:admin@localhost/nhai"
    db_table_name = f'nhai_toll_plaza_{date.today()}'
    ids = get_all_plaza_ids()
    partial_etl_function = partial(create_etl_object_and_run, db_credential = db_credential, db_table_name = db_table_name)
    with concurrent.futures.ThreadPoolExecutor(10) as executor:
        executor.map(partial_etl_function,ids)