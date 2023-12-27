import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figure input from the user
    """
    while True:
        print("Please sales data from from the last market")
        print("Data should be six numbers, seperated by commas.")
        print("Examples: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter data here:")

        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print("data is valid")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if string cant be converted into int
    and if there arent exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) !=6:
             raise ValueError(
                 f"6 values required, you provided {len(values)}"
             )
    except ValueError as e:
        print(f"Invalid data:{e}, please try again\n")
        return False

    return True

#these two function is no longer in use because
#the def update_worksheet runs both these fucntions
#so that we would understand possibility making function shorter
#and minimal repetion of same code
# def update_sales_workheet(data):
#     """
#     Update sales worksheet, add new row with user list provided
#     """
#     print("updatinging sales worksheet\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("sales worksheet updated successfully.\n")

# def update_surplus_workheet(data):
#     """
#     Update surplus worksheet, add new row with user list provided
#     """
#     print("updating surplus worksheet\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("surplus worksheet updated now.\n")

def update_worksheet(data, worksheet):
    """
    Recives list of integers to be inserted into worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"updatinging {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated now.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus idicates waste
    - Negative surplus indicates extra made after stock rached 0 
    """
    print("claculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales 
        surplus_data.append(surplus)

    return surplus_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


print("welcome to Love Sandwiches Data Automations")
main()