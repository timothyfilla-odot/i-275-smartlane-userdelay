from ritis_api import *
from write_to_warehouse import *

if __name__ == '__main__':
    ritis_request(method='manual', start_date='2023-01-01', end_date='2023-06-30')
    ritis_request(method='manual', start_date='2023-07-01', end_date='2023-12-31')
    ritis_request(method='manual', start_date='2022-01-01', end_date='2022-06-30')
    ritis_request(method='manual', start_date='2022-07-01', end_date='2022-12-31')
    ritis_request(method='manual', start_date='2021-01-01', end_date='2021-06-30')
    ritis_request(method='manual', start_date='2021-07-01', end_date='2021-12-31')
    ritis_request(method='manual', start_date='2020-01-01', end_date='2020-06-30')
    ritis_request(method='manual', start_date='2020-07-01', end_date='2020-12-31')
    ritis_request(method='manual', start_date='2019-01-01', end_date='2019-06-30')
    ritis_request(method='manual', start_date='2019-07-01', end_date='2019-12-31')
    ritis_request(method='manual', start_date='2018-01-01', end_date='2018-06-30')
    ritis_request(method='manual', start_date='2018-07-01', end_date='2018-12-31')
    files_to_sql()
