import streamlit as st
from gpt_ui import run_ui

if __name__ == '__main__':
    st.set_page_config(page_title="Student-Athlete GPTCoach", layout="wide")
    run_ui()

