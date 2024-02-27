from kaki.app import App 
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from mydb import *
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.relativelayout import  MDRelativeLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFabButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.fitimage import FitImage
from kivymd.uix.imagelist.imagelist import MDSmartTileImage
from kivy.utils import platform
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
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
from circle_draw import circle_pic, circle_pic2, table_pic, table_pic2
from data_mass import point_quantity_circle
from kivy.lang import Builder


class SectionScreen(MDScreen):
    id = None
    current_record = None
    check_box_choise = 0
    count = 0
    selection_widget = None
    screen_width = 1000
    screen_height = 1000

    def on_enter(self):
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height
        # if platform == 'android':
        #     self.ids.custom_widget_box.height = self.screen_height * 0.8
        # else:
        self.ids.custom_widget_box.height = self.screen_height * 0.7

        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]
        self.ids.proba_name_bar.text = self.current_record[1]
        self.ids.part_len.text = str(self.current_record[11]) #part_len
        print("switch active = ", self.current_record[16])
        self.ids.double_poins_id.active = self.current_record[16]
        #print("Form1: ",self.current_record[12]) 
        # measures = fetch_records_by_record_id(self.id)
        
        if self.current_record[12] == 0:
            self.ids.circle_checkbox.active = True
            self.ids.rectangle_checkbox.active = False
            self.add_circle_main_layout()
        else:
            self.ids.circle_checkbox.active = False
            self.ids.rectangle_checkbox.active = True
            self.add_rectangle_main_layout()

    def on_checkbox_active(self, checkbox):
        if not self.check_box_choise == checkbox:
            self.check_box_choise = checkbox
            self.current_record[12] = checkbox
            self.update_record()
            if checkbox == 0:
                print("circle")
                self.add_circle_main_layout()
            else:
                self.add_rectangle_main_layout()
                
    def update_record(self):
        (record_id, name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length, form, diameter, min_side, max_side, double_quantity) =  self.current_record
        update_record(record_id, name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length, form, diameter, min_side, max_side, double_quantity)
    
#---------------------------------------------------    add_rectangle_main_layout ------------------------------
    def add_rectangle_main_layout(self):
        if platform == 'android':
            self.ids.custom_widget_box.height = 1600
        else:
            self.ids.custom_widget_box.height = 600
        parent_widget = self.ids.custom_widget_box
        # selection_widget = self.ids.selection_widget
        if parent_widget is not None and self.selection_widget is not None:
            parent_widget.remove_widget(self.selection_widget)

    #----------------------------------------------------------------------------------------------------------
    def calculate_rectangle_area(self, instance):
        print(self.ids.part_len.text)
        diameter = 0
        area = 0
        try:
            diameter = float(self.diametr_id.text)
            area = pi * (diameter ** 2) / 4
            self.square_area_id.text = f"Площадь сечения: [b]{area:.4f}[/b]"
        except ValueError:
            self.square_area_id.text = "Площадь сечения: Неверный ввод"
        try:
            if area > 0:
                proportion = float(self.ids.part_len.text) / area
                self.proportion_id.text = f"Отношение линейного участка к диаметру: [b]{proportion:.4f}[/b]"
        except ValueError:
            self.proportion_id.text = "Отношение линейного участка к диаметру: Неверный ввод"
#----------------------------------------------------------------------------------------------------------
    def calculate_circle_area(self, instance):
        print(self.ids.part_len.text)
        diameter = 0
        area = 0
        try:
            diameter = float(self.diametr_id.text)
            area = pi * (diameter ** 2) / 4
            #self.square_area_id.text = f"Площадь сечения: [b][color=#FFA500]{area:.4f}[/color][/b]"
        except ValueError:
            self.square_area_id.text = "Площадь сечения: Неверный ввод"
        try:
            if area > 0:
                part_len = float(self.ids.part_len.text)
                #proportion = part_len / area
                #self.proportion_id.text = f"Отношение линейного участка к диаметру: [b][color=#FFA500]{proportion:.4f}[/color][/b]"
                self.current_record[13] = diameter
                self.current_record[11] = part_len
                self.update_record()
                self.add_circle_main_layout()
        except ValueError:
            self.proportion_id.text = "Отношение линейного участка к диаметру: Неверный ввод"
