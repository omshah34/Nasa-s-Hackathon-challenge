from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import math

class MyApp(App):
    def build(self):
        root_widget = BoxLayout(orientation='vertical')
        output_label = Label(size_hint_y=.75, font_size=50, text="")

        button_symbols = (
            '%', 'CE', 'C', '⌫',
            'e','log(','^','π',
            '1/x', 'x²', '√x', '÷',
            '7', '8', '9', '×',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '+/-', '0', '.', '='
        )

        button_grid = GridLayout(cols=4, size_hint_y=2)
        buttons = []

        for symbol in button_symbols:
            btn = Button(text=symbol)
            button_grid.add_widget(btn)
            buttons.append(btn)

        def print_button_text(instance):
            output_label.text += instance.text

        def resize_label_text(label, new_height):
            label.font_size = .5 * label.height

        def evaluate_result(instance):
            try:
                expression = output_label.text.replace('÷', '/').replace('×', '*').replace('^', '**')
                output_label.text = str(eval(expression))
            except:
                output_label.text = "Syntax Error"

        def square_root(instance):
            try:
                value = float(output_label.text)
                output_label.text = str(value ** 0.5)
            except:
                output_label.text = "Error"

        def square(instance):
            try:
                value = float(output_label.text)
                output_label.text = str(value ** 2)
            except:
                output_label.text = "Error"

        def reciprocal(instance):
            try:
                value = float(output_label.text)
                if value == 0:
                    output_label.text = "Error"
                else:
                    output_label.text = str(1 / value)
            except:
                output_label.text = "Error"

        def pi(instance):
            try:
                if output_label.text == "":
                    output_label.text = str(math.pi)
                else:
                    output_label.text += str(math.pi)
            except:
                output_label.text = "Error"

        def log(instance):
            try:
                if output_label.text == "":
                    value = 1  
                else:
                    value = float(output_label.text)
                if value <= 0:
                    output_label.text = "Error"
                else:
                    output_label.text = str(math.log10(value))
            except:
                output_label.text = "Error"

        def e_power_x(instance):
            try:
                if output_label.text == "":
                    exponent = 1  
                else:
                    exponent = float(output_label.text)
                output_label.text = str(math.e ** exponent)
            except:
                output_label.text = "Error"

        def power(instance):
            output_label.text += "^"

        def backspace(instance):
            output_label.text = output_label.text[:-1]

        def clear_label(instance):
            output_label.text = ""

        def clear_entry(instance):
            text = output_label.text
            if " " in text:
                text = text.rsplit(" ", 1)[0]
            else:
                text = ""
            output_label.text = text

        button_map = {
            '=': evaluate_result,
            '√x': square_root,
            'x²': square,
            '1/x': reciprocal,
            '⌫': backspace,
            'C': clear_label,
            'CE': clear_entry,
            'π' : pi,
            'log(': log,
            'e': e_power_x,
            '^' : power
        }

        for btn in buttons:
            if btn.text in button_map:
                btn.bind(on_press=button_map[btn.text])
            elif btn.text not in ('=', '√x', 'x²', '1/x', '⌫', 'C', 'CE','^','e','log(','π'):
                btn.bind(on_press=print_button_text)

        output_label.bind(height=resize_label_text)
        root_widget.add_widget(output_label)
        root_widget.add_widget(button_grid)

        return root_widget

MyApp().run()
