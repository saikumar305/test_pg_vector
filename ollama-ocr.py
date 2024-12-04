import ollama
import streamlit as st
from PIL import Image
import os


st.set_page_config(page_title="OLLAMA OCR", 
                   page_icon="",
                   layout="wide",
                   initial_sidebar_state="expanded")


st.title("OLLAMA OCR")

col1, col2 = st.columns([6,1])

with col2:
    if st.button("Clear"):
        if 'ocr_result' in st.session_state:
            del st.session_state.ocr_result
        st.rerun()

st.markdown('<p style="font-size: 20px; margin-top: -20px;">Extract text from an image using llama 3.2 vision model</p>', unsafe_allow_html=True)

st.markdown('---')

with st.sidebar:
    st.header("Upload an image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        if st.button("Extract Text", type="primary"):
            with st.spinner("Extracting text..."):
                try:
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=[{
                            'role': 'user',
                            'content': '''Analyse the text in provided image. Extract all the readable content
                              and present it in a structured markdown format that is clear, concise, and well organized.
                                Ensure proper formatting (e.g., headings, lists, or code blocks) as necessary to represent content effectively.
                                If no text is detected, respond with "No text detected''',
                            'images': [uploaded_file.getvalue()]
                            
                        }]
                    )
                    print(response)
                    st.session_state.ocr_result = response.message.content

                except Exception as e:
                    st.error(f"Error processing image: {e}")

if 'ocr_result' in st.session_state:
    st.markdown(st.session_state.ocr_result, unsafe_allow_html=True)

st.markdown('---')
st.markdown('made with ❤️ by [ollama](https://ollama.ai)')
        