import streamlit as st

def install_dependencies():
    """
    Provides a guide for manually installing the necessary system and Python dependencies.
    """
    st.write("### Installation Guide for Dependencies")
    st.write(
        """
        Below are the commands to manually install the necessary dependencies. 
        Please copy and paste these commands into your terminal:
        """
    )

    # Guide for system packages
    st.subheader("1. Install System Packages")
    st.code(
        """
sudo apt-get install python3-dev default-libmysqlclient-dev
""",
        language="bash"
    )

    # Guide for Python packages
    st.subheader("2. Install Python Packages")
    st.code(
        """
# Install Python dependencies:
pip install pymysql
""",
        language="bash"
    )

    st.success("Copy the above commands and execute them in your terminal to install the dependencies.")
