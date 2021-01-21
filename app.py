import numpy as np
import pandas as pd

import plotly.express as px
import urllib.request

import streamlit as st
import streamlit.components.v1 as components

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from io import StringIO

classes = [
    'Bánh bèo',
    'Bánh bột lọc',
    'Bánh canh',
    'Bánh căn',
    'Bánh chưng',
    'Bánh cuốn',
    'Bánh giò',
    'Bánh khọt',
    'Bánh mì',
    'Bánh pía',
    'Bánh tét',
    'Bánh tráng nướng',
    'Bánh xèo',
    'Bún bò Huế',
    'Bún mắm',
    'Bún riêu',
    'Bún thịt nướng',
    'Bún đậu mắm tôm',
    'Canh chua',
    'Cao lầu',
    'Cá kho tộ',
    'Cháo lòng',
    'Cơm tấm',
    'Gỏi cuốn',
    'Hủ tiếu',
    'Mì quảng',
    'Nem chua',
    'Phở',
    'Xôi xéo'
]

with open('camera.html', 'r') as f:
    camera_html = f.read()


def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    return img


def plot_probs(outputs):
    probs = pd.Series(np.round(outputs * 100, 2), classes)
    probs = probs.sort_values(ascending=False).reset_index()
    probs.columns = ['Class', 'Probability']
    fig = px.bar(probs, x='Class', y='Probability')
    fig.update_layout(xaxis_tickangle=-60)
    st.plotly_chart(fig, use_container_width=True)


st.markdown(
    "<h1 style='text-align: center;'>What is this Vietnamese food?🍜</h1> ",
    unsafe_allow_html=True
)

st.markdown(
    """
    <center>
        <img 
            src='https://www.google.com/logos/doodles/2020/celebrating-banh-mi-6753651837108330.3-2xa.gif' 
            style='width: 90%;'
        >
    </center>
    """,
    unsafe_allow_html=True
)

url = st.text_input(
	'URL: ', 
	'https://upload.wikimedia.org/wikipedia/commons/5/53/Pho-Beef-Noodles-2008.jpg'
)
uploaded_file = st.file_uploader("Choose a file")
# components.html(camera_html, height=400, scrolling=True)

st.markdown(
    "<h2 style='text-align: center;'>Image📷</h2>",
    unsafe_allow_html=True
)

if url:
    urllib.request.urlretrieve(url, './test.jpg')
    st.markdown(
        f"<center><img src='{url}' style='width: 90%;'></center>",
        unsafe_allow_html=True
    )
elif uploaded_file is not None:
    bytes_data = uploaded_file.read()
    st.image(bytes_data, use_column_width=True)
    with open('./test.jpg', 'wb') as f:
        f.write(bytes_data)

img_test = preprocess_image('./test.jpg')
model = load_model('model.h5')
pred_probs = model.predict(img_test)[0]

index = np.argmax(pred_probs)
label = classes[index]

st.markdown(f'## {label}')
st.markdown(f"*Read on [Wikipedia](https://en.wikipedia.org/wiki/{label.replace(' ', '%20')})*")
st.markdown(f'**Probability:** {pred_probs[index] * 100:.2f}%')
plot_probs(pred_probs)
