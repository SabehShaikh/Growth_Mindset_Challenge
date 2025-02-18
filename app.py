import streamlit as st
import pandas as pd
import os 
from io import BytesIO 

# Set up the app:
st.set_page_config(page_title="Q3 Assignment 01", layout="wide")

st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            continue

        # Display file info
        st.write(f"**File Name:** {uploaded_file.name}")
        st.write(f"**File Size:** {uploaded_file.size / 1024:.2f} KB")
        
        # Display the first 5 rows
        st.write("### Preview of the First 5 Rows")
        st.dataframe(df.head())

        # Sidebar for data cleaning options
        st.sidebar.subheader(f"Data Cleaning Options - {uploaded_file.name}")
        if st.sidebar.checkbox(f"Clean data for {uploaded_file.name}"):
            if st.sidebar.button(f"Remove Duplicates - {uploaded_file.name}"):
                df.drop_duplicates(inplace=True)
                st.sidebar.success("Duplicates Removed!")

            if st.sidebar.button(f"Fill Missing Values - {uploaded_file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.sidebar.success("Missing values filled!")

        # Select specific columns to keep
        st.sidebar.subheader(f"Select Columns for {uploaded_file.name}")
        columns = st.sidebar.multiselect(f"Choose columns", df.columns, default=df.columns)
        df = df[columns]  

        # Data visualization
        st.sidebar.subheader(f"📊 Data Visualization - {uploaded_file.name}")
        if st.sidebar.checkbox(f"Show Visualization for {uploaded_file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File conversion
        st.sidebar.subheader(f"🔄 Conversion Options - {uploaded_file.name}")
        conversion_type = st.sidebar.radio(f"Convert {uploaded_file.name} to", ("CSV", "Excel"))
        if st.sidebar.button(f"Convert {uploaded_file.name} to {conversion_type}"):
            buffer = BytesIO()
            new_filename = uploaded_file.name.replace(file_ext, f".{conversion_type.lower()}")
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.sidebar.download_button(
                label=f"Download {new_filename}",
                data=buffer,
                file_name=new_filename,
                mime=mime_type
            )

st.success("All files processed successfully!")
