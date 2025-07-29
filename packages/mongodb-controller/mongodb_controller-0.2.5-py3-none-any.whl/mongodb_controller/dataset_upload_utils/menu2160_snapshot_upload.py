from aws_s3_controller import scan_files_in_bucket_by_regex, open_df_in_bucket_by_regex
from .fund_code_preprocess import preprocess_fund_code, get_menu2160_snapshot_file_names
from ..mongodb_connector import client
from ..mongodb_basis import insert_many_data_in_collection

DATABASE_NAME = 'database-FMBOS'
COLLECTION_NAME = 'dataset-menu2160-snapshot'
BUCKET_PREFIX = COLLECTION_NAME
FILE_NAMES_MENU2160_SNAPSHOT = get_menu2160_snapshot_file_names()

collection = client[DATABASE_NAME][COLLECTION_NAME]


def upload_menu2160_snapshot_to_mongodb(collection, date_ref=None):
    regex = f'menu2160-code000000-at{date_ref.replace("-","")}' if date_ref else f'menu2160-code000000'
    file_names = scan_files_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=BUCKET_PREFIX, regex=regex, option='name')
    df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=BUCKET_PREFIX, regex=file_names[-1])
    df['펀드'] = df['펀드'].apply(preprocess_fund_code)
    data = map_df_to_data(df)
    insert_many_data_in_collection(data, collection)
    return None

def upload_menu2160_snapshot_to_mongodb_by_file_name(file_name):
    df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix='dataset-menu2160-snapshot', regex=file_name)
    df['펀드'] = df['펀드'].apply(preprocess_fund_code)
    data = map_df_to_data(df)
    insert_many_data_in_collection(data, collection)
    return None

def upload_menu2160_snapshots_to_mongodb(file_names):
    for file_name in file_names:
        upload_menu2160_snapshot_to_mongodb_by_file_name(file_name)
    return None
