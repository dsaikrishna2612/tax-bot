import streamlit as st
from personal_info import get_personal_info
from income import get_income_details
from deductions import get_deductions
from tax_utils import classify_age, calculate_tax_old, calculate_tax_new
from pdf_utils import generate_pdf
from email_utils import send_email

st.title("Income Tax Calculator")

# Get user inputs
personal_info = get_personal_info()
income_info = get_income_details()
deduction_info = get_deductions()

# Process
age_class = classify_age(personal_info["age"])
net_income = income_info["gross_income"] - deduction_info["total_deductions"]
tax_old = calculate_tax_old(net_income, age_class)
tax_new = calculate_tax_new(income_info["gross_income"])

# Action
if st.button("Send Email"):
    data = {**personal_info, **income_info, **deduction_info,
            "age_class": age_class,
            "net_income": net_income,
            "tax_old": tax_old,
            "tax_new": tax_new}

    # Generate PDF
    pdf_buffer = None
    try:
        pdf_buffer = generate_pdf(data)
    except Exception as e:
        st.error(f"❌ Failed to generate PDF. Please check your input and try again.\nError: {e}")

    if pdf_buffer is None:
        st.error("❌ Failed to generate PDF. Please check your input and try again.")
    else:
        # Reset buffer before sending email
        pdf_buffer.seek(0)
        # Send Email
        try:
            send_email(personal_info["email"], pdf_buffer, data)
            st.success(f"✅ PDF sent to {personal_info['email']} successfully!")
            st.balloons() #balloons animation on success
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
