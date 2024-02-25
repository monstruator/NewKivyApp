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
from circle_draw import circle_pic
from data_mass import data_mas

class SectionScreen(MDScreen):
    id = None
    current_record = None
    check_box_choise = 0

    def on_enter(self):
        name =  App.get_running_app().current_record
        self.current_record = search_record(name)
        self.id = self.current_record[0]
        self.ids.proba_name_bar.text = self.current_record[1]
        print("Form1: ",self.current_record[12]) 
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
            if checkbox == 0:
                print("circle")
                self.add_circle_main_layout()
            else:
                self.add_rectangle_main_layout()
                

#---------------------------------------------------    add_rectangle_main_layout ------------------------------
    def add_rectangle_main_layout(self):
        selection_widget = self.ids.selection_widget
        selection_widget.clear_widgets()
        screen_width = MDApp.get_running_app().root.width
        text_field_width = screen_width / 2

        big_side = MDBoxLayout(spacing = "44dp")
        self.big_side = MDTextField(
                id="diametr_id", text="0", #pos_hint={"center_x": .5},
                size_hint_x=None,
                width =  text_field_width
        )
        self.big_side.add_widget(MDTextFieldHintText(text="Большая сторона"))
        big_side.add_widget(self.big_side)
        selection_widget.add_widget(big_side) 

        min_side = MDBoxLayout(spacing = "44dp")
        self.min_side = MDTextField(
                id="diametr_id", text="0", #pos_hint={"center_x": .5},
                size_hint_x=None,
                width =  text_field_width
        )
        self.min_side.add_widget(MDTextFieldHintText(text="Меньщая сторона"))
        button = MDFabButton(
            icon =  "calculator",
            style=  "standard",
            color_map =  "tertiary",
            size_hint_x=0.15,
            pos_hint={"center_x": .8},
            on_release=self.calculate_rectangle_area
        )
        min_side.add_widget(self.min_side)
        min_side.add_widget(button)
        selection_widget.add_widget(min_side)         

        self.square_area_id = MDLabel(text="Площадь сечения: [b][color=#FFA500]0[/color][/b]", font_style="Title", role="medium", markup = True)
        selection_widget.add_widget(self.square_area_id)

        self.eqviv_diametr_id = MDLabel(text="Эквивалентный диаметр: [b][color=#FFA500]0[/color][/b]", font_style="Title", role="medium", markup = True)
        selection_widget.add_widget(self.eqviv_diametr_id)

        self.proportion_id = MDLabel(text="Отношение линейного участка к эквивалентному диаметру: [b][color=#FFA500]0[/color][/b]",  font_style="Title", role="medium",  markup = True)
        selection_widget.add_widget(self.proportion_id)

        self.proportion_side_id = MDLabel(text="Отношение сторон: [b][color=#FFA500]0[/color][/b]",  font_style="Title", role="medium",  markup = True)
        selection_widget.add_widget(self.proportion_side_id)

        #poins_count_layout = MDBoxLayout()
        self.poins_count_id = MDLabel(text="Количество рабочих точек: [b][color=#FFA500]0[/color][/b]",  font_style="Title", role="medium", markup = True)
        #poins_count_layout.add_widget(self.poins_count_id)
        selection_widget.add_widget(self.poins_count_id)

        poins_doube_layout = MDBoxLayout(spacing = "44dp")
        poins_count_id = MDLabel(id="poins_count_id", text="Удвоить число точек ",  font_style="Title", role="medium", markup = True, size_hint_x=None, width =  text_field_width)
        point_swith = MDSwitch(pos_hint={"center_x": .8, "center_y": .5})
        poins_doube_layout.add_widget(poins_count_id)
        poins_doube_layout.add_widget(point_swith)
        selection_widget.add_widget(poins_doube_layout)

        spacer = Widget(size_hint_y=None, height="22dp")
        selection_widget.add_widget(spacer)

        image_layout = MDBoxLayout(md_bg_color="red", theme_bg_color="Custom", size_hint_y=None, height=screen_width)
        distaces = [100,100,100,100]
        circle_pic(distaces)

        image_widget = FitImage(source="assets/circle_image.png")
        image_layout.add_widget(image_widget)
        selection_widget.add_widget(image_layout)

        
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

    def calculate_circle_area(self, instance):
        print(self.ids.part_len.text)
        diameter = 0
        area = 0
        try:
            diameter = float(self.diametr_id.text)
            area = pi * (diameter ** 2) / 4
            self.square_area_id.text = f"Площадь сечения: [b][color=#FFA500]{area:.4f}[/color][/b]"
        except ValueError:
            self.square_area_id.text = "Площадь сечения: Неверный ввод"
        try:
            if area > 0:
                proportion = float(self.ids.part_len.text) / area
                self.proportion_id.text = f"Отношение линейного участка к диаметру: [b][color=#FFA500]{proportion:.4f}[/color][/b]"
        except ValueError:
            self.proportion_id.text = "Отношение линейного участка к диаметру: Неверный ввод"
        

    def add_circle_main_layout(self):
        #new_label = MDLabel(text="Диаметр", id=diametr_id)
        #selection_widget.add_widget(new_label)
        selection_widget = self.ids.selection_widget
        selection_widget.clear_widgets()
        screen_width = MDApp.get_running_app().root.width
                
        print(screen_width)
        # for child in selection_widget.children:
        #     if isinstance(child, MDBoxLayout) and child.id == main_rectangle_id:
        #         break
        # else: 
        diametr_id = "diametr_id"
        square_area_id = "square_area_id"
        proportion_id = "proportion_id"
        poins_count_id = "poins_count_id"
            #main_layout = MDBoxLayout(orientation="vertical", theme_text_color="Custom", id=main_rectangle_id, md_bg_color=[0, 0, 1, 1])
            

            # MDCard:
            # padding: "24dp"
            # size_hint_y: None
            # size_y: "60dp"
            # theme_bg_color:"Custom"
            # md_bg_color: self.theme_cls.primaryContainerColor

        # , md_bg_color=self.theme_cls.primaryContainerColor, theme_bg_color="Custom"

        #diameter_layout = MDCard(padding="24dp")
        text_field_width = screen_width / 2
        diameter_layout = MDBoxLayout(spacing = "44dp")
        #diameter_relative_layout = MDRelativeLayout()
        #label = MDLabel(text="Диаметр", size_hint_x=0.3, font_style="Title", role="medium", pos_hint={"center_y": .5})
        self.diametr_id = MDTextField(
                id="diametr_id", text="0", #pos_hint={"center_x": .5},
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
        selection_widget.add_widget(diameter_layout)          


        #area_layout = MDCard(padding="24dp", size_hint_y=None,  md_bg_color="red", theme_bg_color="Custom") #size_hint_y=None, size_y="120dp",
        # area_layout = MDBoxLayout()
        self.square_area_id = MDLabel(id="square_area_id", text="Площадь сечения: [b][color=#FFA500]0[/color][/b]", font_style="Title", role="medium", markup = True)
        # area_layout.add_widget(self.square_area_id)
        selection_widget.add_widget(self.square_area_id)

        #proportion_layout = MDBoxLayout()#MDCard(padding="24dp",  md_bg_color="red", theme_bg_color="Custom")
        self.proportion_id = MDLabel(id="proportion_id", text="Отношение линейного участка к диаметру: [b][color=#FFA500]0[/color][/b]",  font_style="Title", role="medium",  markup = True)
        #proportion_layout.add_widget(self.proportion_id)
        selection_widget.add_widget(self.proportion_id)

        poins_count_layout = MDBoxLayout()#MDCard(padding="24dp", md_bg_color="red", theme_bg_color="Custom")
        self.poins_count_id = MDLabel(id="poins_count_id", text="Количество рабочих точек: [b][color=#FFA500]0[/color][/b]",  font_style="Title", role="medium", markup = True)
        poins_count_layout.add_widget(self.poins_count_id)
        selection_widget.add_widget(poins_count_layout)

        poins_doube_layout = MDBoxLayout(spacing = "44dp")#MDCard(padding="24dp", md_bg_color="red", theme_bg_color="Custom")
        poins_count_id = MDLabel(id="poins_count_id", text="Удвоить число точек ",  font_style="Title", role="medium", markup = True, size_hint_x=None, width =  text_field_width)
        point_swith = MDSwitch(pos_hint={"center_x": .8, "center_y": .5})
        poins_doube_layout.add_widget(poins_count_id)
        poins_doube_layout.add_widget(point_swith)
        selection_widget.add_widget(poins_doube_layout)


        spacer = Widget(size_hint_y=None, height="22dp")
        selection_widget.add_widget(spacer)
    
        # MDSmartTile:
        # pos_hint: {"center_x": .5, "center_y": .5}
        # size_hint: None, None
        # size: "320dp", "320dp"
        # overlap: False

        # MDSmartTileImage:
        #     source: "bg.jpg"
        #     radius: [dp(24), dp(24), 0, 0]

        image_layout = MDBoxLayout(md_bg_color="red", theme_bg_color="Custom", size_hint_y=None, height=screen_width)
        distaces = [100,100,100,100]
        circle_pic(distaces)

        image_widget = FitImage(source="assets/circle_image.png")
        image_layout.add_widget(image_widget)
        selection_widget.add_widget(image_layout)