import streamlit as st
from PIL import Image
import google.generativeai as genai


genai.configure(api_key="AIzaSyCapBovz77iB34MHL2UjqlxsvcCB4GhyoQ")
## function to load Gemini Flash
model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

#image processing
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data=uploaded_file.getvalue()
        image_parts= [
            {
                "mime_type": uploaded_file.type, 
                "data" : bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
#initialize streamlit app

st.set_page_config(page_title="InvoQuery")

st.header("InvoQuery")
input=st.text_input("Ask question:", key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...", type=["jpg","'jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image.",use_column_width=True)

submit=st.button("Submit")

input_prompt="""
You are an expert in understanding invoices. We will upload a image as invoice 
and you will have to answer any questions based on the uploaded invoice image
"""

# If submit button is clicked
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is ")
    st.write(response)
