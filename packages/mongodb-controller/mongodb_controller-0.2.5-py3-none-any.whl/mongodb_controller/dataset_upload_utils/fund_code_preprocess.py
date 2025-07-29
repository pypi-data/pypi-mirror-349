import pandas as pd
import numpy as np 

def preprocess_fund_code(fund_code):
    if pd.isna(fund_code):
        fund_code = None
    elif isinstance(fund_code, float):
        fund_code = str(fund_code).replace('.0', '').zfill(6)
    elif isinstance(fund_code, str):
        fund_code = fund_code.zfill(6)
    elif isinstance(fund_code, int):
        fund_code = str(fund_code).zfill(6)
    elif isinstance(fund_code, np.number):
        fund_code = str(fund_code).replace('.0', '').zfill(6)
    return fund_code