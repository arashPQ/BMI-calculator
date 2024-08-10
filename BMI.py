############################
####      Developer:    ####
####        Arash       ####
####        Paghe       ####
############################

import customtkinter as ctk
from customtkinter import CTkButton
from settings import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = Green)
        self.title("Volume Calculator")
        self.geometry("400x400")
        self.resizable(False, False)

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')


        # Data
        self.metric_bool = ctk.BooleanVar(value=True)
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=70)
        self.bmi_string = ctk.StringVar()
        self.update_bmi()


        # Tracing
        self.height_int.trace('w', self.update_bmi)
        self.weight_float.trace('w', self.update_bmi)

        self.metric_bool.trace('w', self.change_units)


        # Widgets

        ResultText(self, self.bmi_string)

        self.weight_input = WheightInput(self, self.weight_float, self.metric_bool)

        self.height_input = HeightInput(self, self.height_int, self.metric_bool)

        UnitSwitcher(self, self.metric_bool)

        self.mainloop()

    def change_units(self, *args):
        self.height_input.update_text(self.height_int)
        self.weight_input.update_weight()


    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter ** 2,2)

        self.bmi_string.set(bmi_result)


class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family=Font, size=Main_text_size, weight='bold')
        super().__init__(master=parent, text=22.5, font=font, text_color=White, textvariable=bmi_string)
        self.grid(column=0, row=0, rowspan=2, sticky='nsew')



class WheightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float, metric_bool):
        super().__init__(master=parent, fg_color=White)
        self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.weight_float = weight_float
        self.metric_bool = metric_bool



        self.output_string = ctk.StringVar()
        self.update_weight()

        # Layout

        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')

        # Widgets
        font = ctk.CTkFont(family=Font, size=Input_font_size)
        label = ctk.CTkLabel(self, textvariable = self.output_string, text_color=Black, font=font)
        label.grid(row=0, column=2)

        # Buttons

        minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'large')), text='-', font=font, text_color=Black, fg_color=Light_gray, hover_color=Gray, corner_radius=Btn_corner_radius)
        minus_button.grid(row=0, column=0, sticky='ns', padx=8, pady=8)

        plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'large')), text='+', font=font, text_color=Black, fg_color=Light_gray, hover_color=Gray, corner_radius=Btn_corner_radius)
        plus_button.grid(row=0, column=4, sticky='ns', padx=8, pady=8)

        small_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'small')), text='+', font=font, text_color=Black, fg_color=Light_gray, hover_color=Gray, corner_radius=Btn_corner_radius)
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)

        small_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'small')), text='-', font=font, text_color=Black, fg_color=Light_gray, hover_color=Gray, corner_radius=Btn_corner_radius)
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)

    def update_weight(self, info=None):
        if info:
            if self.metric_bool.get():
                amount = 1 if info[1] == 'large' else 0.1
            
            else:
                amount = 0.453592 if info[1] == 'large' else 0.453592 / 16
            
            
            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)

        if self.metric_bool.get():
            self.output_string.set(f'{round(self.weight_float.get(),1)}kg')
        else:
            raw_ounces = self.weight_float.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f'{int(pounds)}lb {int(ounces)}oz')


class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        font = ctk.CTkFont(family=Font, size=Input_font_size)
        super().__init__(master=parent, fg_color=White)
        self.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.metric_bool = metric_bool


        # Widgets

        slider = ctk.CTkSlider(master=self, 
                               command=self.update_text, 
                               button_color=Green, 
                               button_hover_color=Gray, 
                               progress_color=Green, 
                               fg_color=Light_gray, 
                               variable=height_int,
                               from_=100,
                               to=250)
        slider.pack(side='left', fill='x', expand=True, pady=10, padx=10)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())


        output_text = ctk.CTkLabel(self, textvariable=self.output_string, text_color=Black, font=font)
        output_text.pack(side='left', padx=20)


    def update_text(self, amount):
        if self.metric_bool.get():
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f'{meter}.{cm}m')
        else:
            feet, inches = divmod(amount / 2.54, 12)
            self.output_string.set(f'{int(feet)}\'{int(inches)}\"')

class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        super().__init__(master=parent, text='metric', text_color=Dark_green,
                          font=ctk.CTkFont(family=Font, size=Switch_font_size))
        self.place(relx=0.98, rely=0.01, anchor='ne')

        self.metric_bool = metric_bool
        self.bind('<Button>', self.change_units)

    def change_units(self, event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text="metric")
        else:
            self.configure(text="imperial")

if __name__ == '__main__':
    App()
