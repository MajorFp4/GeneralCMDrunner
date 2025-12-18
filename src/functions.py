import flet as ft

#SideButton class
class side_button(ft.Container):
    def __init__(self,text,simbol):
        super().__init__()
        
        button_text=ft.Text(text,color=ft.Colors.WHITE,weight="bold",no_wrap=True)
        content=ft.Container(
            content=ft.Row(controls=[
                button_text,ft.Icon(simbol)
            ],alignment=ft.MainAxisAlignment.END,spacing=15),
        width=180,
        height=45,
        padding=ft.padding.only(right=10),
        right=0
        )
        self.content=ft.Stack(controls=[content])
        self.width=50
        self.height=40
        self.border_radius=ft.border_radius.only(top_right=10,bottom_right=10)
        self.bgcolor=ft.Colors.BLUE_GREY_900
        self.on_hover=self.animate_button
        self.animate=ft.Animation(300,ft.AnimationCurve.EASE_OUT)
        self.clip_behavior=ft.ClipBehavior.HARD_EDGE
    
    #Slide animation function
    def animate_button(self,e):
        if e.data == "true":
            self.width=180
        else:
            self.width=50
        self.update()