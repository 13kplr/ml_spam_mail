import streamlit as st
from transform import email_to_clean_text1, rfc, vectorizer




t1sm = email_to_clean_text1()
st.title('Загрузи письмо и узнай является ли оно спамом!')
st.markdown('Данная модель основана на алгоритме RFC с обучением на датасетах spamassasin и enron.')
st.markdown('В данный момент модель обрабатывает письма только на английском языке.')


uploaded_file = st.file_uploader("Пожалуйста, выберите и загрузите файл")

if uploaded_file is None:
    st.session_state['upload_state'] = 'Upload file first!'
else: 
    bytes_data = uploaded_file.getvalue()
    data = uploaded_file.getvalue().decode('ISO-8859-1')
    test_data = data
    new_d = t1sm.transform(test_data)
    list_w_st = [ ]
    list_w_st += [new_d]
    prepared_data = vectorizer.transform(list_w_st).toarray()
    predict = rfc.predict(prepared_data)
    if predict == [0]: 
        st.subheader ('Ваше письмо не является спамом с вероятностью 96.7%.')
    else: 
        st.subheader('Ваше письмо с точностью до 96.7% является спамом.')



