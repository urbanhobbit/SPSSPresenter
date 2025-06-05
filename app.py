import streamlit as st
import csv
import io
from collections import Counter
import statistics
import stata_reader  # pure Python package

st.title("Ultra-Simple Descriptive Statistics Viewer (CSV and Stata DTA files)")

uploaded_file = st.file_uploader("Upload your CSV or DTA file", type=["csv", "dta"])

if uploaded_file is not None:
    filename = uploaded_file.name.lower()

    if filename.endswith(".csv"):
        content = uploaded_file.read().decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(content))
        data = list(csv_reader)

    elif filename.endswith(".dta"):
        reader = stata_reader.read_dta(io.BytesIO(uploaded_file.read()))
        data = [dict(zip(reader.columns, row)) for row in reader]

    else:
        st.error("Unsupported file type.")
        st.stop()

    if not data:
        st.error("The file is empty.")
        st.stop()

    columns = list(data[0].keys())
    selected_column = st.selectbox("Select a variable", columns)

    values = [row[selected_column] for row in data if row[selected_column] not in ('', None)]

    st.write(f"Total valid entries: {len(values)}")

    # Try numeric conversion
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
