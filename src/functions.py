import flet as ft
import json

#SideButton class
class side_button(ft.Container):
    def __init__(self,text,simbol):
        super().__init__()
        max_width=60+(len(text)*7)
        self.max_width=max_width
        self.text=text
        button_text=ft.Text(self.text,color=ft.Colors.WHITE,weight="bold",no_wrap=True)
        content=ft.Container(
            content=ft.Row(controls=[
                button_text,simbol
            ],alignment=ft.MainAxisAlignment.END,spacing=20),
        width=max_width,
        height=37,
        padding=ft.padding.only(right=10),
        right=0
        )
        self.content=ft.Stack(controls=[content])
        self.width=45
        self.height=37
        self.border_radius=ft.border_radius.only(top_right=10,bottom_right=10)
        self.bgcolor=ft.Colors.BLUE_GREY_900
        self.on_hover=self.animate_button
        self.animate=ft.Animation(300,ft.AnimationCurve.EASE_OUT)
        self.clip_behavior=ft.ClipBehavior.HARD_EDGE
        self.command_value=""
        self.window=None
        self.position=None
        self.input_type=None
        self.simbol=None

    #Set window to var
    def set_window(self,window_value):
        self.window=window_value
    
    #Slide animation function
    def animate_button(self,e):
        if e.data == "true":
            self.width=self.max_width
        else:
            self.width=45
        self.update()

    #Set on click event
    def on_click_event(self,event):
        self.on_click=event

    #command set value
    def command_set(self,command):
        self.command_value=command
    
    #window value input class
    class window_input(ft.TextField):
        def __init__(self,name,size,father,value):
            super().__init__()
            self.label=name
            self.width=size
            self.father=father
            self.value=value
            self.on_change=self.update
        def update(self,e):
            self.father.command_set(e.control.value)
            self.father.side_button_textfield_saver
    
    #window create value input function
    def new_input(self,name,size,remember=True):
        value=self.command_value
        if remember == False:
            self.command_value=""
            value=""
        return self.window_input(name,size,self,value)
    
    #Window custom dropdown list input class
    class custom_list(ft.Stack):
        def __init__(self,value :str,size: int,father,max_height: int):
            super().__init__()
            self.value=value
            self.width=size
            self.max_height=max_height
            self.father=father
            self.options: list=[ft.Container(ft.Row(controls=[ft.Text(value="Adicionar",weight='bold')]),height=40,on_click=self.new_option)]
            self.items=self.build_list_items
            self.controls=[self.build_list_button,self.items]
            self.items.animate=ft.Animation(300,ft.AnimationCurve.EASE_OUT)
        
        @property
        def build_list_button(self):
            built_list=ft.Container(
                    border=ft.border.all(2,color=ft.Colors.GREY),
                    border_radius=10,
                    content=ft.Text(value=self.value,weight='bold'),
                    alignment=ft.alignment.center_left,
                    height=40,
                    on_click=self.show_items,
                    padding=ft.padding.only(left=10)
                )
            return built_list
        
        @property
        def build_list_items(self):
            built_list=ft.Container(content=ft.Column(controls=self.options,expand=True,spacing=0,scroll=True),height=0,top=50,padding=ft.padding.only(left=10),border_radius=10,bgcolor=ft.Colors.BLUE_GREY,width=self.width)
            return built_list
        
        def show_items(self,e=None):
            items_height=len(self.options)*40
            total_height=items_height + 90
            self.items.height=(self.max_height if items_height >= self.max_height else items_height) if self.items.height == 0 else 0
            self.height=total_height
            self.update()

        def new_option(self,e):
            self.items.height=0
            self.controls=[ft.TextField(label="Nova opção",on_submit=self.add_option)]
            self.update()

        def add_option(self,e):
            option=self.container_option(e.control.value,self)
            self.options.append(option)
            self.items.content=ft.Column(controls=self.options,expand=True,spacing=0,scroll=True)
            self.controls=[self.build_list_button,self.items]
            self.update()

        class container_option(ft.Container):
            def __init__(self,value,father):
                super().__init__()
                self.value=value
                self.content=ft.Row(controls=[ft.Text(value=self.value,weight='bold'),ft.Container(expand=True,content=ft.Icon(ft.Icons.EDIT,color=ft.Colors.WHITE),alignment=ft.alignment.center_right,on_click=self.edit_option)],expand=True)
                self.height=40
                self.padding=ft.padding.only(right=10)
                self.father=father
                self.on_click=self.set_value
            
            def edit_option(self,e):
                for i in self.father.items.content.controls[1:]:
                    i.change_content()
                self.content=ft.TextField(value=self.value,on_submit=self.change_content,on_change=lambda e:setattr(self,'value',e.control.value),height=40)
                self.update()

            def change_content(self,e=None):
                self.content=ft.Row(controls=[ft.Text(value=self.value,weight='bold'),ft.Container(expand=True,content=ft.Icon(ft.Icons.EDIT,color=ft.Colors.WHITE),alignment=ft.alignment.center_right,on_click=self.edit_option)],expand=True)
                self.father.update()

            def set_value(self,e):
                self.father.value=self.value
                self.father.father.value=self.value
                self.father.father.command_value=self.value
                self.father.controls[0].content=ft.Text(self.value,weight='bold')
                self.father.show_items()
                return
            
    #Window create custom dropdown list input function
    def new_dropdown_cl(self,name,size,max_height=200):
        return self.custom_list(name,size,self,max_height)
    
    #loaders
    
    #simple textfield loader
    def load_textfield(vardict,window):
        textfield_button=side_button(vardict["text"],vardict["simbol"])
        def button_window(e):
            window.content=ft.Container(expand=True,content=ft.Column(
                controls=[ft.Row(controls=[side_button.new_input(f'{vardict["text"]} value',350)],
                alignment=ft.MainAxisAlignment.CENTER)],alignment=ft.MainAxisAlignment.CENTER
            ))
            window.update()
        textfield_button.on_click=button_window
        return textfield_button
    
    #side button textfield saver
    @property
    def side_button_textfield_saver(self):
        side_button_data={
            "command_value":self.command_value,
            "name":self.text,
            "input_type":self.input_type,
            "simbol":self.simbol,
            "position":self.position
        }
        with open("GeneralData.json","a",encoding="utf-8") as json_file:
            json_file.write(json.dump(side_button_data,json_file)+"\n")

#function for build the variables simbol
def build_var_simbol(var_name):
        var_name_words=var_name.split(" ")
        var_simbol=""
        for i in var_name_words:
            if len(i)>0:
                var_simbol+=i[0].upper()
        return var_simbol

#build single centered row function
def build_single_centered_row(row_controls: list):
    return ft.Column(controls=[ft.Row(controls=row_controls,alignment=ft.MainAxisAlignment.CENTER)],alignment=ft.MainAxisAlignment.CENTER)

def window_builder(var,var_name,input_type):
    interface_generator={
            "text": lambda: var.new_input(f'{var_name} value',350),
            "list": lambda: var.new_dropdown_cl(f'{var_name} list',350)
        }
    built_window=build_single_centered_row([interface_generator[input_type]()])
    return built_window

#data saver class
class data():
    def __init__(self,data_var):
        super().__init__()
        self.var=data_var
    
    #data input
    def input(self,data):
        1
    
    #saver function
    @property
    def save(self):
        with open("GeneralData","w",encoding="utf-8") as file:
            json.dump(self.var,file)