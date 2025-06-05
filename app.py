import streamlit as st
import pandas as pd

st.title("Descriptive Statistics Viewer (CSV & Stata DTA)")

uploaded_file = st.file_uploader("Upload CSV or Stata DTA file", type=["csv", "dta"])

if uploaded_file is not None:
    filename = uploaded_file.name.lower()

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith('.dta'):
            df = pd.read_stata(uploaded_file)
        else:
            st.error("Unsupported file type.")
            st.stop()
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.write("### Data Preview")
    st.dataframe(df.head())

    column = st.selectbox("Select variable", df.columns)

    values = df[column].dropna()

    if pd.api.types.is_numeric_dtype(values):
        st.write("### Descriptive Statistics (Numeric)")
        st.write(values.describe())
    else:
        st.write("### Descriptive Statistics (Non-Numeric)")
        st.write(f"Unique values: {values.nunique()}")

    st.write("### Frequency Distribution")
    freq_table = values.value_counts().reset_index()
    freq_table.columns = ['Value', 'Frequency']
    st.dataframe(freq_table)
