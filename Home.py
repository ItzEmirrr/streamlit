import streamlit as st
import pygwalker as pyg
import pandas as pd
import sys

st.set_page_config(page_title='APP', page_icon=":smiley", layout="wide")


st.write()

st.markdown("<h1 style='text-align: center;'>Some app</h1>", unsafe_allow_html=True)

st.sidebar.write("****File upload****")

ft = st.sidebar.selectbox("*What is the file type?*", ["Excel", "csv"])

uploaded_file = st.sidebar.file_uploader("*Upload file here*")

if uploaded_file is not None:
    file_path = uploaded_file

    if ft == 'Excel':
        try:
            sh = st.sidebar.selectbox("*Which sheet name in the file should be read?*",
                                      pd.ExcelFile(file_path).sheet_names)
            h = st.sidebar.number_input("*Which row contains the column names?*", 0, 100)
        except:
            st.info("File is not recognised as an Excel file")
            sys.exit()

    elif ft == 'csv':
        try:
            sh = None
            h = None
        except:
            st.info("File is not recognised as a csv file.")
            sys.exit()


    @st.cache_data(experimental_allow_widgets=True)
    def load_data(file_path, ft, sh, h):

        if ft == 'Excel':
            try:
                data = pd.read_excel(file_path, header=h, sheet_name=sh, engine='openpyxl')
            except:
                st.info("File is not recognised as an Excel file.")
                sys.exit()

        elif ft == 'csv':
            try:
                data = pd.read_csv(file_path)
            except:
                st.info("File is not recognised as a csv file.")
                sys.exit()

        return data


    data = load_data(file_path, ft, sh, h)
    data.columns = data.columns.str.replace('_', ' ')

    data = data.reset_index()

    data.columns = data.columns.str.title()

    st.sidebar.divider()
    st.write('### 1. Dataset Preview ')

    try:
        st.dataframe(data, use_container_width=True, hide_index=True)

    except:
        st.info("The file wasn't read properly. Please ensure that the input parameters are correctly defined.")
        sys.exit()

    st.divider()
    st.write('### Overview ')

    selected = st.sidebar.radio("**What would you like to know about the data?**",
                                ["Data Dimensions",
                                 "Field Descriptions",
                                 "Summary Statistics",
                                 "Value Counts of Fields"])

    if selected == 'Field Descriptions':
        fd = data.dtypes.reset_index().rename(columns={'index': 'Field Name', 0: 'Field Type'}).sort_values(
            by='Field Type', ascending=False).reset_index(drop=True)
        st.dataframe(fd, use_container_width=True, hide_index=True)

    elif selected == 'Summary Statistics':
        ss = pd.DataFrame(data.describe(include='all').round(2).fillna(''))
        nc = pd.DataFrame(data.isnull().sum()).rename(columns={0: 'count_null'}).T
        ss = pd.concat([nc, ss]).copy()
        st.dataframe(ss, use_container_width=True)

    elif selected == 'Value Counts of Fields':
        sub_selected = st.sidebar.radio("*Which field should be investigated?*", data.select_dtypes('object').columns)
        vc = data[sub_selected].value_counts().reset_index().rename(columns={'count': 'Count'}).reset_index(drop=True)
        st.dataframe(vc, use_container_width=True, hide_index=True)

    else:
        st.write('###### The data has the dimensions :', data.shape)

    st.divider()

    st.sidebar.divider()



    columns = st.selectbox("Parameter 1", data.columns.tolist())
    row = st.selectbox("Parameter 2", data.columns.tolist())


    chart = st.sidebar.radio("**Select chart type**",
                                ["Line chart",
                                 "Bar chart",
                                 "Area chart",])

    if chart == 'Line chart':
        st.line_chart(data, x=row, y=columns)
    elif chart == 'Bar chart':
        st.bar_chart(data, x=row, y=columns)
    elif chart == 'Area chart':
        st.area_chart(data, x=row, y=columns)

else:
    st.info("Please upload a file to proceed.")




