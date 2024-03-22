from kaki.app import App 
from kivymd.app import MDApp
# from kivymd.uix.button import MDButton, MDButtonTexte
from kivymd.uix.screen import MDScreen
from mydb import *
# from kivymd.uix.imagelist.imagelist import MDSmartTileImage
from kivy.utils import platform
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)


class ResultScreen(MDScreen):
    check_box_choise = 0
    id = 0
    measures = None

    def on_enter(self):
        self.ids.gost_checkbox.active = True
        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]
        self.measures = fetch_records_by_record_id(self.id)
        
        if len(self.measures) == 0:
            self.ids.calc_but.disabled = True 
            MDDialog(
                MDDialogHeadlineText(text="Ошибка",),
                MDDialogSupportingText(text="В серии нет измерений",),
            ).open()  

        

    def on_checkbox_active(self, checkbox):
        if not self.check_box_choise == checkbox:
            self.check_box_choise = checkbox
            print(self.check_box_choise)
                
    
    def choise_result(self):
        if self.check_box_choise == 0:
            if len(self.measures) > 0:
                print(self.measures)
                for meas in self.measures:
                    if meas[2] <= 0 or meas[3] <= 0:
                        self.ids.calc_but.disabled = True 
                        MDDialog(
                            MDDialogHeadlineText(text="Ошибка",),
                            MDDialogSupportingText(text="В серии есть измерения с отрицательными или нулевыми значениями. Исправьте измерения и вернитесь к расчету.",),
                        ).open()
                        return
                App.get_running_app().go_to_gost()
            else:
                self.ids.calc_but.disabled = True 
            
        else:
            App.get_running_app().go_to_tube()

