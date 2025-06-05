import streamlit as st
import csv
import io
from collections import Counter
import statistics

st.title("Ultra-Simple Descriptive Statistics Viewer (Streamlit Cloud Compatible)")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(content))
    data = list(csv_reader)

    if not data:
        st.error("The file is empty.")
        st.stop()

    columns = list(data[0].keys())
    selected_column = st.selectbox("Select a variable", columns)

    values = [row[selected_column] for row in data if row[selected_column] != '']
    st.write(f"Total valid entries: {len(values)}")

    # Try to convert to numbers if possible
    try:
        numeric_values = list(map(float, values))
        st.write("### Descriptive Statistics")
        st.write(f"Mean: {statistics.mean(numeric_values):.3f}")
        st.write(f"Median: {statistics.median(numeric_values):.3f}")
        st.write(f"Std Dev: {statistics.stdev(numeric_values):.3f}")
    except:
        st.write("### Descriptive Statistics (non-numeric data)")
        st.write(f"Unique Values: {len(set(values))}")

    st.write("### Frequency Distribution")
    freq = Counter(values)
    freq_table = [{"Value": k, "Frequency": v} for k, v in freq.items()]
    st.write(freq_table)
