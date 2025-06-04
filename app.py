import pandas as pd
import pyreadstat
import streamlit as st

st.title("SPSS File Descriptive Statistics Viewer")

# Load preloaded SPSS file
default_file_path = "example.sav"

df, meta = pyreadstat.read_sav(default_file_path)

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
