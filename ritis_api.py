import asyncio
from config_ud import seg_file
from util import *
from loguru import logger
import sys

sys.path.insert(1, r"\\itcfs007\Traffic_Management\Analytics_PerformanceMeasures\Python\API_Loaders\RITIS")

from api import userDelayCost
from ritis import prepare_request_intervals_in_range


def ritis_request(method, start_date='', end_date=''):
    logger.log('INFO', 'Preparing information for RITIS request...')

    date_range = find_date_range(method, start_date, end_date)

    segments = find_segs('tmc', seg_file)

    logger.log('INFO', 'Successfully compiled information. Making request for {start_date} to {end_date...')
    asyncio.run(userDelayCost(segments, date_range[0].isoformat(), date_range[1].isoformat(), "csv", 'ritis_files'))
    logger.log('INFO', 'Request successful; CSV files saved.')
