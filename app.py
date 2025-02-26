import streamlit as st
import pandas as pd
import os
from io import BytesIO
from sklearn.impute import KNNImputer #AI-based missing value handling
#set up our app
st.set_page_config(page_title="Data sweeper", layout='wide')

st.title("Data sweeper")
st.write("Transform your file between CSV and Excel formats with built_in data cleaning and visualization!")
# File upload option
uploaded_files= st.file_uploader("uplod you files (CSV or Excel):", type=["csv", "xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv" :
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
             df = pd.read_excel(file)
        else:
            st.error(f"Unsupport file type: {file_ext}")
            continue
        #Display about info the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f}KB")
        
        #show 5 rows of our df
        st.write("📊 **Preiew The Head of The DataFrame:**")
        st.dataframe(df.head())
       


        # Data Cleaning Options inside loop
        st.subheader(f"🛠Data Cleaning Option for {file.name}")
        if st.checkbox(f"Enable Clean data for {file.name}"):
            col1 , col2, col3 = st.columns(3)

            with col1:
                if st.button(f"🚀Remove Duplicate form {file.name}"):
                    before_rows = df.shape[0]
                    df.drop_duplicates(inplace=True)
                    after_rows = df.shape[0]
                    removed = before_rows - after_rows

                    st.success("✅ remover {removed} duplicate rows!")

            with col2:
                if st.button(f"File Missing Values (Mean) for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    
                    st.success("✅ Missing values filled using Mean!")
            with col3:
                if st.button(f"AI Fill Missing (KNN) for {file.name}"):
                 numeric_cols = df.select_dtypes(include=["number"]).columns
                 imputer = KNNImputer(n_neighbors=3) # AI-based Imputer
                 df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
                 st.success("✅ AI-based Missing Value Imputation Completed!")
                # ✅ Updated data preview inside loop
                st.write("📌 **Updated Data Preview:**")
                st.dataframe(df.head())

    #Choose specsific Colums to keep over convert
    st.subheader(f"📌select Columns to Convert for {file.name} ")
    columns = st.multiselect(f"Chose Colams for {file.name}", df.columns, default=df.columns)
    df = df[columns]

    #Create Some Visualization
    st.subheader(f"📊Data Visualization {file.name} ")
    if st.checkbox(f"show Visualizationfor {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        # Convwer a file  -> CSV to Excel
        st.subheader(f"📁 Conversion Options {file.name}")
        converstion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"convert {file.name}"):
            buffer = BytesIO()
            if converstion_type == "CSV":
                df.to_csv(buffer,index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif converstion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                #Download button
                st.download_button(
                    label=f"Download {file.name} as {converstion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                
                st.success("✅ File processed successfully!")




