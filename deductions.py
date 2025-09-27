import streamlit as st

def get_deductions():
    st.header("Deductions (Max ₹150,000)")
    deductions = {}
    deductions['Life Insurance Policy'] = st.number_input("Life Insurance Policy", min_value=0)
    deductions['PPF'] = st.number_input("Public Provident Fund", min_value=0)
    deductions['Employees Contribution to PF / Superannuation'] = st.number_input("PF / Superannuation", min_value=0)
    deductions['Loan Repayment (Principal Amount)'] = st.number_input("Loan Repayment for House(Principal Amount)", min_value=0)
    deductions['FD (≥5 years)'] = st.number_input("Fixed Deposits ≥5 years", min_value=0)
    deductions['Education Fee (Max 2 children)'] = st.number_input("Education Fee for Children(max 2 Children)", min_value=0)

    total_deductions = min(sum(deductions.values()), 150000)

    return {
        "deductions": deductions,
        "total_deductions": total_deductions
    }
