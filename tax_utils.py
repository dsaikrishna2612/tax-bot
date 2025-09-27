def classify_age(age):
    if age < 60:
        return "Citizen"
    elif 60 <= age <= 79:
        return "Senior Citizen"
    else:
        return "Super Senior Citizen"

def calculate_tax_old(total_income, age_class):
    tax = 0
    if age_class == "Citizen":
        if total_income <= 250000:
            tax = 0
        elif total_income <= 500000:
            tax = (total_income - 250000) * 0.05
        elif total_income <= 1000000:
            tax = 12500 + (total_income - 500000) * 0.20
        else:
            tax = 112500 + (total_income - 1000000) * 0.30
    elif age_class == "Senior Citizen":
        if total_income <= 300000:
            tax = 0
        elif total_income <= 500000:
            tax = (total_income - 300000) * 0.05
        elif total_income <= 1000000:
            tax = 10000 + (total_income - 500000) * 0.20
        else:
            tax = 110000 + (total_income - 1000000) * 0.30
    else:  # Super Senior
        if total_income <= 500000:
            tax = 0
        elif total_income <= 1000000:
            tax = (total_income - 500000) * 0.20
        else:
            tax = 100000 + (total_income - 1000000) * 0.30
    return tax

def calculate_tax_new(total_income):
    tax = 0
    if total_income <= 400000:
        tax = 0
    elif total_income <= 800000:
        tax = (total_income - 400000) * 0.05
    elif total_income <= 1200000:
        tax = 20000 + (total_income - 800000) * 0.10
    elif total_income <= 1600000:
        tax = 60000 + (total_income - 1200000) * 0.15
    elif total_income <= 2000000:
        tax = 120000 + (total_income - 1600000) * 0.20
    elif total_income <= 2400000:
        tax = 200000 + (total_income - 2000000) * 0.25
    else:
        tax = 300000 + (total_income - 2400000) * 0.30
    return tax

