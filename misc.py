from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import urllib.request 
import json
from tqdm import tqdm
import requests

def generate_months(start_month, end_month):
    
	start_date = datetime.strptime(start_month, "%Y%m")
	end_date = datetime.strptime(end_month, "%Y%m")

	months_list = []

	current_date = start_date
	while current_date <= end_date:
		new_month = 'EPD_'+str(current_date.strftime("%Y%m"))
		months_list.append(new_month)
		current_date += relativedelta(months=1)

	return months_list

def get_month_data(resource_name):

	base_endpoint = 'https://opendata.nhsbsa.net/api/3/action/'
	package_list_method = 'package_list'
	package_show_method = 'package_show?id='
	action_method = 'datastore_search_sql?' 

	used_columns = ['TOTAL_QUANTITY', 'YEAR_MONTH', 'POSTCODE', 'PRACTICE_CODE', 'REGIONAL_OFFICE_NAME', 'BNF_DESCRIPTION']
	substance = 'Salbutamol' 
	bnf_description = '2.5mg'

	single_month_query = f'''
		SELECT {', '.join(used_columns)} 
		FROM `{resource_name}`
		WHERE chemical_substance_bnf_descr = '{substance}'
		  AND (bnf_description LIKE '%2.5mg%')
		  AND NOT unidentified
		'''

	urllib.parse.quote(single_month_query)

	single_month_api_call = f"{base_endpoint}" \
					f"{action_method}" \
					"resource_id=" \
					f"{resource_name}" \
					"&" \
					"sql=" \
					f"{urllib.parse.quote(single_month_query)}"


	json_data = requests.get(single_month_api_call).json()
	
	if json_data['success'] == False:
		raise KeyError(f"The Inputted Key {resource_name} is Incorrect")

	records = json_data['result']['result']['records']
	
	month_df = pd.DataFrame(records)

	return month_df


def preprocessing(df:pd.DataFrame, verbose:int=1):

	try:
		df['YEAR_MONTH'] = pd.to_datetime(df['YEAR_MONTH'].astype(str), format='%Y%m')
	except:
		print('YEAR_MONTH is in the correct format.')

	n = df.shape[0]
	print('Start Number of Rows:', n)

	nas_dropped_df = df.dropna(inplace=False)
	m = df.shape[0] - nas_dropped_df.shape[0]
	print('Number of Rows with NAs Dropped:', m)
	
	no_duplicates_df = nas_dropped_df.drop_duplicates(inplace=False)
	m = no_duplicates_df.shape[0] - nas_dropped_df.shape[0]
	print('Number of Duplicate Rows Dropped:', m)

	no_duplicates_df.drop(columns=['Unnamed: 0'], inplace=True)

	n, m = no_duplicates_df.shape
	print('Processed Number of Rows:', n)
	print('Processed Number of Columns:', m)

	return no_duplicates_df