import streamlit as st
import pandas as pd
import json
from collections import Counter

# Embedded files (relative paths)
DATA_FILE = "example.csv"
VAR_LABEL_FILE = "variable_labels.json"
VAL_LABEL_FILE = "value_labels.json"

# Load everything
df = pd.read_csv(DATA_FILE, dtype=str)
with open(VAR_LABEL_FILE, 'r', encoding='utf-8') as f:
    variable_labels = json.load(f)
with open(VAL_LABEL_FILE, 'r', encoding='utf-8') as f:
    value_labels = json.load(f)

# Normalize keys to ensure perfect matching
df.columns = df.columns.str.strip()
variable_labels = {k.strip(): v for k, v in variable_labels.items()}
value_labels = {k.strip(): {str(kk): vv for kk, vv in v.items()} for k, v in value_labels.items()}

st.title("CSV Viewer with Variable and Value Labels")

# Build dropdown using variable labels
var_options = [
    f"{variable_labels.get(var, var)} [{var}]" for var in df.columns
]
selected_option = st.selectbox("Select variable", var_options)
selected_var = selected_option.split("[")[-1].strip("]")

# Display selected variable label
var_label = variable_labels.get(selected_var, selected_var)
st.subheader(f"Variable: {selected_var}")
st.write(f"Label: {var_label}")

series = df[selected_var].dropna()
label_dict = value_labels.get(selected_var, None)

# Apply value labels if available
if label_dict:
    series_mapped = series.map(label_dict).fillna(series)
else:
    series_mapped = series

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
