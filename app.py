import streamlit as st
import pandas as pd
import io

# Remove space from above and side
st.markdown("""
<style>
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
    margin-left: 0rem;
}
</style>
""", unsafe_allow_html=True)


st.title("Data Sorter")

col1, col2=st.columns(2)


dataframe=None
data_type=st.selectbox("Select file type",['csv','xlsx'])
file=st.file_uploader("Upload File", type=['csv','xlsx'])



# If a file is uploaded
if file and data_type is not None:
    if data_type=='csv':
        dataframe = pd.read_csv(file)
    elif data_type=='xlsx':
        dataframe== pd.read_excel(file)

    column=None
    order=None
    col1,col2=st.columns(2)
    with col1:
        col=dataframe.columns
        column=st.selectbox("Select Column You Want to Sort",col)
    with col2:
        order=st.selectbox("Select order",['Ascending','Descending'])


    sorted_data=None
    if order=="Descending":
        sorted_data=dataframe.sort_values(column,ascending=False)
    else:
        sorted_data=dataframe.sort_values(column,ascending=True)

    btn=st.button("Sort File")

    if btn:

        # Create a BytesIO object to store the Excel file
        output = io.BytesIO()

        # Save the sorted DataFrame to the BytesIO object
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            sorted_data.to_excel(writer, index=False, sheet_name="Sorted Data")
            writer.save()

        # Move the cursor to the start of the BytesIO object
        output.seek(0)

        # Create the download button
        download_button = st.download_button(
            label="Download Sorted File",
            data=output,
            file_name=f"sorted_data_{column}_{order}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # Display a pop-up message after download
        if download_button:
            st.success("File downloaded successfully!")

        # btn1= st.button("View Data")
        # if btn1:
        #     tab1, tab2 = st.tabs(["Original Data", "Sorted Data"])
        #     with tab1:
        #         st.write(dataframe)
        #     with tab2:
        #         st.write(sorted_data)
        
