import pandas as pd
from loguru import logger
import sys
from datetime import date, timedelta, datetime


def find_segs(seg_type, file_name) -> dict:
    df = pd.read_csv(file_name)
    if seg_type == 'tmc':
        segments = {
                'ids': df['tmc'].to_list(),
                'type': 'tmc'
                }
        return segments
    elif seg_type == 'xd':
        segments = {
                'ids': [str(x) for x in df['Segment ID'].to_list()],
                'type': 'xd'
                }
        return segments
    else:
        logger.log('ERROR', 'Invalid segment type provided.')
        sys.exit('Invalid parameters.')


def find_date_range(method, start_date, end_date) -> tuple:
    if method == 'manual':
        if not start_date or not end_date:
            logger.log('ERROR', 'Provide start_date and end_date parameters.')
            sys.exit('Insufficient parameters supplied.')
        date_tup = (date.fromisoformat(start_date), date.fromisoformat(end_date))
    elif method == 'weekly':
        date_tup = ((datetime.now() - timedelta(days=9)).date(), (datetime.now() - timedelta(days=3)).date())
    else:
        logger.log('ERROR', "Invalid request method specified. Use 'manual' with two dates as following arguments, or "
                            "'weekly' to run last week.")
        sys.exit('Invalid parameters.')

    return date_tup
