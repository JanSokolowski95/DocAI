import streamlit as st
import yaml
import model
import image_formatting
import base64

from io import BytesIO
from PIL import Image


def sumbit_callback():
    st.session_state.page = "waiting"


def run():
    if "page" not in st.session_state:
        st.session_state.page = "uploading"
    if "result" not in st.session_state:
        st.session_state.result = None
    if "img" not in st.session_state:
        st.session_state.img = None

    st.write("""
    # PDF reader
    """)

    if st.session_state.page == "uploading":
        pdf_file = st.file_uploader("Pick a PDF document")

        if pdf_file is not None:
            img = image_formatting.img_from_pdf(pdf_file)
            st.session_state.img = img

            keys = st.multiselect(
                "Select fields you want to read (note that those are predefined default fields, and they might not exist in your document!):",
                ["Date", "Customer Name", "Phone Number"],
                accept_new_options=True,
                key="keys_multiselect",
            )
            submit_button = st.button(label="SUBMIT", on_click=sumbit_callback)

            st.image(img)
            

    if st.session_state.page == "waiting":
        with st.spinner(text="Waiting for response..."):
            st.session_state.result = model.send(st.session_state.img, st.session_state.keys_multiselect)
        st.session_state.page = "result"

    if st.session_state.page == "result":
        result = st.session_state.result
        st.write(result)
