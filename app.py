import streamlit as st
import pandas as pd
import json
from collections import Counter

# Embed files directly into the app
DATA_FILE = "example.csv"
VAR_LABEL_FILE = "variable_labels.json"
VAL_LABEL_FILE = "value_labels.json"

# Load data (embedded)
df = pd.read_csv(DATA_FILE)
with open(VAR_LABEL_FILE, 'r', encoding='utf-8') as f:
    variable_labels = json.load(f)
with open(VAL_LABEL_FILE, 'r', encoding='utf-8') as f:
    value_labels = json.load(f)

st.title("CSV Viewer with Embedded Variable and Value Labels")

# Build dropdown using variable labels
var_options = [
    f"{variable_labels.get(var, var)} [{var}]" for var in df.columns
]
selected_option = st.selectbox("Select variable", var_options)
selected_var = selected_option.split("[")[-1].strip("]")

# Display selected variable label
st.subheader(f"Variable: {selected_var}")
st.write(f"Label: {variable_labels.get(selected_var, '(no label)')}")

series = df[selected_var].dropna()
label_dict = value_labels.get(selected_var, None)

# Apply value labels if available
if label_dict:
    series_mapped = series.map(label_dict).fillna(series)
else:
    series_mapped = series

# Build frequency table
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
