import streamlit as st
import pandas as pd
import statafile
from collections import Counter

st.title("Stata DTA Viewer with Full Labels (Pure Python Streamlit Cloud Compatible)")

uploaded_file = st.file_uploader("Upload Stata DTA file", type=["dta"])

if uploaded_file is not None:
    try:
        with statafile.open(uploaded_file) as dta:
            data = [row for row in dta]  # full data read
            var_names = dta.variable_names
            var_labels = dta.variable_labels
            value_labels = dta.value_labels
            label_sets = dta.value_label_sets
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Convert data to pandas DataFrame
    df = pd.DataFrame(data, columns=var_names)

    # Build selection menu with variable labels
    var_options = [
        f"{var_labels.get(var, var)} [{var}]" for var in var_names
    ]
    selected_option = st.selectbox("Select variable", var_options)
    selected_var = selected_option.split("[")[-1].strip("]")

    st.write(f"### Variable: {selected_var}")
    st.write(f"Label: {var_labels.get(selected_var, '(no label)')}")

    series = df[selected_var].dropna()

    # Apply value labels if exist
    label_name = value_labels.get(selected_var, None)
    label_dict = label_sets.get(label_name, None)

    if label_dict:
        mapped_series = series.map(label_dict).fillna(series)
    else:
        mapped_series = series

    # Frequency table with percentages
    freq = Counter(mapped_series)
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
