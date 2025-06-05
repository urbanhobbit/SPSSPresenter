import pandas as pd
import streamlit as st

st.title("Stata File Descriptive Statistics Viewer (Streamlit Cloud Safe)")

uploaded_file = st.file_uploader("Upload your Stata (.dta) file", type=["dta"])

if uploaded_file is not None:
    df = pd.read_stata(uploaded_file)

    st.write("### Data Preview")
    st.dataframe(df.head())

    selected_variable = st.selectbox("Select a variable to analyze", df.columns)

    st.write(f"### Descriptive Statistics for {selected_variable}")
    st.dataframe(df[selected_variable].describe())

    st.write(f"### Frequency Distribution for {selected_variable}")
    freq_table = df[selected_variable].value_counts(dropna=False).reset_index()
    freq_table.columns = ['Value', 'Frequency']
    st.dataframe(freq_table)
    st.bar_chart(freq_table.set_index('Value')['Frequency'])
