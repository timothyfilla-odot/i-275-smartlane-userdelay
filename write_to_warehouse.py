import pandas as pd
import numpy as np
import os
import shutil
from loguru import logger
from config_ud import warehouse_table
from tsmo_db.db_factory import DbFactory, DbTypes, VaultConnectionType
from tqdm import tqdm
from math import ceil, isnan
import json

engine = DbFactory.get_provider(DbTypes.AZURE_SYNAPSE, VaultConnectionType.SQL_SERVER).get_engine()


def files_to_sql():
    for dirpath, dirs, files in os.walk(os.getcwd() + '\\ritis_files'):
        csv_files = [f for f in files if f.endswith('.csv')]
        for file in csv_files:
            logger.log('INFO', 'Attempting to warehouse ' + file)
            path = os.path.join(dirpath, file)
            df = pd.read_csv(path, index_col=0)
            df['tmcGroup'] = 'I-275 Phase 1'
            df = df.replace({np.nan: -99})
            df['Hour'] = df['Hour'].astype('int32')
            with engine.begin() as con:
                for i in tqdm(range(ceil(df.shape[0] / 1000) + 1)):
                    json_string = json.dumps(df.iloc[i * 1000: (i + 1) * 1000].to_dict('records'))
                    con.execute(f"""
                                INSERT INTO {warehouse_table}
                                SELECT *
                                FROM OPENJSON('{json_string}')
                                    WITH (
                                        Date date '$.Date',
                                        DailyOrHourly varchar(10) '$.DailyOrHourly',
                                        VehicleType varchar(10) '$.VehicleType',
                                        Hour int '$.Hour',
                                        Volume decimal(38,10) '$.Volume',
                                        DelayPersonHours decimal(38,10) '$.DelayPersonHours',
                                        DelayCost decimal(38,10) '$.DelayCost',
                                        DelayVehicleHours decimal(38,10) '$.DelayVehicleHours',
                                        VMT decimal(38,10) '$.VMT',
                                        tmcGroup varchar(100) '$.tmcGroup'
                                    )
                                """)
            shutil.move(path, os.path.join(os.getcwd(), 'loaded', file))
            engine.execute('UPDATE [dbo].[RitisPerfMeas_UDC] SET Hour = NULL WHERE Hour = -99')
            logger.log('INFO', 'Loaded ' + file)
