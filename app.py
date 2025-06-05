import streamlit as st
import pandas as pd
import pyreadstat

st.title("Full Descriptive Statistics Viewer with Labels")

uploaded_file = st.file_uploader("Upload SPSS (.sav) or Stata (.dta) file", type=["sav", "dta"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.sav'):
            df, meta = pyreadstat.read_sav(uploaded_file)
        elif uploaded_file.name.endswith('.dta'):
            df, meta = pyreadstat.read_dta(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Create dropdown with variable labels
    variable_options = [
        f"{meta.column_labels[i]} [{var}]" if meta.column_labels[i] else var
        for i, var in enumerate(meta.column_names)
    ]

    selected_option = st.selectbox("Select variable", variable_options)
    selected_var = selected_option.split("[")[-1].strip("]")

    # Display selected variable label
    var_label = meta.column_labels[meta.column_names.index(selected_var)]
    st.subheader(f"Variable: {selected_var}")
    if var_label:
        st.write(f"Label: {var_label}")

    series = df[selected_var].dropna()

    # Apply value labels if they exist
    value_label_set = meta.variable_value_labels.get(selected_var, None)
    if isinstance(value_label_set, dict):
        display_series = series.map(value_label_set).fillna(series)
    else:
        display_series = series

    # Frequency table with percentages
    freq_table = display_series.value_counts(dropna=False).reset_index()
    freq_table.columns = ['Value Label', 'Frequency']
    freq_table['Percentage'] = (freq_table['Frequency'] / freq_table['Frequency'].sum() * 100).rou*_
