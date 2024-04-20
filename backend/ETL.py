from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from MySQL import MySQL

class ETL:
    def __init__(self) -> None:
        pass

    def csv_load(self, data):
        try:
            df = pd.read_csv(data)
            # df.set_index('UniqueID', inplace=True)
            # specific_id = 'your_specific_id_value'
            # specific_row = df.loc[specific_id]

        except KeyError as e:
            return f'Error from csv_load : {e}'
        return df
    
    def sql_load(self,  table, db_name):
        try:
            query = f'SELECT * FROM {table}'
            sql = MySQL(db_name)
            df = sql.mysql_load(query)
        except KeyError as e:
            return f'Error from sql_load : {e}'
        return df
    
    def query_customer_info(self, UniqueID, table, db_name):
        try:
            query = f'SELECT * FROM {table} WHERE UNIQUEID = {UniqueID}'
            sql = MySQL(db_name)
            df = sql.mysql_load(query)
        except KeyError as e:
            return f'Error from query_customer_info : {e}'
        return df

    def columns_with_null(self, df):
        try:
            null_values = df.isnull().any()
            columns_with_null = null_values[null_values].index.tolist()
        except KeyError as e:
            return f'Error from columns_with_null : {e}'
        return columns_with_null


    def convert_to_mysql_datetime(self, df):
        try:
            if pd.api.types.is_datetime64_any_dtype(df['DISBURSAL_DATE']):
                pass  # Do nothing if already in datetime format
            else:
                df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], dayfirst=True).dt.strftime('%Y-%m-%d')
                
            if pd.api.types.is_datetime64_any_dtype(df['DATE_OF_BIRTH']):
                pass  # Do nothing if already in datetime format
            else:
                df['DATE_OF_BIRTH'] = pd.to_datetime(df['DATE_OF_BIRTH'], dayfirst=True).dt.strftime('%Y-%m-%d')
        except KeyError as e:
            return f'Error from convert_to_mysql_datetime: {e}'
        return df


    def fill_null_values(self, df):
        try:
            if not isinstance(df, pd.DataFrame):
                raise ValueError("Input must be a pandas DataFrame.")

            # Iterate over columns and fill null values
            for column in df.columns:
                if df[column].isnull().any():  # Check if any null values exist
                    if pd.api.types.is_numeric_dtype(df[column]):
                        fill_value = df[column].mean() if df[column].count() > 0 else None
                    elif pd.api.types.is_bool_dtype(df[column]):
                        fill_value = df[column].mode().iloc[0] if df[column].count() > 0 else None
                    elif pd.api.types.is_categorical_dtype(df[column]) or df[column].dtype == 'object':
                        fill_value = df[column].mode().iloc[0]
                    else:
                        raise ValueError(f"Unsupported data type in column '{column}'. Please provide a numeric, boolean, or categorical column.")

                    df[column] = df[column].fillna(fill_value)
        except KeyError as e:
            return f'Error from fill_null_values : {e}'

        return df

    def create_age_column(self, df):
        try:
            df['DISBURSAL_DATE'] = pd.to_datetime(df['DISBURSAL_DATE'], dayfirst=True)
            df['DATE_OF_BIRTH'] = pd.to_datetime(df['DATE_OF_BIRTH'], dayfirst=True)

            # Now you can perform arithmetic operations between datetime objects
            df['AGE'] = ((df['DISBURSAL_DATE'] - df['DATE_OF_BIRTH']).dt.days // 365)
        except KeyError as e:
            return f'Error from create_age_column : {e}'
        return df

    def convert_to_months(self, age):
        try:
            years, months = age.split(' ')
            years = int(years.replace('yrs', ''))
            months = int(months.replace('mon', ''))
            total_months = years * 12 + months
        except KeyError as e:
            return f'Error from convert_to_months : {e}'
        return total_months

    def convertToNumeric(self, sent):
        try:
            if 'Very High' in sent:
                return 5
            elif 'High' in sent:
                return 4
            elif 'Medium' in sent:
                return 3
            elif 'Low' in sent:
                return 2
            elif 'Very Low' in sent:
                return 1
            else:
                return 3
        except KeyError as e:
            print(f'Error from convertToNumeric : {e}')

    def encode_binary_categorical_column(self, df, column_name):
        try:
            encoder = LabelEncoder()
            encoder.fit(df[column_name])
            df_encoded = df.copy()
            df_encoded[column_name] = encoder.transform(df_encoded[column_name])
        except KeyError as e:
            print(f'Error from encode_binary_categorical_column : {e}')
        return df_encoded, encoder

   
    def transform(self, X=None, document_type='csv', sql_data=None):
        try:
            if document_type == 'csv':
                df = self.csv_load(X)
            elif document_type == 'sql':
                if sql_data is not None and 'table' in sql_data and 'db_name' in sql_data:
                    df = self.query_customer_info(sql_data['UniqueID'], sql_data['table'], sql_data['db_name'])
                else:
                    print("Error: Invalid SQL data provided.")
                    df = None
            else:
                print(f"Error: Invalid document type '{document_type}'.")
                df = None

            if df is not None:
                df = self.fill_null_values(df)
                df = self.create_age_column(df)
                df = self.convert_to_mysql_datetime(df)
                df['AVERAGE_ACCT_AGE'] = df['AVERAGE_ACCT_AGE'].apply(self.convert_to_months)
                df['CREDIT_HISTORY_LENGTH'] = df['CREDIT_HISTORY_LENGTH'].apply(self.convert_to_months)
                df['PERFORM_CNS_SCORE_DESCRIPTION'] = df['PERFORM_CNS_SCORE_DESCRIPTION'].apply(self.convertToNumeric)
                df, _ = self.encode_binary_categorical_column(df, 'EMPLOYMENT_TYPE')
                

        except KeyError as e:
            print(f'Error from transform: {e}')
            df = None

        return df



# Test
    
# elt = ETL()

# document_type = 'sql'
# sql_data = {'table': 'rawdata', 'db_name': 'data_warehouse', 'UniqueID': 655269}
# df = elt.transform(document_type=document_type, sql_data=sql_data)

# print(df)