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
        content=ft.Container(width=max_width,right=0,content=ft.Row(controls=[button_text,ft.Row(controls=[ft.Container(content=simbol,padding=ft.padding.all(5))],alignment=ft.MainAxisAlignment.END,width=45)],alignment=ft.MainAxisAlignment.END,spacing=0))
        self.content=ft.Stack(controls=[content])
        self.width=45
        self.height=34
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
        self.data=None
        self.child_custom_list=None
        self.father=None
    
    #Slide animation function
    def animate_button(self,e):
        if e.data == "true":
            self.width=self.max_width
        else:
            self.width=45
        self.update()

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
            self.father.command_value=e.control.value
            self.father.save()
    
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
            self.options: list=[ft.Container(content=ft.Row(controls=[ft.Text(value="Adicionar",weight='bold')]),height=40,on_click=self.new_option)]
            self.items=self.build_list_items
            self.controls=[self.build_list_button,self.items]
            self.items.animate=ft.Animation(300,ft.AnimationCurve.EASE_OUT)
            self.father.child_custom_list=self
        
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
            self.controls=[ft.TextField(label="Nova opção",on_submit=self.e_add_option)]
            self.update()

        def add_option(self,option_text):
            option=self.container_option(option_text,self)
            self.options.append(option)
            self.items.content=ft.Column(controls=self.options,expand=True,spacing=0,scroll=True)
            self.controls=[self.build_list_button,self.items]
            self.father.save()

        def e_add_option(self,e):
            self.add_option(e.control.value)
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
                self.father.father.save()
                return
            
    #Window create custom dropdown list input function
    def new_dropdown_cl(self,name,size,max_height=200):
        return self.custom_list(name,size,self,max_height)

    #delete icon class
    class delete_icon(ft.Container):
        def __init__(self,father):
            super().__init__()
            self.father=father
            self.content=ft.Icon(ft.Icons.DELETE_FOREVER,color=ft.Colors.WHITE)
        def 
    
    #general saver
    def save(self):
        general_saver={
            "text": self.textfield_saver,
            "list": self.custom_list_saver
        }
        general_saver[self.input_type]()
    
    #side button textfield saver
    def textfield_saver(self):
        side_button_data={
            "command_value":self.command_value,
            "name":self.text,
            "input_type":self.input_type,
            "simbol":self.simbol,
            "position":self.position
        }
        self.data.input(side_button_data)
    
    #custom dropdown list saver
    def custom_list_saver(self):
        custom_list_options=[]
        for i in self.child_custom_list.options:
            if i.content.controls[0].value!="Adicionar":
                custom_list_options.append(i.content.controls[0].value)
            else:
                continue
        side_button_data={
            "command_value":self.command_value,
            "name":self.text,
            "input_type":self.input_type,
            "simbol":self.simbol,
            "position":self.position,
            "options":custom_list_options
        }
        self.data.input(side_button_data)
    
    #general side_button data loader
    def load(self,side_button_data,window):
        general_side_button_loader={
            "text": self.textfield_sidebutton_loader,
            "list": self.custom_list_sidebutton_loader
        }
        general_side_button_loader[self.input_type](side_button_data,window)
    
    #textfield side_button loader
    def textfield_sidebutton_loader(self,side_button_data,window):
        self.window=window_builder(self,self.text,self.input_type)
        def window_event(e):
            window.content=self.window
            window.update()
            print("called")
        self.on_click=window_event
    
    #custom_list side_button loader
    def custom_list_sidebutton_loader(self,side_button_data,window):
        self.window=window_builder(self,self.text,self.input_type)
        def window_event(e):
            window.content=self.window
            window.update()
            window.window_user=self.position
        self.on_click=window_event
        for i in side_button_data["options"]:
            self.child_custom_list.add_option(i)
        if self.command_value!="":
            self.child_custom_list.value=self.command_value

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
    def delete_event(e):
        var.data.remove(var)
        var.father.remove(var)
        var.father.update()
        var.data.save()
    interface_generator={
            "text": lambda: var.new_input(f'{var_name} value',350),
            "list": lambda: var.new_dropdown_cl(f'{var_name} list',350)
        }
    base_window_content=build_single_centered_row([interface_generator[input_type]()])
    delete_icon=ft.Row(controls=[ft.Column(controls=[ft.Container(content=ft.Icon(ft.Icons.DELETE_FOREVER,color=ft.Colors.WHITE),padding=10,on_click=delete_event)],alignment=ft.MainAxisAlignment.START)],alignment=ft.MainAxisAlignment.END)
    built_window=ft.Stack(controls=[base_window_content,delete_icon])
    return built_window

#data saver class
class data_handler(dict):
    def __init__(self):
        super().__init__()
    
    #data input
    def input(self,new_data: dict):
        key_name=new_data.get("name")
        if key_name in self:
            self[key_name].update(new_data)
        else:
            self[key_name]=new_data
        self.save()
    
    #saver function
    def save(self):
        with open("GeneralData.json","w",encoding="utf-8") as file:
            json.dump(self,file,indent=4)

#general data loader
def data_loader(data: dict,buttons_list: list,window):
    sorted_data=sorted(data.values(),key=lambda x:x["position"])
    for i in sorted_data:
        new_side_button=side_button(i["name"],ft.Text(i["simbol"],color=ft.Colors.WHITE,weight="bold"))
        new_side_button.data=data
        new_side_button.input_type=i["input_type"]
        new_side_button.command_value=i["command_value"]
        new_side_button.position=i["position"]
        new_side_button.father=buttons_list
        new_side_button.load(i,window)
        buttons_list.append(new_side_button)

#window class
class window_class(ft.Container):
    def __init__(self):
        super().__init__()
        self.window_user=-1
        self.expand=True