#------------------------------------------------------------------------------------------------------------        
    def add_circle_main_layout(self):
        if platform == 'android':
            self.ids.custom_widget_box.height = 1600
        else:
            self.ids.custom_widget_box.height = 600
        parent_widget = self.ids.custom_widget_box
        # selection_widget = self.ids.selection_widget
        if parent_widget is not None and self.selection_widget is not None:
            parent_widget.remove_widget(self.selection_widget)

        # selection_widget.clear_widgets()
        self.selection_widget = MDBoxLayout(
            id="selection_widget",
            orientation="vertical",
            spacing="10dp"  # Adjust spacing as needed
        )
        
        parent_widget.add_widget(self.selection_widget)
        text_field_width = self.screen_width / 2
        diameter_layout = MDBoxLayout(spacing = "44dp")
        #diameter_relative_layout = MDRelativeLayout()
        #label = MDLabel(text="Диаметр", size_hint_x=0.3, font_style="Title", role="medium", pos_hint={"center_y": .5})
        self.diametr_id = MDTextField(
                id="diametr_id", text=str(self.current_record[13]), #pos_hint={"center_x": .5},
                size_hint_x=None,
                width =  text_field_width
        )
        self.diametr_id.add_widget(MDTextFieldHintText(text="Диаметр"))
        # e,   on_text=self.calculate_area)
        # self.diametr_id.bind(on_text=self.calculate_area)
        button = MDFabButton(
            icon =  "calculator",
            style=  "standard",
            color_map =  "tertiary",
            size_hint_x=0.15,
            pos_hint={"center_x": .8},
            on_release=self.calculate_circle_area
            # theme_bg_color: "Custom"
            # md_bg_color: 0.4, .4, .7, 1
        )

        # diameter_relative_layout.add_widget(label)
        diameter_layout.add_widget(self.diametr_id)
        diameter_layout.add_widget(button)
        #diameter_layout.add_widget(diameter_relative_layout)
        self.selection_widget.add_widget(diameter_layout)          

        #area_layout = MDCard(padding="24dp", size_hint_y=None,  md_bg_color="red", theme_bg_color="Custom") #size_hint_y=None, size_y="120dp",
        # area_layout = MDBoxLayout()
        self.square_area_id = MDLabel(id="square_area_id", text="Площадь сечения: [b][color=#FFA500]0[/color][/b]", font_style="Title", role="medium", markup = True)
        # area_layout.add_widget(self.square_area_id)
        self.selection_widget.add_widget(self.square_area_id)

        #proportion_layout = MDBoxLayout()#MDCard(padding="24dp",  md_bg_color="red", theme_bg_color="Custom")
        self.proportion_id = MDLabel(id="proportion_id", text="Отношение линейного участка к диаметру: [b][color=#FFA500]0[/color][/b]",  font_style="Title", role="medium",  markup = True)
        #proportion_layout.add_widget(self.proportion_id)
        self.selection_widget.add_widget(self.proportion_id)

        poins_count_layout = MDBoxLayout()#MDCard(padding="24dp", md_bg_color="red", theme_bg_color="Custom")
        self.poins_count_id = MDLabel(id="poins_count_id", text="Количество рабочих точек: [b][color=#FFA500]0[/color][/b]",  font_style="Title", role="medium", markup = True)
        poins_count_layout.add_widget(self.poins_count_id)
        self.selection_widget.add_widget(poins_count_layout)

        # poins_doube_layout = MDBoxLayout(spacing = "44dp")#MDCard(padding="24dp", md_bg_color="red", theme_bg_color="Custom")
        # poins_count_id = MDLabel(id="poins_count_id", text="Удвоить число точек ",  font_style="Title", role="medium", markup = True, size_hint_x=None, width =  text_field_width)
        # point_swith = Builder.load_string(KV_switch)
        # #MDSwitch( pos_hint={"center_x": .8, "center_y": .5}, on_active=self.switch_text )
        # #point_swith.bind(on_active=self.on_switch_active)
        # poins_doube_layout.add_widget(poins_count_id)
        # poins_doube_layout.add_widget(point_swith)
        # self.selection_widget.add_widget(poins_doube_layout)

        diameter = self.current_record[13]
        if diameter > 0:
            area = pi * (diameter ** 2) / 4
            self.square_area_id.text = f"Площадь сечения: [b][color=#FFA500]{area:.4f}[/color][/b]"
            proportion = self.current_record[11] / area  #part_len / S
            self.proportion_id.text = f"Отношение линейного участка к диаметру: [b][color=#FFA500]{proportion:.4f}[/color][/b]"

            if self.current_record[11] > 0:  #part_len
                spacer = Widget(size_hint_y=None, height="22dp")
                self.selection_widget.add_widget(spacer)

                self.image_layout = MDBoxLayout(theme_bg_color="Custom", size_hint_y=None, height=self.screen_width-50)
                point_quantity = point_quantity_circle(diameter, self.current_record[11])  #11-part_len
                if self.current_record[16] == 1: # switch double points
                    point_quantity = point_quantity * 2
                self.poins_count_id.text = f"Количество рабочих точек: [b][color=#FFA500]{str(point_quantity)}[/color][/b]"
                
                if point_quantity > 2:
                    circle_pic(int(point_quantity/4))
                    table_pic(int(point_quantity/4), self.current_record[13]/2)
                else:
                    circle_pic2()
                    table_pic2(self.current_record[13]/2)    
                image_widget = FitImage()
                image_widget.source = "assets/circle_image.png"
                image_widget.reload()
                self.image_layout.add_widget(image_widget)
                self.selection_widget.add_widget(self.image_layout)

                spacer = Widget(size_hint_y=None, height="22dp")
                self.selection_widget.add_widget(spacer)
                
                # if platform == 'android':
                #     self.ids.custom_widget_box.height = self.screen_height * 0.8 + self.screen_width-50 + point_quantity*90 + 60
                #     self.image_layout1 = MDBoxLayout(theme_bg_color="Custom", size_hint_y=None, height=point_quantity*90+560)
                # else:
                koef = self.screen_width / 380
                table_height = (33 + point_quantity * 40) * koef
                print("table_height=", koef, table_height)
                print("point_quantity=",point_quantity, self.screen_width * point_quantity / 9, self.screen_width * point_quantity / 9 - 100)
                
                self.ids.custom_widget_box.height = self.screen_height*0.9 + self.screen_width-50 + table_height
                self.image_layout1 = MDBoxLayout(theme_bg_color="Custom", size_hint_y=None, height=table_height)
                
                image_widget1 = FitImage()
                image_widget1.source = "assets/table_image.png"
                image_widget1.reload()
                self.image_layout1.add_widget(image_widget1)
                self.selection_widget.add_widget(self.image_layout1)
                

    def double_points_switch(self, checkbox, value):
        if value:
            self.current_record[16] = 1
        else:
            self.current_record[16] = 0
        self.update_record()