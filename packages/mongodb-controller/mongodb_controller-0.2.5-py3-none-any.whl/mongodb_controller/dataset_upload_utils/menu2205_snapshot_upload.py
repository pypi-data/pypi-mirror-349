from aws_s3_controller import scan_files_in_bucket_by_regex, open_df_in_bucket_by_regex
from .fund_code_preprocess import preprocess_fund_code, get_menu2205_snapshot_file_names
from .file_name_utils import get_menu2205_snapshot_file_names, extract_date_ref_in_file_name
from ..mongodb_connector import client
from ..mongodb_basis import insert_data_in_collection

DATABASE_NAME = 'database-FMBOS'
COLLECTION_NAME = 'dataset-menu2205-snapshot'
BUCKET_PREFIX = COLLECTION_NAME
FILE_NAMES_MENU2205_SNAPSHOT = get_menu2205_snapshot_file_names()

collection = client[DATABASE_NAME][COLLECTION_NAME]

def upload_menu2205_snapshot_to_mongodb(collection, date_ref=None):
    regex = f'menu2205-code000000-at{extract_date_ref_in_file_name(file_name)}' if date_ref else f'menu2205-code000000'
    file_names = scan_files_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=BUCKET_PREFIX, regex=regex, option='name')
    df = open_df_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=BUCKET_PREFIX, regex=file_names[-1])
    data_by_date = map_df_to_data(df)
    data = {'date_ref': date_ref, 'data': data_by_date}
    insert_data_in_collection(data, collection)
    return None

