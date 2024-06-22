import pandas as pd
import os
import random

class Balance:
    def __init__(self):
        """Initialize Balance with default and user categories."""
        self.categories = [
            "Income",
            "Food",
            "Utilities",
            "Entertainment",
            "Clothes",
            "Housing",
            "Transportation",
            "Health",
        ]
        self.user_categories = self.load_user_categories()
        self.title = ["ID", "Date", "Categories", "Amount", "Balance"]


    def create_csv_file(self, filename="finance.csv"):
        """Creating a csv file if it doesn't exist"""
        df = pd.DataFrame(columns=self.title)
        df.to_csv(filename, index=False)
        return df


    def load_user_categories(self, filename="user_categories.csv"):
        """Load user categories from a file if it exists"""
        if os.path.isfile(filename):
            df = pd.read_csv(filename)
            return df['Category'].tolist()
        else:
            return []


    def save_user_categories(self, filename="user_categories.csv"):
        """Save user categories to a file"""
        df = pd.DataFrame(self.user_categories, columns=['Category'])
        df.to_csv(filename, index=False)


    def add_category(self, new_category):
        print(new_category)
        """I'm adding new category saving it to self.user_categories"""
        if (
            new_category not in self.categories
            and new_category not in self.user_categories
        ):
            self.user_categories.append(new_category)
            self.save_user_categories()


    def edit_category(self, category_name, new_category_name):
        """Editing existing categories and saving them in self.categories"""
        if not isinstance(new_category_name, str):
            raise TypeError("Category must be a string.")
        if category_name in self.user_categories:
            index = self.user_categories.index(category_name)
            self.user_categories[index] = new_category_name
            self.save_user_categories()


    def remove_category(self, category_name):
        """Removing unwanted category from self.categories"""
        if category_name in self.user_categories:
            self.user_categories.remove(category_name)
            self.save_user_categories()


    def generate_random_id(self):
        """generating random ID for row in csv"""
        df = self.read_file()
        existing_ids = df.iloc[:, 0].tolist()
        new_id = str(random.randint(1000, 9999))
        while new_id in existing_ids:
            new_id = str(random.randint(1000, 9999))
        return new_id
    

    def read_file(self, filename="finance.csv"):
        """Reading csv file"""
        if not os.path.isfile(filename):
            df = self.create_csv_file()
        else:
            df = pd.read_csv(filename)
        return df


    def add_new_line_to_file(self, new_line, filename="finance.csv"):
        """adding new line to csv file (to the end of the file)"""
        id = self.generate_random_id()
        new_line.insert(0, id)
        df = self.read_file()
        new_data = pd.DataFrame([new_line], columns=self.title)
        df = pd.concat([df, new_data], ignore_index=True)
        df['Balance'] = self.calculate_balances(df)
        df.to_csv(filename, index=False)


    def deleting_line_from_file(self, row_id, filename="finance.csv"):
        """deleting specific row from the file by searching the ID of that row"""
        df = self.read_file(filename)
        df = df[df['ID'] != int(row_id)]
        df['Balance'] = self.calculate_balances(df)
        df.to_csv(filename, index=False)


    def editing_row_of_file(self, id, edited_line, filename="finance.csv"):
        """editing specific row from the file by searching the ID of that row"""
        df = self.read_file(filename)
        edited_line[2] = float(edited_line[2]) 
        df.loc[df['ID'] == int(id), ['Date', 'Categories', 'Amount']] = edited_line
        df['Balance'] = self.calculate_balances(df)
        df.to_csv(filename, index=False)


    def calculate_balances(self, df):
        """Calculate balances for each row based on categories."""
        balance = 0.0
        balances = []
        
        for _, row in df.iterrows():
            if row['Categories'] == 'Income':
                balance += float(row['Amount'])
            else:
                balance -= float(row['Amount'])
            balances.append(balance)
        
        return balances
    

    def count_balance(self):
        """Calculate total balance"""
        df = self.read_file()
        income = df[df['Categories'] == 'Income']['Amount'].sum()
        expenses = df[df['Categories'] != 'Income']['Amount'].sum()
        balance = income - expenses
        
        return balance

class EstimateCost:
    def __init__(self, balance: Balance):
        self.balance = balance
        self.title = ["ID", "Date", "Categories", "Amount"]

    def generate_random_id(self):
        """generating random ID for row in csv"""
        df = self.read_estimate_csv_file()
        existing_ids = df.iloc[:, 0].tolist()
        new_id = str(random.randint(1000, 9999))
        while new_id in existing_ids:
            new_id = str(random.randint(1000, 9999))
        return new_id


    def create_estimate_csv_file(self, filename="estimate.csv"):
        """Creating a csv file if it doesn't exist"""
        df = pd.DataFrame(columns=self.title)
        df.to_csv(filename, index=False)
        return df


    def read_estimate_csv_file(self, filename="estimate.csv"):
        """Reading csv file"""
        if not os.path.isfile(filename):
            df = self.create_estimate_csv_file()
        else:
            df = pd.read_csv(filename)
        return df


    def add_estimate_line_to_file(self, new_line, filename="estimate.csv"):
        """adding new line to csv file (to the end of the file)"""
        id = self.balance.generate_random_id()
        new_line.insert(0, id)
        df = self.read_estimate_csv_file()
        new_data = pd.DataFrame([new_line], columns=self.title)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(filename, index=False)


    def delete_estimate_line_from_file(self, row_id, filename="estimate.csv"):
        """deleting specific row from the file by searching the ID of that row"""
        df = self.read_estimate_csv_file(filename)
        df = df[df['ID'] != int(row_id)]
        df.to_csv(filename, index=False)


    def edit_estimate_row_of_file(self, id, new_line, filename="estimate.csv"):
        """editing specific row from the file by searching the ID of that row"""
        df = self.read_estimate_csv_file(filename)
        new_line[2] = float(new_line[2]) 
        df.loc[df['ID'] == int(id), ['Date', 'Categories', 'Amount']] = new_line
        df.to_csv(filename, index=False)
