"""General template validator."""
import re
import pandas as pd
import pandera as pa
import streamlit as st

AIMI_CATEGORIES = [
    '-',
    '1_Full_RBI',
    '2_Full_Traditional',
    '3_PCMS_Data_Validation_Only',
    '4_PCMS_Documentation_Record',
    '5_Piping',
    '6_Other'
]


def validate(df_input: pd.DataFrame, df_rules, df_picklists_map, schema_dict, check_empty, check_duplicate) -> pd.DataFrame:
    """Validate input table."""
    print(df_input.columns)
    print(df_rules['Column'].values)
    print()

    for index in df_rules.index:
        column = df_rules.loc[index]['Column']
        if column in schema_dict:
            continue

        field_type = df_rules.loc[index]['Data Type']
        print(field_type)
        
        if column in df_picklists_map:
            schema_dict[column] = \
                pa.Column(
                    checks=[check_picklist(df_picklists_map[column])], 
                    required=False
                    )
        elif 'Alpha/Numeric' in field_type:
            schema_dict[column] = pa.Column(checks=[check_alphanumeric()],
                                                    required=False)
        elif 'Numeric' in field_type:
            decimals = df_rules.loc[df_rules['Column'] == column,'Decimals'].iloc[0]
            schema_dict[column] = pa.Column(
                checks=[check_number(), check_decimals(decimals)],
                required=False
            )
        elif 'Date' in field_type:
            schema_dict[column] = pa.Column(checks=[check_date_format()], required=False)
        elif 'Y/N' in field_type:
            schema_dict[column] = pa.Column(checks=[check_picklist(["Y", "N"])], required=False)
        else:
            schema_dict[column] = pa.Column(required=False)

    dynamic_schema = pa.DataFrameSchema(
        columns=schema_dict,
        checks=[check_empty],
        unique_column_names=True,
        strict=True
    )

    try:
        dynamic_schema.validate(df_input.fillna('').astype(str), lazy=True)
        return pd.DataFrame()
    except pa.errors.SchemaErrors as e:
        replacements = {
            'field_uniqueness': 'Field is not unique',
            'column_in_dataframe': 'Missing mandatory column',
            'column_in_schema': 'Unknown column name',
        }
        error_df = pd.DataFrame(e.failure_cases[['column', 'check', 'failure_case', 'index']])
        error_df.fillna('', inplace=True)
        
        error_df['check'] = error_df['check'].replace(replacements)
        
        error_df = error_df.rename(
            columns={
                'column': 'Column', 'check': 'Error', 'failure_case': 'Value', 'index': 'Index'
            })

        error_df['Index'] = error_df['Index'].map(lambda x: int(x)+2 if str(x).isnumeric() else x)
        
        return error_df

def df_to_picklist_map(df: pd.DataFrame) -> dict:
        """Transform table to dictionary of picklists."""
        picklist_dict = df.to_dict(orient='list')
        data_dict_cleaned = {
            key: [value for value in values if pd.notna(value)]
            for key, values in picklist_dict.items()
        }
        return data_dict_cleaned

def check_uniqueness(val):
    """Verifies that a column has the same values."""
    return pa.Check(
        lambda x: x == val,
        error=f'All values must be equal to {val}',
        element_wise=True
    )

def check_valid_list(lst: list):
    """Verifies that a column has values only from the input list."""
    return pa.Check(
        lambda x: x in lst if lst else True,
        error='Value is not valid/does not exist',
        element_wise=True
    )

def check_picklist(valid_values: list[str]) -> pa.Check:
    """Verifies picklist compatibility of a column in a dataframe."""
    return pa.Check(
        check_fn=lambda x: x in valid_values,
        error='Value not in picklist',
        element_wise=True
    )

def check_date_format():
    """Verifies date format of a column in a dataframe."""
    def _check_date(date_string):
        """Internal helper function to check the date format."""
        try:
            pd.to_datetime(date_string, format='%m/%d/%Y')
            return True
        except (pd.errors.ParserError, ValueError):
            return False
    return pa.Check(_check_date, error='Invalid date format', element_wise=True)

def check_alphanumeric():
    """Verifies that column from a dataframe is alphanumeric, allows -, _, ., <space> characters"""
    return pa.Check(
        lambda x: bool(re.match('^[-A-Za-z0-9_. ]*$', x)),
        error='Value is not alphanumeric',
        element_wise=True
    )

def is_float(string):
    """Verifies if input is a number."""
    try:
        float(string)
        return True
    except ValueError:
        return False

def check_number():
    """Verifies that the column from a dataframe is numeric."""
    def _is_float(string):
        """Internal helper to verify that input is a number."""
        try:
            float(string)
            return True
        except ValueError:
            return False
    return pa.Check(
        check_fn=lambda s: _is_float(str(s)),
        error='Value is not a number',
        element_wise=True
    )

def check_decimals(decimals):
    """Verifies the number of decimal places in a number."""
    def _check_number_of_decimals(number, decimals):
        """Internal helper to check the number of decimals."""
        if not decimals.isnumeric():
            return True  # can have any number of decimals
        required_decimals = int(decimals)
        fractional_part = ''
        if '.' in number:
            _, fractional_part = number.split('.')
            if fractional_part == '0':
                fractional_part = ''
        if len(fractional_part) <= required_decimals:
            return True
        return False

    return pa.Check(
        check_fn=lambda s: _check_number_of_decimals(str(s), decimals),
        error=f'Number has more decimals than the allowed {decimals}',
        element_wise=True
    )

def validator(excel_file):
    print('here')

    path = r"C:\Users\dumit\OneDrive\Desktop\PY validator\excel validator\Equipment_Data_Mocked.xlsx"

    input_df = pd.read_excel(excel_file, sheet_name='Equipment Invalid')
    rules_df = pd.read_excel(excel_file, sheet_name='Data Types')
    picklist_df = pd.read_excel(excel_file, sheet_name='Picklists')
    valid_input_df = pd.read_excel(excel_file, sheet_name='Equipment Valid')

    primary_columns = [
        "Plant",
        "Equipment ID",
        "Description",
        "Type",
        "Category"
    ]


    id_column = 'Equipment ID'

    columns: list[str] = primary_columns
    df_picklists_map: dict[str, list[str]] = df_to_picklist_map(picklist_df)
    df_rules: pd.DataFrame = rules_df

    check_empty = \
        pa.Check(lambda x: x != '', error='Value cannot be empty', element_wise=True)
    check_duplicate = pa.Check(lambda x: ~x.duplicated(), error='Value is duplicated')

    schema_dict = {
        id_column: pa.Column(checks=[check_duplicate], required=True)
    }

    if 'AIMI Category' in columns:
        schema_dict['AIMI Category'] = \
            pa.Column(checks=[check_picklist(AIMI_CATEGORIES)], required=True)



    df_errors = validate(input_df, df_rules, df_picklists_map, schema_dict, check_empty, check_duplicate)

    # df_errors.to_excel("output.xlsx", index=False)

    return df_errors


