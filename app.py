
import streamlit as st

import torch
from PIL import Image

import os
import meta

from utils import (
    load_image_from_url,
    load_image_from_local,
    image_to_base64,
)

from textOCR import tesseract_ocr, tesseract_ocr_ko, easyocr_ko
# from keywords_extraction import keywords_extraction
from st_diffusion import generate_v1, generate_v2


def image_uploader():
    image = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
    
    return image


def main():
    st.set_page_config(
        page_title='Text to Image.',
        layout='wide',
        initial_sidebar_state='expanded'
    )

    st.sidebar.markdown("# Settings")
    # select_style -> generate_v2 에서 styler 입력.
    st.sidebar.markdown('#### Select style of image')
    select_style = st.sidebar.selectbox('Stable Diffusion provides some styles',['realistic', 'story', 'anime', 'concept art'])
    
    st.sidebar.markdown("#### Select size of image")
    # delete the sidebars and add buttons that click or not
    image_height = st.sidebar.slider('height', 128, 1024, 128)
    image_width = st.sidebar.slider('width', 128, 1024, 128)


    col1, col2 = st.columns([6,4])
    with col2:
        # 여기부분에 로고 넣기
        # st.image(load_image_from_local('/content/book-g366ded744_640.jpg'),width=500)
        st.markdown(meta.SIDEBAR_INFO, unsafe_allow_html=True)

        with st.expander("How to use the application", expanded=True):
            st.markdown(meta.STORY, unsafe_allow_html=True)

    with col1:
        # 여기 부분이 제목에 대한 부연 설명 넣기
        st.markdown(meta.HEADER_INFO, unsafe_allow_html=True)

        # 여기 부분이 첫 번째 ocr 이미지 input 으로 넣으라고 항목 표시
        st.markdown(meta.HEAD2_INFO, unsafe_allow_html=True)
        # upload 할 수 있도록 만듦.
        my_upload = image_uploader()
        if my_upload:
            upload_image = Image.open(my_upload)
            st.image(upload_image)

            # 여기 부분에서 textocr 결과 확인
            st.markdown('###')
            st.markdown('#### Result of textOCR:')
            prompt = tesseract_ocr_ko(my_upload)
            # prompt = keywords_ext(prompt)
            st.text(prompt)
        else:
            pass 

    gen_button = st.button("Generate Image")

    if gen_button:
        
        with st.spinner("Generating Image..."):

            if prompt is None:
                st.error("There are some errors in prompt, try again")

            else:
                ### 여기서부터는 이미지 생성 후 보이게 하는 것
                ################# 여기에 styler 추가해야됨 -> 03.01 사이드바로 추가 완료. height, width 설정도 추가.
                image = generate_v2(prompt, styler=select_style, height=image_height, width=image_height)
        
        st.markdown('#### Result of Image Generator')
        st.text('If you want to find other images, re-generate image')
        st.image(image)

if __name__ == '__main__':
    main()
