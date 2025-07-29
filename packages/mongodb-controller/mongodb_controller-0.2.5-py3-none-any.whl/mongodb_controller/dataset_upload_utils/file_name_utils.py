from aws_s3_controller import scan_files_in_bucket_by_regex

def get_file_names_in_bucket(subject, regex):
    file_names = scan_files_in_bucket_by_regex(bucket='dataset-system', bucket_prefix=subject, regex=regex, option='name')
    return file_names

def get_menu2160_snapshot_file_names():
    regex = f'menu2160-code000000'
    file_names = get_file_names_in_bucket(subject='dataset-menu2160-snapshot', regex=regex)
    return file_names

def get_menu2205_snapshot_file_names():
    regex = f'menu2205-code000000'
    file_names = get_file_names_in_bucket(subject='dataset-menu2205-snapshot', regex=regex)
    return file_names

def get_menu2205_file_names(fund_code):
    regex = f'menu2205-code{fund_code}'
    file_names = get_file_names_in_bucket(subject='dataset-menu2205', regex=regex)
    return file_names

def extract_date_ref_in_file_name(file_name):
    date = file_name.split('-at')[1].split('-')[0]
    date = date[:4] + '-' + date[4:6] + '-' + date[6:8]
    return date

def extract_fund_code_in_file_name(file_name):
    fund_code = file_name.split('-code')[0].split('-')[1]
    return fund_code