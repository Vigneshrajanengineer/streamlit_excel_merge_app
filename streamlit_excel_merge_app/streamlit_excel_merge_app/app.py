import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Excel Merger", layout="centered")

st.title("Merge Multiple Excel Files")

uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx", "xls"], accept_multiple_files=True)

sheet_name = st.text_input("Sheet name (optional)", value="")

if st.button("Merge Files") and uploaded_files:
    dfs = []
    for file in uploaded_files:
        try:
            df = pd.read_excel(file, sheet_name=sheet_name if sheet_name else 0)
            dfs.append(df)
        except Exception as e:
            st.error(f"Error with file {file.name}: {e}")

    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        output = BytesIO()
        merged_df.to_excel(output, index=False)
        output.seek(0)

        st.success("Files merged successfully!")
        st.download_button(
            label="Download Merged Excel",
            data=output,
            file_name="merged_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No valid files to merge.")