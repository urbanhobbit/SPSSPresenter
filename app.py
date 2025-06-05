import streamlit as st
import pandas as pd

st.title("Descriptive Statistics Viewer (CSV & Stata DTA with Value Labels)")

uploaded_file = st.file_uploader("Upload CSV or Stata DTA file", type=["csv", "dta"])

if uploaded_file is not None:
    filename = uploaded_file.name.lower()

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            value_labels = {}  # No labels in CSV
        elif filename.endswith('.dta'):
            # Use iterator to access value labels
            reader = pd.read_stata(uploaded_file, iterator=True)
            df = reader.read()
            value_labels = reader.value_labels()
        else:
            st.error("Unsupported file type.")
            st.stop()
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    # Display data preview safely
    df_display = df.astype(str)
    st.write("### Data Preview")
    st.dataframe(df_display.head())

    # Display value labels if any
    if value_labels:
        st.write("### Value Labels (from Stata file)")
        for var, labels in value_labels.items():
            st.write(f"**{var}**: {labels}")

    # Variable selector
    column = st.selectbox("Select variable", df.columns)
    values = df[column].dropna()

    # Descriptive stats
    if pd.api.types.is_numeric_dtype(values):
        st.write("### Descriptive Statistics (Numeric)")
        st.write(values.describe())
    else:
        st.write("### Descriptive Statistics (Non-Numeric)")
        st.write(f"Unique values: {values.nunique()}")

    # Frequency distribution
    freq_table = values.value_counts().reset_index()
    freq_table.columns = ['Value', 'Frequency']
    st.write("### Frequency Distribution")
    st.dataframe(freq_table)
