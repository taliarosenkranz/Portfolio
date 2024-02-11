import streamlit as st

# Collecting organizations details


def registration_form():
    with st.form(key="registration", clear_on_submit=True):
        name = st.text_input("Organization Name: ")
        street = st.text_input("Street name: ")
        house_number = st.text_input("House number: ")
        city = st.text_input("City: ")
        people_needed = st.number_input(
            "Number of people needed: ", min_value=0)
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        submit_button = st.form_submit_button("Register")

    if submit_button:
        st.success("Your details have been submitted successfully!")

    address = street+' '+house_number+','+' '+city
    

    organization_data = [name, address, people_needed, email, phone]
    return organization_data
