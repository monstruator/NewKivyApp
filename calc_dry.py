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
from kivymd.uix.list import  MDListItemSupportingText, MDListItemTertiaryText, MDListItemTrailingIcon, MDListItemHeadlineText
from kivy.utils import platform
from kivymd.uix.button import MDIconButton
from kivy.utils import get_color_from_hex
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox
from kivymd.uix.divider import MDDivider

from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
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
from circle_draw import * #circle_pic, circle_pic2, table_pic, table_pic2, rect_pic, table_rec_pic
from data_mass import point_quantity_circle, point_quantity_rectangle
# from kivy.lang import Builder

class Info():
    pass


class CalcDryScreen(MDScreen):
    id = None
    current_record = None
    check_box_choise1 = 0
    check_box_choise2 = 0
    count = 0
    selection_widget = None
    screen_width = 1000
    screen_height = 1000

    def on_enter(self):
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height

        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]

        self.add_componentes()

    def add_componentes(self):
        total_height = 0
        parent_widget = self.ids.custom_widget_box

        if self.selection_widget is not None:
            self.selection_widget.clear_widgets()
            self.selection_widget.height = 0
        else:
            self.selection_widget = MDBoxLayout(
                orientation="vertical",
                spacing="10dp"  # Adjust spacing as needed
            )
            parent_widget.add_widget(self.selection_widget)

        for child in parent_widget.children:
            total_height += child.height + 20
            # print(child, child.height)
        print("1 ", total_height)
        parent_widget.height = total_height 

        list_item = MDBoxLayout(
                md_bg_color = get_color_from_hex("#C4C4FF"), 
                adaptive_height=True, 
                orientation="vertical", 
                spacing="30dp", padding=["20dp", "20dp", "20dp", "20dp"]) 

        label0 = MDLabel(text="[b]Добавление компоненты[/b]", font_style="Title", role="medium",markup = True, )  # Adjust the width as needed
        list_item.add_widget(label0)

        name_component = MDTextField() #text=str(self.current_record[14]), #pos_hint={"center_x": .5},
        
        name_component.add_widget(MDTextFieldHintText(text="Компонент 2"))
        list_item.add_widget(name_component)

        label = MDLabel(text="Плотность 2 (кг/м³) = [color=#FFA500]1.964[/color]", markup = True, font_style="Title", role="medium")  # Adjust the width as needed
        list_item.add_widget(label)

        val1 = MDTextField()#text=str(self.current_record[14]), #pos_hint={"center_x": .5},)
        val1.add_widget(MDTextFieldHintText(text="Введите значение"))
        list_item.add_widget(val1)


        container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                #size_hint_x=None,
                #width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                adaptive_height=True,
                padding=["10dp", "20dp", "10dp", "20dp"],
                spacing="20dp",
            )
        ckeck1 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=1, id=str(0), group='group')#size_hint_x=None, width=label_width,
        label1 = MDLabel(text="кг/м³", font_style="Title", role="medium")

        ckeck2 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=0, id=str(0), group='group')#size_hint_x=None, width=label_width,
        label2 = MDLabel(text="г/моль", font_style="Title", role="medium")  
        #
        container.add_widget(ckeck1)
        container.add_widget(label1)
        container.add_widget(ckeck2)
        container.add_widget(label2)
        container.height = label1.height

        list_item.add_widget(container)

        label2 = MDLabel(text="Объемная доля 2 (%) = [color=#FFA500]0.214[/color]", markup = True, font_style="Title", role="medium")  # Adjust the width as needed
        list_item.add_widget(label2)

        val2 = MDTextField()#text=str(self.current_record[14]), #pos_hint={"center_x": .5},)
        val2.add_widget(MDTextFieldHintText(text="Введите значение"))
        list_item.add_widget(val2)


        container1 = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                #size_hint_x=None,
                #width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                adaptive_height=True,
                padding=["10dp", "20dp", "10dp", "20dp"],
                spacing="10dp",
            )
        ckeck3 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=1, id=str(0), group='group1')#size_hint_x=None, width=label_width,
        label3 = MDLabel(text="кг/м³", font_style="Title", role="small")
        ckeck4 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=0, id=str(0), group='group1')#size_hint_x=None, width=label_width,
        label4 = MDLabel(text="г/моль", font_style="Title", role="small")  
        ckeck5 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=1, id=str(0), group='group1')#size_hint_x=None, width=label_width,
        label5 = MDLabel(text="кг/м³", font_style="Title", role="small")
        ckeck6 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=0, id=str(0), group='group1')#size_hint_x=None, width=label_width,
        label6 = MDLabel(text="г/моль", font_style="Title", role="small")  
        container1.add_widget(ckeck3)
        container1.add_widget(label3)
        container1.add_widget(ckeck4)
        container1.add_widget(label4)
        container1.add_widget(ckeck5)
        container1.add_widget(label5)
        container1.add_widget(ckeck6)
        container1.add_widget(label6)

        container1.height = label6.height
        list_item.add_widget(container1)

        self.selection_widget.add_widget(list_item)

        # print(parent_widget.height)
        total_height = 0
        for child in list_item.children:
            total_height += child.height + 20
            print(child, child.height)
        print("self.selection_widget.height", self.selection_widget.height)
        print("list_item.height", list_item.height)
        print("total_height", total_height)
        parent_widget.height += total_height 
        print(parent_widget.height)

    def go_to_newrecods(self):
        print("go_to_newrecods")
        # MDDialog(
        #         title="Добавление компонента", 
        #         # type="custom",
        #         # size_hint=[.5, None],
        #         # content_cls=Info(),
        # ).open()
            # # MDDialogIcon(
            # #     icon="plus",
            # # ),
            # MDDialogHeadlineText(
            #     text="Добавление компонента",
            # ),
            
            # MDDialogContentContainer(
            #     MDListItem(
            #     # MDDialogButtonContainer(
            #         MDCheckbox(),
            #         MDLabel(text="кг/м3", markup = True, font_style="Body", role="small", halign='center'),
            #         MDCheckbox(),     
            #         MDLabel(text="г/моль", markup = True, font_style="Body", role="small", halign='center'),
            #     ),
            # ),
            
            # MDDialogContentContainer(
            #     MDListItem(
            #     # MDDialogButtonContainer(
            #         MDCheckbox(),
            #         MDLabel(text="кг/м3", markup = True, font_style="Body", role="small", halign='center'),
            #         MDCheckbox(),     
            #         MDLabel(text="г/моль", markup = True, font_style="Body", role="small", halign='center'),
            #     ),
            # ),
            
            # MDDialogContentContainer(
            #     MDListItem(
            #     # MDDialogButtonContainer(
            #         MDCheckbox(),
            #         MDLabel(text="кг/м3", markup = True, font_style="Body", role="small", halign='center'),
            #         MDCheckbox(),     
            #         MDLabel(text="г/моль", markup = True, font_style="Body", role="small", halign='center'),
            #     ),
            # ),
            

            

            # MDDialogButtonContainer(
            #     Widget(),
            #     MDButton(
            #         MDButtonText(text="Cancel"),
            #         style="text",
            #     ),
            #     MDButton(
            #         MDButtonText(text="Accept"),
            #         style="text",
            #     ),
            #     spacing="8dp",
            # ),
        


    def show_alert_dialog(self):
        print("show_alert_dialog")
        try:
            self.current_record[18] = float(self.ids.contr_tube.text)
            self.current_record[19] = float(self.ids.work_tube.text)
            self.current_record[20] = float(self.ids.temp_gas.text)
            self.current_record[21] = float(self.ids.p_dry_gas.text)
            self.current_record[22] = float(self.ids.f_wet_gas.text)
            self.update_record()
            print("save", self.current_record)
        except:
            print("Error float to str")
            text_err = "Введено неправильное значение"
            MDDialog(
                MDDialogHeadlineText(text="Ошибка сохранения записи",),
                MDDialogSupportingText(text=text_err,),
            ).open()

    def on_checkbox_active1(self, checkbox):
        if not self.check_box_choise1 == checkbox:
            self.current_record[23] = checkbox
            self.check_box_choise1 = checkbox
    
    def on_checkbox_active2(self, checkbox):
        if not self.check_box_choise1 == checkbox:
            self.current_record[24] = checkbox
            self.check_box_choise1 = checkbox
                
    def update_record(self):
        (record_id, name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length, form, diameter, min_side, max_side, double_quantity, n_points, contr_tube, work_tube, temp_gas, p_dry_gas, f_wet_gas, p_choise, f_choise, p_dry_calc, f_wet_calc) =  self.current_record
        update_record(record_id, name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length, form, diameter, min_side, max_side, double_quantity, n_points, contr_tube, work_tube, temp_gas, p_dry_gas, f_wet_gas, p_choise, f_choise, p_dry_calc, f_wet_calc)
