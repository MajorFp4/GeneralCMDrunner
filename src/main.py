import flet
from functions import side_button, build_var_simbol, build_single_centered_row, window_builder
import subprocess

def main_screen(page: flet.Page):
    page.title='GeneralCMDrunner'
    page.window.width=700
    page.window.height=500
    page.padding=0
    window=""
    greater_position=0
    data=None

    #main var
    central_var_button=side_button("Variável central",flet.Text("VC",color=flet.Colors.WHITE,weight="bold"))
    def run_button_function(e):
        command_parts=[]
        for i in buttons_column.controls:
            part=i.command_value
            if part=="":
                continue
            elif i.text=="Variável central":
                continue
            else:
                command_parts.append(part)
        command_parts.append(central_var_button.command_value)
        command=" ".join(command_parts)
        subprocess.run(command,shell=True)
    def central_var(e):
        central_var_input=central_var_button.new_input("Test",300,False)
        run_button=flet.Container(content=flet.Text("RUN",color=flet.Colors.WHITE,weight="bold"),border_radius=15,on_click=run_button_function,bgcolor=flet.Colors.LIGHT_BLUE,width=50,alignment=flet.alignment.center,height=35)
        central_var_window=build_single_centered_row([central_var_input,run_button])
        window.content=central_var_window
        window.update()
    central_var_button.on_click_event(central_var)

    #add var
    add_var_button=side_button("Adicionar variável",flet.Icon(flet.Icons.ADD,color=flet.Colors.WHITE))
    new_var_name=""
    new_var_simbol=flet.Text(value="",size=70,color="#FFFFFF",weight='bold')
    
    var_type_dropdown=flet.Dropdown(width=185,label="Type",options=[flet.DropdownOption(key="text",text="Text field"),flet.DropdownOption(key="list",text="Dropdown list")])
    def edit_var_name_field(e):
        nonlocal new_var_name
        nonlocal new_var_simbol
        new_var_name=e.control.value
        new_var_simbol.value=build_var_simbol(new_var_name)
        window.update()
    var_name_input=flet.TextField(label="Variable name",width=363,on_change=edit_var_name_field)
    def create_var(e):
        error=False
        if not var_name_input.value or var_name_input.value.strip() == "":
            error=True
            var_name_input.error_text="Required"
        else:
            var_name_input.error_text=None
        if not var_type_dropdown.value:
            error=True
            var_type_dropdown.error_text="Required"
        else:
            var_type_dropdown.error_text=None
        if error:
            window.update()
            return
        new_var=side_button(new_var_name,flet.Text(new_var_simbol.value,color=flet.Colors.WHITE,weight="bold"))
        new_var_window=window_builder(new_var,new_var_name,var_type_dropdown.value)
        def set_new_var_window(event):
            window.content=new_var_window
            window.update()
        new_var.on_click_event(set_new_var_window)
        new_var.window=new_var_window
        new_var.input_type=var_type_dropdown.value
        new_var.simbol=new_var_name
        buttons_column.controls.append(new_var)
        page.update()
    def add_var(e):
        window.content=flet.Container(expand=True,content=flet.Row(controls=[flet.Column(controls=[flet.Container(
            height=page.height/1.2,
            width=page.width/1.2,
            border_radius=15,
            bgcolor="#1E1E1E",
            padding=30,
            content=flet.Column(spacing=50,controls=[
                flet.Text(value="Create new variable",color=flet.Colors.WHITE,weight='bold',size=30),
                flet.Row(controls=[
                    flet.Container(
                        border=flet.border.all(width=2,color="#313131"),
                        border_radius=5,
                        content=new_var_simbol,
                        height=150,
                        width=150,
                        alignment=flet.alignment.center,
                        padding=10
                        ),
                    flet.Column(
                        alignment=flet.MainAxisAlignment.START,spacing=20,controls=[
                        var_name_input,
                        flet.Row(controls=[
                            var_type_dropdown,
                            flet.TextField(
                                label="Initial value",
                                width=168
                                )
                            ]
                        )])
                ]),
                flet.Row(alignment=flet.MainAxisAlignment.END,controls=[
                    flet.ElevatedButton(text="Create variable",bgcolor=flet.Colors.BLUE_600,color=flet.Colors.WHITE,on_click=create_var)
                    ])
            ])
            )],alignment=flet.MainAxisAlignment.CENTER)],alignment=flet.MainAxisAlignment.CENTER))
        window.update()
    add_var_button.on_click_event(add_var)

    #screen content
    buttons_column=flet.Column(controls=[add_var_button,central_var_button],spacing=10,top=30,left=0)
    window=flet.Container(expand=True)
    screen=flet.Stack(controls=[
        window,
        buttons_column
        ],expand=True)

    page.add(screen)
    page.update()

flet.app(main_screen)