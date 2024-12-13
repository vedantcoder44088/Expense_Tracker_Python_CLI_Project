import sys

import numpy as np
import pandas as pd
from datetime import datetime

budget_file_path = "monthly_budget.csv"
expense_file_path = "expense_details.csv"


def create_csv(file_path, columns):
    try:
        pd.read_csv(file_path)
        print(f"{file_path} already exists.")
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        print(f"{file_path} created successfully")

def date_input():
    while True:
        date_input = input("Enter a date (YYYY-MM-DD):")
        try:
            date = datetime.strptime(date_input, "%Y-%m-%d").date()
            return date
        except ValueError:
            print("Invalid date Format")

def input_add_month():
    input_month = int(input("Enter Month:"))
    if input_month > 12 or input_month < 1:
        print("Provide Specific Month")
        input_add_month()
    input_budget = int(input("Enter Budget:"))
    add_monthly_budget(budget_file_path, input_month, input_budget)




def add_monthly_budget(file_path, month, budget):
    try:
        df = pd.read_csv(file_path)
        print(df)
        if month in df["Month"].values:
            print("Date For Provided Month Already Exists.")
            return
        if not df.empty:
            carried_over = df.iloc[-1]["Remaining"]

        new_row = {
            "Month": month,
            "Starting Budget": budget + carried_over,
            "Spent": 0,
            "Remaining": budget + carried_over,
            "Carried Over": carried_over
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(file_path, index=False)
        print(f"Added New Month: {month} with Budget {budget}")

    except Exception as e:
        print("Error:",e)

def input_add_expense():
    input_date = date_input()
    input_category = input("Enter Expense Category:")
    input_expense_value = int(input("Enter Amount:"))
    input_description = input("Enter Description:")

    add_expense(expense_file_path, budget_file_path, input_date , input_expense_value, input_category, input_description)

def add_expense(expense_file_path, budget_file_path, input_date,input_expense_value, input_category = '', input_description = ''):
    try:
        expense_df = pd.read_csv(expense_file_path)
        new_expense = {
            "Date": input_date,
            "Category": input_category,
            "Expense Value": input_expense_value,
            "Description": input_description
        }

        budget_df = pd.read_csv(budget_file_path)

        if input_date.month not in budget_df["Month"].values:
            print(f"No Data For Month {input_date.month}. Please Add Month and Budget First.")
        else:
            expense_df = pd.concat([expense_df, pd.DataFrame([new_expense])], ignore_index=True)
            expense_df.to_csv(expense_file_path, index=False)

            budget_df.loc[budget_df["Month"] == input_date.month, "Spent"] += input_expense_value
            budget_df.loc[budget_df["Month"] == input_date.month, "Remaining"] -= input_expense_value
            budget_df.to_csv(budget_file_path, index=False)

            print(f"Recorded expense of {input_expense_value} in category {input_category} for {input_date}")
    except Exception as e:
        print("Error:", e)

def input_month():
    month = input("Enter Month:")

def display_expenses(expense_file_path, budget_file_path, month=None):
    try:
        # budget_df = pd.read_csv(budget_file_path)
        expense_df = pd.read_csv(expense_file_path)

        if month:
            filtered_expense_df = expense_df[pd.to_datetime(expense_df["Date"]).dt.month == int(month)]
            # print("Budget Table:")
            # print(budget_df)
            print("Expense Table:")
            print(filtered_expense_df)
        else:
            # print("Budget Table:")
            # print(budget_df)
            print("Expense Table:")
            print(expense_df)
    except Exception as e:
        print("Error:", e)

def display_budget(budget_file_path, month=None):
    print(month)
    try:
        budget_df = pd.read_csv(budget_file_path)
        if month:
            filtered_budget_df = budget_df[budget_df["Month"] == int(month)]
            print("Budget Table:")
            print(filtered_budget_df)

        specific_month_df = budget_df[budget_df["Month"] == int(month)]
        if not specific_month_df.empty:
            remaining_budget = specific_month_df["Remaining"].iloc[0]
            if remaining_budget < 0:
                print(f"Warning: Budget Of Month {month} is Out")
            else:
                print(f"Budget Of Month {month} is Remaining {remaining_budget}")
    except Exception as e:
        print("Error:", e)


def validate_month(input_month):
    if input_month > 12 and input_month < 1:
        print("Provide Specific Month")


create_csv(budget_file_path, ["Month", "Starting Budget", "Spent", "Remaining", "Carried Over"])
create_csv(expense_file_path, ["Date", "Category", "Expense Value", "Description"])
def main_menu():
    print("Welcome To The Expense Tracker App")
    print("1. Add Expense")
    print("2. Add Budget")
    print("3. View Expense")
    print("4. Track Budget")
    print("5. Exit")

    input_menu_code = int(input("Enter Option From 1 to 5:"))

    if(input_menu_code == 1):
        input_add_expense()
        main_menu()
    if (input_menu_code == 2):
        input_add_month()
        main_menu()
    if (input_menu_code == 3):
        month = (input("Enter Month:"))
        display_expenses(expense_file_path, budget_file_path, month)
        main_menu()
    if (input_menu_code == 4):
        month = (input("Enter Month:"))
        display_budget(budget_file_path, month)
        main_menu()
    if (input_menu_code == 5):
        sys.exit()
    else:
        print("Input Specific Oprion Between 1 To 5")
        main_menu()


main_menu()

