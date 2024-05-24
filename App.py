import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
import base64

def main():
    """
    Main function to define the Streamlit application.
    """

    st.title("Automated Exploratory Data Analysis (EDA)")
    st.subheader("Welcome!")

    activities = ["EDA", "About"]
    choice = st.sidebar.selectbox("Select Activity", activities)

    if choice == "EDA":
        st.subheader("Upload Your Dataset")
        data_file = st.file_uploader("Choose a file", type=['csv', 'json', 'xlsx'])

        if data_file is not None:
            try:
                df = pd.read_csv(data_file) if data_file.name.endswith('.csv') else pd.read_json(data_file) if data_file.name.endswith('.json') else pd.read_excel(data_file)

                st.success("Data uploaded successfully!")

                # Display a sample of the data
                st.subheader("Data Sample")
                st.dataframe(df.head())

                # Perform EDA using Pandas Profiling
                if st.button("Perform EDA"):
                    try:
                        profile = ProfileReport(df)
                        profile.to_file("output.html")
                        st.success("EDA report generated successfully! You can download the report or view it in the sidebar.")
                        st.sidebar.subheader("EDA Report")
                        st.sidebar.markdown(get_sidebar_link("output.html", "View EDA Report", "Download EDA Report"), unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"An error occurred during EDA: {e}")

            except Exception as e:
                st.error(f"Error reading the file: {e}")

    elif choice == "About":
        st.subheader("About")
        st.write("This is an Automated Exploratory Data Analysis (EDA) Streamlit Application.You can upload your dataset, and the application will perform EDA on it, saving you time and effort.")

        
def get_sidebar_link(file_path, view_text, download_text):
    """Generates links to view and download the report."""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    view_link = f'<a href="data:text/html;base64,{b64}" target="_blank">{view_text}</a>'
    download_link = f'<a href="data:file/html;base64,{b64}" download="EDA_Report.html">{download_text}</a>'
    return f"{view_link} | {download_link}"

if __name__ == "__main__":
    main()
