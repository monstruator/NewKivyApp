from kaki.app import App 
from kivymd.app import MDApp
from kivy.uix.widget import Widget
# from kivymd.uix.button import MDButton, MDButtonTexte
from kivymd.uix.screen import MDScreen
from mydb import *
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.relativelayout import  MDRelativeLayout
# from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFabButton
# from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.fitimage import FitImage
# from kivymd.uix.imagelist.imagelist import MDSmartTileImage
from kivy.utils import platform
# from kivymd.uix.dialog import (
#     MDDialog,
#     MDDialogIcon,
#     MDDialogHeadlineText,
#     MDDialogSupportingText,
#     MDDialogButtonContainer,
# )
from kivymd.uix.textfield import (
    MDTextField,
    MDTextFieldLeadingIcon,
    MDTextFieldHintText,
    MDTextFieldHelperText,
    MDTextFieldTrailingIcon,
    MDTextFieldMaxLengthText,
)
from math import pi
import time
from circle_draw import * #circle_pic, circle_pic2, table_pic, table_pic2, rect_pic, table_rec_pic
from data_mass import point_quantity_circle, point_quantity_rectangle
from kivy.lang import Builder


class TubeScreen(MDScreen):
    check_box_choise = 0

    def on_enter(self):
        pass
        # self.screen_width = MDApp.get_running_app().root.width
        # self.screen_height = MDApp.get_running_app().root.height
        # if platform == 'android':
        #     self.ids.custom_widget_box.height = self.screen_height
        # else:
        #     self.ids.custom_widget_box.height = self.screen_height * 0.7

        # name =  App.get_running_app().current_record
        # self.current_record = list(search_record(name))
        # self.id = self.current_record[0]
        # self.ids.proba_name_bar.text = self.current_record[1]
        # self.ids.part_len.text = str(self.current_record[11]) #part_len
        # print("switch active = ", self.current_record[16])
        # self.ids.double_poins_id.active = self.current_record[16]
        # #print("Form1: ",self.current_record[12]) 
        # # measures = fetch_records_by_record_id(self.id)
        
        # if self.current_record[12] == 0:
        #     self.ids.circle_checkbox.active = True
        #     self.ids.rectangle_checkbox.active = False
        #     self.add_circle_main_layout()
        # else:
        #     self.ids.circle_checkbox.active = False
        #     self.ids.rectangle_checkbox.active = True
        #     self.add_rectangle_main_layout()

    def on_checkbox_active(self, checkbox):
        if not self.check_box_choise == checkbox:
            self.check_box_choise = checkbox
            print(self.check_box_choise)
                
    

