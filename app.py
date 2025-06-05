import streamlit as st
import pandas as pd
import json
from collections import Counter

# Embedded files
DATA_FILE = "example.csv"
VAR_LABEL_FILE = "variable_labels.json"
VAL_LABEL_FILE = "value_labels.json"

# Load everything
df = pd.read_csv(DATA_FILE, dtype=str)  # Load as string to avoid dtype issues
with open(VAR_LABEL_FILE, 'r', encoding='utf-8') as f:
    variable_labels = json.load(f)
with open(VAL_LABEL_FILE, 'r', encoding='utf-8') as f:
    value_labels = json.load(f)

st.title("CSV Viewer with Variable and Value Labels")

# Build mapping: var name → label
var_label_pairs = [
    (var, variable_labels.get(var, var)) for var in df.columns
]

# Create dropdown options: show label only
options = [f"{label} [{var}]" for var, label in var_label_pairs]
selected_option = st.selectbox("Select variable", options)

# Extract selected variable
selected_var = selected_option.split("[")[-1].strip("]")

# Show variable label on output
var_label = variable_labels.get(selected_var, selected_var)
st.subheader(f"Variable: {selected_var}")
st.write(f"Label: {var_label}")

# Prepare frequency table
series = df[selected_var].dropna()
label_dict = value_labels.get(selected_var, None)

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
