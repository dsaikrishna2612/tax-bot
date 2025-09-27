import streamlit as st

def get_personal_info():
    st.header("Personal Details")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender Type",["Select","Male","Female","Other"])
    place = st.text_input("Place")
    email = st.text_input("Email")
    taxpayer_type = st.selectbox("Taxpayer Type", ["Select","Individual","HUF","AOP","BOI","AJP"])
    employee_type = None
    if taxpayer_type == "Individual":
        employee_type = st.selectbox("Employment Type", ["Select","Government Employee","Private Employee"])
    
    return {
        "name": name,
        "age": age,
        "gender": gender,
        "place": place,
        "email": email,
        "taxpayer_type": taxpayer_type,
        "employee_type": employee_type
    }
