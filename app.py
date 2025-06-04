import pandas as pd
import pyreadstat
import streamlit as st
import tempfile
import os

st.title("SPSS & Stata File Descriptive Statistics Viewer")

uploaded_file = st.file_uploader("Upload your SPSS (.sav) or Stata (.dta) file", type=["sav", "dta"])

if uploaded_file is not None:
    suffix = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    if suffix == ".sav":
        df, meta = pyreadstat.read_sav(tmp_file_path)
    elif suffix == ".dta":
        df, meta = pyreadstat.read_dta(tmp_file_path)
    else:
        st.error("Unsupported file type.")
        st.stop()

    st.write("### Data Preview")
    st.dataframe(df.head())

    variables = meta.column_names
    labels = meta.column_labels

    variable_options = []
    for var, label in zip(variables, labels):
        display_label = label if label else var
        variable_options.append(f"{display_label} [{var}]")

    selected_option = st.selectbox("Select a variable to analyze", variable_options)
    selected_variable = selected_option.split('[')[-1].strip(']')

    st.write(f"### Descriptive Statistics for {selected_variable}")
    st.dataframe(df[selected_variable].describe())

    st.write(f"### Frequency Distribution for {selected_variable}")

    # Extract value labels (works for both SPSS and Stata)
    value_label_set = meta.variable_value_labels.get(selected_variable, None)

    if isinstance(value_label_set, dict):
        value_labels_dict = value_label_set
    elif isinstance(value_label_set, str):
        value_labels_dict = meta.value_labels.get(value_label_set, {})
    else:
        value_labels_dict = {}

    if value_labels_dict:
        df_display = df[selected_variable].map(value_labels_dict).fillna(df[selected_variable])
        freq_table = df_display.value_counts(dropna=False).reset_index()
        freq_table.columns = ['Value Label', 'Frequency']
    else:
        freq_table = df[selected_variable].value_counts(dropna=False).reset_index()
        freq_table.columns = ['Value', 'Frequency']

    st.dataframe(freq_table)
    st.bar_chart(freq_table.set_index(freq_table.columns[0])['Frequency'])
