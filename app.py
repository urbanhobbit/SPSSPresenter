import streamlit as st
import pandas as pd

st.title("Stata DTA Viewer with Labels")

uploaded_file = st.file_uploader("Upload Stata DTA file", type=["dta"])

if uploaded_file is not None:
    try:
        reader = pd.read_stata(uploaded_file, iterator=True)
        df = reader.read()
        value_labels = reader.value_labels()
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # Simulated variable labels (pandas cannot read variable labels)
    # We simply fall back to column names.
    variable_labels = {col: col for col in df.columns}

    # Build selection menu with variable labels
    var_options = [
        f"{variable_labels[var]} [{var}]" for var in df.columns
    ]
    selected_option = st.selectbox("Select a variable to analyze", var_options)
    selected_var = selected_option.split("[")[-1].strip("]")

    values = df[selected_var].dropna()

    # Apply value labels if exist
    label_dict = value_labels.get(selected_var, None)

    if label_dict:
        mapped_values = values.map(label_dict).fillna(values)
        display_series = mapped_values
    else:
        display_series = values

    # Descriptive statistics
    if pd.api.types.is_numeric_dtype(values):
        st.write("### Descriptive Statistics (Numeric)")
        st.write(values.describe())
    else:
        st.write("### Descriptive Statistics (Non-Numeric)")
        st.write(f"Unique values: {values.nunique()}")

    # Frequency distribution with value labels applied
    freq_table = display_series.value_counts(dropna=False).reset_index()
    freq_table.columns = ['Value Label', 'Frequency']
    st.write("### Frequency Distribution")
    st.dataframe(freq_table)
