import streamlit as st
import pandas as pd
import json
from collections import Counter
import matplotlib.pyplot as plt

# Embedded files
DATA_FILE = "example.csv"
VAR_LABEL_FILE = "variable_labels.json"
VAL_LABEL_FILE = "value_labels.json"

# Load data
df = pd.read_csv(DATA_FILE, dtype=str)
with open(VAR_LABEL_FILE, 'r', encoding='utf-8') as f:
    variable_labels = json.load(f)
with open(VAL_LABEL_FILE, 'r', encoding='utf-8') as f:
    value_labels = json.load(f)

# Normalize keys
df.columns = df.columns.astype(str).str.strip()
variable_labels = {str(k).strip(): v for k, v in variable_labels.items()}
value_labels = {str(k).strip(): {str(kk).strip(): vv for kk, vv in v.items()} for k, v in value_labels.items()}

# Sidebar variable selection
st.sidebar.header("Select Variable")
var_options = [f"{variable_labels.get(var, var)} [{var}]" for var in df.columns]
selected_option = st.sidebar.selectbox("Variable", var_options)
selected_var = selected_option.split("[")[-1].strip("]")
var_label = variable_labels.get(selected_var, selected_var)

# Main UI
st.title("📊 Survey Data Viewer")
st.subheader(var_label)

# Frequency analysis
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
    "Percentage": [round(v / total * 100, 1) for v in freq.values()]
}).sort_values("Frequency", ascending=False)

st.write("### Frequency Table")
st.dataframe(freq_table.style.format({"Percentage": "{:.1f}%"}))

# Plot
st.write("### Distribution")
fig, ax = plt.subplots(figsize=(8, 5))
freq_table.plot.barh(x="Value", y="Frequency", ax=ax, color="#4C72B0", legend=False)
plt.xlabel("Frequency")
plt.ylabel("")
plt.gca().invert_yaxis()
st.pyplot(fig)
