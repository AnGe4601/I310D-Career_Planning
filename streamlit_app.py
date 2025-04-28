import streamlit as st
import random

st.title("Job Fulfillment Checker 🎯")

early_pay = st.text_input("Enter your early career pay ($):")
mid_career = st.text_input("Enter your mid-career pay ($):")

if st.button("Check Fulfillment"):
    fulfillment_rate = round(random.random(), 2)
    st.metric(label="Fulfillment Rate", value=f"{fulfillment_rate*100:.0f}%")

    if fulfillment_rate <= 0.5:
        st.warning("😕 Looks like you are not very satisfied with your job.")
    else:
        st.success("😄 You are really enjoying it!")
