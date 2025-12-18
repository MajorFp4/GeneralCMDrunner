import flet
from functions import side_button

def main_screen(page: flet.Page):
    page.title='GeneralCMDrunner'
    page.window.width=700
    page.window.height=500
    page.padding=0
    
    Side_buttons=flet.Container(
        flet.Column(controls=[
            side_button("Adicionar variável",flet.Icons.ADD)
                ],spacing=10),
        margin=flet.margin.only(top=30)
    )

    page.add(Side_buttons)    
    page.update()
    
flet.app(main_screen)