#----------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------        
    
    #---------------------   ----------------------    ----------------------------   ------------------------
    def add_card(self, num_meas, meas):
        label_texts = []
        label_texts.append(f"[color=#000000]{str(num_meas)}[/color]")
        label_texts.append(f"[color=#00FF00]{str(num_meas)}[/color]")
        label_texts.append(f"[color=#0000FF]{str(129)}[/color]")
        label_texts.append(f"[color=#0000FF]{str(126)}[/color]")
        label_texts.append(f"[color=#0000FF]{str(-1649)}[/color]")
        label_texts.append(f"[color=#8F8040]{str(0.97)}[/color]")

        grid_layout = self.ids.custom_widget_box  # Accessing the MDGridLayout
        label_width = self.screen_width / 9
        
        widget_center = Widget()
        widget_center1 = Widget()
        widget_center2 = Widget()
        widget_center3 = Widget()

        list_item = MDListItem()
        
        icon_btn1 = MDIconButton(icon="file-edit",
                                pos_hint={'center_x': .1, 'center_y': .5},
                                on_release=lambda x: self.icon_del_click(list_item),
                                size_hint_x=None, width=label_width)
        
        list_item = MDBoxLayout(
                md_bg_color = get_color_from_hex("#C4C4FF"), 
                adaptive_height=True,  
                spacing="2dp", padding="5dp",) 

        ckeck1 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, size_hint_x=None, width=label_width)

        
        containers = []
        for text in label_texts:
            container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                size_hint_x=None,
                width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                padding=["5dp", "10dp", "5dp", "10dp"]
            )
            label = MDLabel(text=text, markup = True, font_style="Body", role="small", halign='center')  # Adjust the width as needed
            container.add_widget(label)
            containers.append(container)

        container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                size_hint_x=None,
                width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                padding=["5dp", "10dp", "5dp", "10dp"]
            )
        container.add_widget(widget_center)
        container.add_widget(ckeck1)
        container.add_widget(widget_center1)
        containers.insert(2, container)

        container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                size_hint_x=None,
                width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                padding=["5dp", "10dp", "5dp", "10dp"],
                adaptive_height=True,
            )
        container.add_widget(widget_center2)
        container.add_widget(icon_btn1)
        container.add_widget(widget_center3)
        containers.append(container)

        for el in containers:
            list_item.add_widget(el)
            grid_layout.height += list_item.height + self.selection_widget.spacing

        grid_layout.add_widget(list_item)

    #    -------------------- ------------------ ------------------- -------------------
    def add_table_title(self,):
        print("add_card")
        label_texts = []
        label_texts.append(f"[color=#000000][b]Изм[/b][/color]")
        label_texts.append(f"[color=#00FF00][b]Тчк[/b][/color]")
        label_texts.append(f"[color=#0000FF][b]В расч[/b][/color]")
        label_texts.append(f"[color=#0000FF][b]Рдр, Па[/b][/color]")
        label_texts.append(f"[color=#0000FF][b]Рдк, Па[/b][/color]")
        label_texts.append(f"[color=#8F8040][b]Рп, Па[/b][/color]")
        label_texts.append(f"[color=#8F8040][b]отн стор[/b][/color]")
        label_texts.append(f"[color=#000000][b]Ред[/b][/color]")
        
        grid_layout = self.ids.custom_widget_box  # Accessing the MDGridLayout

        list_item = MDListItem()
        
        label_width = self.screen_width / 9

        list_item = MDBoxLayout(
                md_bg_color = get_color_from_hex("#C4C4FF"), 
                adaptive_height=True,
                # height=30,
                spacing="2dp", padding="5dp",) 
    
        containers = []
        for text in label_texts:
            container = MDBoxLayout(
                #md_bg_color=get_color_from_hex("#F00490"),
                size_hint_x=None,
                adaptive_height=True,
                width=label_width,  # Adjust the width as needed
                #theme_bg_color="Custom"
                padding=["5dp", "12dp", "5dp", "12dp"]

            )
            label = MDLabel(text=text, markup = True, font_style="Body", role="small", halign='center')  # Adjust the width as needed
            container.add_widget(label)
            containers.append(container)

        
        # containers.insert(2, ckeck1)
        # containers.append(icon_btn1)

        for el in containers:
            list_item.add_widget(el)
            grid_layout.height += list_item.height + self.selection_widget.spacing

        grid_layout.add_widget(list_item)

        # self.ids.custom_widget_box.height
    