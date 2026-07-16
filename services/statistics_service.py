from models.category import OperationType

def aggregate(transactions) -> dict:
    total_income = 0.0
    total_expense = 0.0
    category_totals = {}
    income_category_totals = {}

    for t in transactions:
        if t.category.type == OperationType.income:
            total_income += t.amount
            resault = income_category_totals.get(t.category.name, 0) + t.amount
            income_category_totals[t.category.name] = resault
        elif t.category.type == OperationType.expense:
            total_expense += t.amount
            resault = category_totals.get(t.category.name, 0) + t.amount
            category_totals[t.category.name] = resault

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "category_totals": category_totals,
        "income_category_totals": income_category_totals,
    }

def calculate_percentages(category_totals: dict, total_expense: float) -> dict:
    percentage = {}
    for category_name, amount in category_totals.items():
        if total_expense > 0:
            percentage[category_name] = (amount / total_expense) * 100
        else:
            percentage[category_name] = 0
        
    return percentage