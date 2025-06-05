import pandas as pd
import streamlit as st

st.title("Simple Descriptive Statistics Viewer")

uploaded_file = st.file_uploader("Upload your dataset (.csv or .dta)", type=["csv", "dta"])

if uploaded_file is not None:
    # Try reading file depending on extension
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
        st.error(f"Error reading file: {e}")
        st.stop()

    st.write("### Data Preview")
    st.dataframe(df.head())

    # Variable selection
    selected_variable = st.selectbox("Select a variable to analyze", df.columns)

    st.write(f"### Descriptive Statistics for {selected_variable}")
    st.write(df[selected_variable].describe())

    st.write(f"### Frequency Distribution for {selected_variable}")
    freq_table = df[selected_variable].value_counts(dropna=False).reset_index()
    freq_table.columns = ['Value', 'Frequency']
    st.dataframe(freq_table)

    st.bar_chart(freq_table.set_index('Value')['Frequency'])
