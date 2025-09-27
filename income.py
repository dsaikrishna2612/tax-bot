import streamlit as st
import pandas as pd

def get_income_details():
    st.header("Income Details")

    # Salary
    salary = st.number_input("Income from Salary (as per form-16)", min_value=0)

    # ---------------- House Property Computation ----------------
    st.subheader("Income from House Property")

    # --- Inputs ---
    sop_interest = st.number_input("Interest on Loan for Construction/Purchase of House Property (Self-Occupied, max 200000/others-30000)", 
                                   min_value=0, max_value=200000, key="sop_interest")

    rent_received_letout = st.number_input("Rent Received (Let Out)", min_value=0, key="rent_received_letout")
    municipal_tax_letout = st.number_input("Municipal Taxes (Let Out)", min_value=0, key="municipal_tax_letout")
    interest_deduction_letout = st.number_input("Interest on Loan for Construction/Purchase of House Property (Let Out, no-limit)", 
                                                min_value=0, key="interest_deduction_letout")

    # --- Calculations ---
    # SOP
    income_sop = -sop_interest

    # Let Out
    nav_letout = max(rent_received_letout - municipal_tax_letout, 0)
    std_deduction_letout = 0.3 * nav_letout
    income_letout = nav_letout - std_deduction_letout - interest_deduction_letout

    # Total House Property Income
    total_house_property = income_sop + income_letout

    # ---------------- Build Table ----------------
    table_data = [
        ["Rent Received", "0", f"{rent_received_letout}"],
        ["Gross Annual Value (GAV)", "0", f"{rent_received_letout}"],
        ["Less: Municipal Taxes", "0", f"{municipal_tax_letout}"],
        ["Net Annual Value (NAV)", "0", f"{nav_letout}"],
        ["(a) Standard Deduction 30% of NAV", "0", f"{std_deduction_letout}"],
        ["(b) Interest on Loan (max 200000)", f"{sop_interest}", f"{interest_deduction_letout}"],
        ["Income from House Property", f"{income_sop}", f"{income_letout}"],
    ]

    df = pd.DataFrame(table_data, columns=["Computation", "Self-Occupied Property", "Let Out Property"])
    st.table(df)

    # ---------------- Other Sources ----------------
    other_sources = st.number_input("Income from Other Sources", min_value=0)

    gross_income = salary + total_house_property + other_sources

    return {
        "salary": salary,
        "house_property": total_house_property,
        "other_sources": other_sources,
        "gross_income": gross_income,
        "sop_interest": sop_interest,
        "rent_received_letout": rent_received_letout,
        "municipal_tax_letout": municipal_tax_letout,
        "nav_letout": nav_letout,
        "std_deduction_letout": std_deduction_letout,
        "interest_deduction_letout": interest_deduction_letout,
        "income_letout": income_letout
    }
