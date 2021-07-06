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
    'Bánh căn',
    'Bánh canh',
    'Bánh chưng',
    'Bánh cuốn',
    'Bánh đúc',
    'Bánh giò',
    'Bánh khọt',
    'Bánh mì',
    'Bánh pía',
    'Bánh tét',
    'Bánh tráng nướng',
    'Bánh xèo',
    'Bún bò Huế',
    'Bún đậu mắm tôm',
    'Bún mắm',
    'Bún riêu',
    'Bún thịt nướng',
    'Cá kho tộ',
    'Canh chua',
    'Cao lầu',
    'Cháo lòng',
    'Cơm tấm',
    'Gỏi cuốn',
    'Hủ tiếu',
    'Mì Quảng',
    'Nem chua',
    'Phở',
    'Xôi xéo'
]


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
    fig.update_layout(xaxis_tickangle=-55)
    fig.update_xaxes(title='')
    st.plotly_chart(fig, use_container_width=True)


st.markdown(
    "<h1 style='text-align: center;'>Vietnamese Foods Classification 🍜</h1> ",
    unsafe_allow_html=True
)

st.markdown(
    """
    <center>
        <img 
            src='https://www.google.com/logos/doodles/2020/celebrating-banh-mi-6753651837108330.3-2xa.gif' 
            style='width: 90%;'
        >
    </center><br/>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Choose a file")
url = st.text_input(
	'Image Url: ', 
	'https://upload.wikimedia.org/wikipedia/commons/5/53/Pho-Beef-Noodles-2008.jpg'
)
st.write('')
st.write('')

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    st.image(bytes_data, use_column_width=True)
    with open('./test.jpg', 'wb') as f: f.write(bytes_data)
elif url:
    urllib.request.urlretrieve(url, './test.jpg')
    st.markdown(
        f"<center><img src='{url}' style='width: 90%;'></center>",
        unsafe_allow_html=True
    )

img_test = preprocess_image('./test.jpg')
model = load_model('Model Implement/model.h5')
pred_probs = model.predict(img_test)[0]

index = np.argmax(pred_probs)
label = classes[index]

st.markdown(
    f'''
        <h2 style='text-align: center;'>
            <a 
                href='https://en.wikipedia.org/wiki/{label.replace(' ', '%20')}' 
                style='text-decoration: none;'
                target='_blank'
            >
                 {label}
            </a>
             - {pred_probs[index] * 100:.2f}%
        </h2>
    ''',
    unsafe_allow_html=True
)

plot_probs(pred_probs)
st.markdown("[![](https://img.shields.io/badge/GitHub-View_Repository-blue?logo=GitHub)](https://github.com/18520339/vietnamese-foods)")