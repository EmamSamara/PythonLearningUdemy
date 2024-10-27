from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import csv
import os
from kivy.core.window import Window

Window.clearcolor = (0.15, 0.15, 0.15, 1)

BALANCE_FILE = 'balance.csv'
DAILY_INCOME_FILE = 'daily_income.csv'
TOTAL_DAILY_INCOME_FILE = 'total_daily_income.csv'

def load_balance():
    if not os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([600])
        return 600
    with open(BALANCE_FILE, mode='r') as file:
        reader = csv.reader(file)
        return int(float(next(reader)[0]))

def save_balance(new_balance):
    with open(BALANCE_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_balance])

def load_daily_income():
    if not os.path.exists(DAILY_INCOME_FILE):
        return [0, 0, 0, 0]
    with open(DAILY_INCOME_FILE, mode='r') as file:
        reader = csv.reader(file)
        return [int(value) for value in next(reader)]

def save_daily_income(incomes):
    with open(DAILY_INCOME_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(incomes)

def load_total_daily_income():
    if not os.path.exists(TOTAL_DAILY_INCOME_FILE):
        return 0
    with open(TOTAL_DAILY_INCOME_FILE, mode='r') as file:
        reader = csv.reader(file)
        return int(next(reader)[0])

def save_total_daily_income(total_income):
    with open(TOTAL_DAILY_INCOME_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([total_income])

class IncomeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        title_label = Label(text="Income Tracker", color=(1, 1, 1, 1), font_size='24sp', size_hint_y=None, height=40, halign='center')
        title_label.bind(size=title_label.setter('text_size'))
        layout.add_widget(title_label)

        self.daily_inputs = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        self.daily_income = load_daily_income()
        self.total_daily_income = load_total_daily_income()

        for i, day in enumerate(days):
            box = BoxLayout()
            box.add_widget(Label(text=f"Daily Income for {day}:", color=(1, 1, 1, 1), font_size='18sp'))
            input_field = TextInput(
                input_filter='int',
                size_hint=(0.5, None),
                height=40,
                background_color=(0, 0, 0, 1),
                foreground_color=(1, 1, 1, 1),
                font_size='20sp'
            )
            input_field.text = ''
            box.add_widget(input_field)
            self.daily_inputs.append(input_field)
            layout.add_widget(box)

        box = BoxLayout()
        box.add_widget(Label(text="Weekend Bonus:", color=(1, 1, 1, 1), font_size='18sp'))
        self.weekend_input = TextInput(
            input_filter='int',
            size_hint=(0.5, None),
            height=40,
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            font_size='20sp'
        )
        self.weekend_input.text = ''
        box.add_widget(self.weekend_input)
        layout.add_widget(box)

        reset_button = Button(text="Reset Daily Values", size_hint=(1, None), height=50)
        reset_button.bind(on_press=self.reset_values)
        layout.add_widget(reset_button)

        calculate_button = Button(text="Calculate", size_hint=(1, None), height=50)
        calculate_button.bind(on_press=self.calculate)
        layout.add_widget(calculate_button)

        self.balance_label = Label(
            text=f"Balance: 600 ₪ (Goal: 1000 ₪, Remaining: {1000 - 600} ₪)", 
            color=(1, 1, 1, 1), 
            font_size='14sp',  
            size_hint=(None, None),
            size=(300, 30),  
            pos_hint={'x': 0, 'y': 0}
        )
        layout.add_widget(self.balance_label)

        self.goal_label = Label(
            text="Goal: 2000 ₪ (Remaining: {2000 - 600} ₪)", 
            color=(1, 1, 1, 1), 
            font_size='14sp',  
            size_hint=(None, None),
            size=(200, 30),  
            pos_hint={'x': 0, 'y': -0.05}
        )
        layout.add_widget(self.goal_label)

        return layout

    def reset_values(self, instance):
        self.daily_income = [0, 0, 0, 0]
        save_daily_income(self.daily_income)
        popup = Popup(
            title='Reset',
            content=Label(text="Daily values have been reset to zero."),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def calculate(self, instance):
        try:
            total_daily_income = 0
            for i, input_field in enumerate(self.daily_inputs):
                if input_field.text:
                    daily_income = int(input_field.text)
                    self.daily_income[i] += daily_income
                    total_daily_income += daily_income

            weekend_bonus = int(self.weekend_input.text) if self.weekend_input.text else 0

            save_daily_income(self.daily_income)

            current_balance = load_balance()
            new_balance = current_balance + weekend_bonus
            save_balance(new_balance)

            remaining_to_goal1 = 1000 - new_balance
            self.balance_label.text = f"Balance: {new_balance} ₪ (Goal: 1000 ₪, Remaining: {remaining_to_goal1} ₪)"
            
            remaining_to_goal2 = 2000 - new_balance
            self.goal_label.text = f"Goal: 2000 ₪ (Remaining: {remaining_to_goal2} ₪)"

            if weekend_bonus > 0:
                for i in range(len(self.daily_income)):
                    self.daily_income[i] = 0
                save_daily_income(self.daily_income)

            popup = Popup(
                title='Results',
                content=Label(text=f"Total Daily Income (Monday-Thursday): {total_daily_income} ₪\n"
                                   f"Weekend Bonus: {weekend_bonus} ₪\n"
                                   f"Balance: {new_balance} ₪"),
                size_hint=(0.6, 0.4)
            )
            popup.open()
        except ValueError:
            popup = Popup(
                title='Error',
                content=Label(text="Please enter valid integers."),
                size_hint=(0.6, 0.4)
            )
            popup.open()

if __name__ == "__main__":
    IncomeApp().run()
