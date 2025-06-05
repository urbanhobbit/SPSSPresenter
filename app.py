import streamlit as st
import pandas as pd
import json
from collections import Counter

st.title("CSV Viewer with Variable and Value Labels")

data_file = st.file_uploader("Upload CSV data file", type=["csv"])
varlabel_file = st.file_uploader("Upload variable labels JSON file", type=["json"])
vallabel_file = st.file_uploader("Upload value labels JSON file", type=["json"])

if data_file and varlabel_file and vallabel_file:
    # Load data
    df = pd.read_csv(data_file)

    # Load variable labels
    variable_labels = json.load(varlabel_file)

    # Load value labels
    value_labels = json.load(vallabel_file)

    # Variable selection with variable labels
    var_options = [
        f"{variable_labels.get(var, var)} [{var}]" for var in df.columns
    ]
    selected_option = st.selectbox("Select variable", var_options)
    selected_var = selected_option.split("[")[-1].strip("]")

    st.write(f"### Variable: {selected_var}")
    st.write(f"Label: {variable_labels.get(selected_var, '(no label)')}")

    series = df[selected_var].dropna()

    # Apply value labels if they exist
    label_dict = value_labels.get(selected_var, None)

    if label_dict:
        series_mapped = series.map(label_dict).fillna(series)
    else:
        series_mapped = series

    # Frequency table with percentages
    freq = Counter(series_mapped)
    total = sum(freq.values())
    freq_table = pd.DataFrame({
        "Value": list(freq.keys()),
        "Frequency": list(freq.values()),
        "Percentage": [round(v / total * 100, 2) for v in freq.values()]
    }).sort_values("Frequency", ascending=False)

    st.write("### Frequency Table")
    st.dataframe(freq_table)

    st.write("### Frequency Plot")
    st.bar_chart(freq_table.set_index("Value")["Frequency"])
