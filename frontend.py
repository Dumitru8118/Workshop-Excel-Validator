import re
import pandas as pd
import pandera as pa
import streamlit as st
from io import BytesIO
from excel_validator import validator



st.title('Excel Data Validator')

file_uploaded = st.file_uploader('Upload an excel file:', type = 'xlsx')

insert_excel_button = st.button(
    label = "Validate Excel file",
    use_container_width=True,
    type='primary',
    disabled=file_uploaded is None
)

if insert_excel_button:
    excel_file = pd.ExcelFile(file_uploaded)
    uploaded_df = pd.read_excel(file_uploaded, dtype = str, keep_default_na=False)
    res = validator(
        excel_file
    )
    if res.empty:
        st.success('Uploaded table is valid and the data was succesfully updated!')
    else:
        st.error('Uploaded template is invalid!')
        res.sort_index(inplace=True)

        # download errors table as Excel
        output1 = BytesIO()
        writer1 = pd.ExcelWriter(output1, engine='xlsxwriter')
        res.to_excel(writer1, header=True, index=False)
        writer1.close()
        st.download_button(
            label = 'Download Validation Errors as Excel',
            data = output1.getvalue(),
            file_name = 'Validation Errors.xlsx',
            mime = "application/vnd.ms-excel",
            use_container_width = True
        )

        # display list of errors in app
        ERRORS_MARKDOWN = 'The following validation errors were found:\n'
        for _, row in res.iterrows():
            if str(row['Index']).isnumeric():
                error_message = \
                    f'In column *{row["Column"]}* line {int(row["Index"])}, ' +\
                        f'entry *{row["Value"]}: *{row["Error"]}'
            else:
                error_message = f'Problem with *{row["Value"]}: *{row["Error"]}'
            ERRORS_MARKDOWN += '- ' + error_message + '\n'
        st.error(ERRORS_MARKDOWN)