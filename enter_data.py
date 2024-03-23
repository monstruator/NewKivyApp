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
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
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
from kivy.lang import Builder


class EnterDataScreen(MDScreen):
    id = None
    current_record = None
    check_box_choise1 = 0
    check_box_choise2 = 0
    count = 0
    selection_widget = None
    screen_width = 0
    screen_height = 0
    Kk = 0
    Kr = 0

    def on_enter(self):
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height

        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]

        if self.current_record[12] == 1:
            self.ids.form_cut.text = f"Форма сечения: [b][color=#FFA500]  прямоугольная[/color][/b]"
            area = self.current_record[14] * self.current_record[15]
        else:
            self.ids.form_cut.text = f"Форма сечения: [b][color=#FFA500]  круглая[/color][/b]"
            diameter = self.current_record[13]
            area = pi * (diameter ** 2) / 4
        
        self.ids.area_cut.text = f"Площадь сечения: [b][color=#FFA500]{area:.3f}[/color][/b] м²"

        self.ids.n_points.text = f"Количество рабочих точек в сечении: [b][color=#FFA500]{self.current_record[17]}[/color][/b]"

        self.ids.contr_tube.text = "{:.3f}".format(self.current_record[18])
        self.ids.work_tube.text = "{:.3f}".format(self.current_record[19])
        self.ids.temp_gas.text = "{:.3f}".format(self.current_record[20])

        self.ids.p_dry_gas.text = "{:.3f}".format(self.current_record[21])
        self.ids.f_wet_gas.text = "{:.3f}".format(self.current_record[22])
        self.ids.p_dry_calc.text = "[color=#FFA5A0]На основании расчета[/color] p= [b][color=#FFA5A0]{:.3f}[/color][/b]  кг/м³".format(self.current_record[25])
        self.ids.f_wet_calc.text = "[color=#FFA5A0]На основании расчета[/color] p= [b][color=#FFA5A0]{:.3f}[/color][/b]  г/м³".format(self.current_record[26])
    
        if self.current_record[23] == 0:
            self.ids.dry_gas1.active = True
        elif self.current_record[23] == 1:
            self.ids.dry_gas2.active = True
        else:
            self.ids.dry_gas3.active = True

        if self.current_record[24] == 0:
            self.ids.wet_gas1.active = True
        elif self.current_record[24] == 1:
            self.ids.wet_gas2.active = True
        else:
            self.ids.wet_gas3.active = True
        
        if self.current_record[12] == 0:
            self.add_circle_main_layout()
        else:
            self.add_rectangle_main_layout()


    def show_alert_dialog(self):
        try:
            # if float(self.ids.contr_tube.text) > 0 and float(self.ids.work_tube.text) > 0:
            self.current_record[18] = float(self.ids.contr_tube.text)
            self.current_record[19] = float(self.ids.work_tube.text)
            self.current_record[20] = float(self.ids.temp_gas.text)
            self.current_record[21] = float(self.ids.p_dry_gas.text)
            self.current_record[22] = float(self.ids.f_wet_gas.text)
            self.update_record()
            # else:
            #     MDDialog(
            #         MDDialogHeadlineText(text="Ошибка ввода значений",),
            #         MDDialogSupportingText(text="Введено нулевое значение",),
            #     ).open()    
            
            if self.current_record[12] == 0:
                self.add_circle_main_layout()
            else:
                self.add_rectangle_main_layout()
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
            # print(self.current_record[23])
            # self.update_record()
    
    def on_checkbox_active2(self, checkbox):
        if not self.check_box_choise1 == checkbox:
            self.current_record[24] = checkbox
            self.check_box_choise1 = checkbox
            # print(self.current_record[24])
            # self.update_record()

    def update_record(self):
        (record_id, name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length, form, diameter, min_side, max_side, double_quantity, n_points, contr_tube, work_tube, temp_gas, p_dry_gas, f_wet_gas, p_choise, f_choise, p_dry_calc, f_wet_calc) =  self.current_record
        update_record(record_id, name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length, form, diameter, min_side, max_side, double_quantity, n_points, contr_tube, work_tube, temp_gas, p_dry_gas, f_wet_gas, p_choise, f_choise, p_dry_calc, f_wet_calc)
#----------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------        
    def add_circle_main_layout(self):
        total_height = 0
        parent_widget = self.ids.custom_widget_box
        # if platform == 'android':
        #     # self.ids.custom_widget_box.height = self.screen_height*1.5
        #     for child in self.ids.custom_widget_box.children:
        #         total_height += child.height
        #         print(child, child.height)
        #     print(total_height)
        #     self.ids.custom_widget_box.height = total_height
        # else:
        #     # self.ids.custom_widget_box.height = self.screen_height*0.6
        if self.selection_widget is not None:
            self.selection_widget.clear_widgets()
            self.selection_widget.height = 0
        else:

            self.selection_widget = MDBoxLayout(
                id="selection_widget",
                orientation="vertical",
                spacing="10dp"  # Adjust spacing as needed
            )
            parent_widget.add_widget(self.selection_widget)

        for child in parent_widget.children:
            total_height += child.height
            print(child, child.height)
        print(total_height)
        parent_widget.height = total_height

        diameter = self.current_record[13]
        if diameter > 0:
            if self.current_record[11] > 0:  #part_len
                spacer = Widget(size_hint_y=None, height="22dp")
                self.selection_widget.add_widget(spacer)
                self.image_layout = MDBoxLayout(theme_bg_color="Custom", size_hint_y=None, height=self.screen_width-50)
                sheme_id = MDLabel(text="Схема расположения рабочих точек:",  
                                   font_style="Title", role="medium", markup = True, 
                )
                self.selection_widget.add_widget(sheme_id)

                image_widget = FitImage()
                image_widget.source = "assets/circle_image.png"
                image_widget.reload()
                self.image_layout.add_widget(image_widget)
                self.selection_widget.add_widget(self.image_layout)

                parent_widget.height = parent_widget.height + self.screen_width*1.2

                measures = fetch_records_by_record_id(self.id)
                # print(measures)
                if len(measures) > 0:
                    label = MDLabel(
                        text="Давления в газоходе",
                        font_style="Title", role="medium", size_hint_y=None)
                    self.selection_widget.add_widget(label)
                    self.add_table_title()
                    for el in range(len(measures)):
                        self.add_card(el, measures[el])

        # for child in self.selection_widget.children:
        #     print(child) 
    #---------------------------------------------------    add_rectangle_main_layout ------------------------------
    def add_rectangle_main_layout(self):
        total_height = 0
        parent_widget = self.ids.custom_widget_box

        if self.selection_widget is not None:
            self.selection_widget.clear_widgets()
            self.selection_widget.height = 0
        else:
            self.selection_widget = MDBoxLayout(
                id="selection_widget",
                orientation="vertical",
                spacing="10dp"  # Adjust spacing as needed
            )
            parent_widget.add_widget(self.selection_widget)

        for child in parent_widget.children:
            total_height += child.height
            print(child, child.height)
        print(total_height)
        parent_widget.height = total_height

        
        if self.current_record[14] > 0 and self.current_record[15] > 0: #стороны
            if self.current_record[11] > 0:  #длины
                spacer = Widget(size_hint_y=None, height="22dp")
                self.selection_widget.add_widget(spacer)

                koef = self.current_record[15] /  self.current_record[14]
                height1 = self.screen_width / koef
                  
                sheme_id = MDLabel(text="Схема расположения рабочих точек:",  
                                   font_style="Title", role="medium", markup = True, 
                                #    size_hint=(None, None),  # Set size_hint to None
                                #    size=(400, 50),  # Set the size of the label (optional)
                                #     pos_hint={"center_x": 0.5, "center_y": 0.5}
                )
                self.selection_widget.add_widget(sheme_id)

                self.image_layout = MDBoxLayout(theme_bg_color="Custom", size_hint_y=None, height=height1)
                image_widget = FitImage()
                image_widget.source = rect_path
                image_widget.reload()
                self.image_layout.add_widget(image_widget)
                self.selection_widget.add_widget(self.image_layout)
                self.selection_widget.height = self.image_layout.height + sheme_id.height + 20
                print("self.selection_widget.height ", self.selection_widget.height)
                self.ids.custom_widget_box.height = self.ids.custom_widget_box.height + self.selection_widget.height

                measures = fetch_records_by_record_id(self.id)
                # print(measures)
                if len(measures) > 0:
                    label = MDLabel(
                        text="Давления в газоходе",
                        font_style="Title", role="medium", size_hint_y=None)
                    self.selection_widget.add_widget(label)
                    self.add_table_title()
                    for el in range(len(measures)):
                        self.add_card(el, measures[el])
        # new_height = sum(w.height for w in self.selection_widget.children) + self.selection_widget.spacing[1] * (len(grid_layout.children) - 1)
        # # Set the new height for the grid layout
        # self.selection_widget.height = new_height
    #---------------------   ----------------------    ----------------------------   ------------------------
    def add_card(self, num_meas, meas):
        label_texts = []
        label_texts.append(f"[color=#000000]{str(num_meas+1)}[/color]")
        label_texts.append(f"[color=#008F80]{str(meas[7])}[/color]")
        label_texts.append(f"[color=#0000FF]{str(meas[2])}[/color]")
        label_texts.append(f"[color=#0000FF]{str(meas[3])}[/color]")
        label_texts.append(f"[color=#0000FF]{str(meas[4])}[/color]")
        if not self.current_record[18] ==0 and not meas[3] == 0:
            var1 = sqrt((meas[2]*self.current_record[19])/(meas[3]*self.current_record[18]))
            # print(meas[2],self.current_record[19],meas[3],self.current_record[18])
            label_texts.append(f"[color=#8F8040]{var1:.2f}[/color]")
        else:
            label_texts.append(f"[color=#8F8040]-[/color]")

        grid_layout = self.ids.custom_widget_box  # Accessing the MDGridLayout
        label_width = self.screen_width / 8
        
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
                spacing="2dp", padding=["0dp", "20dp", "0dp", "20dp"]) 

        ckeck1 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, size_hint_x=None, width=label_width, active=meas[8], id=str(num_meas))
        ckeck1.bind(active=self.on_checkbox_active)
        
        containers = []
        for text in label_texts:
            container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                size_hint_x=None,
                width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                # padding=["15dp", "20dp", "0dp", "20dp"]
            )
            label = MDLabel(text=text, markup = True, font_style="Body", role="small", halign='center')  # Adjust the width as needed
            container.add_widget(label)
            containers.append(container)

        container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                size_hint_x=None,
                width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                # padding=["15dp", "20dp", "0dp", "20dp"]
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
                # padding=["15dp", "20dp", "0dp", "20dp"],
                adaptive_height=True,
            )
        container.add_widget(widget_center2)
        container.add_widget(icon_btn1)
        container.add_widget(widget_center3)
        # containers.append(container)

        for el in containers:
            list_item.add_widget(el)
            grid_layout.height += list_item.height + self.selection_widget.spacing

        self.selection_widget.add_widget(list_item)

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
        label_texts.append(f"[color=#8F8040][b]Отн скор[/b][/color]")
        # label_texts.append(f"[color=#000000][b]Ред[/b][/color]")
        
        grid_layout = self.ids.custom_widget_box  # Accessing the MDGridLayout

        list_item = MDListItem()
        
        label_width = self.screen_width / 8

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

        self.selection_widget.add_widget(list_item)

        # self.ids.custom_widget_box.height
    
    def on_checkbox_active(self, checkbox, value):
        measures = fetch_records_by_record_id(self.id)
        meas = measures[int(checkbox.id)]
        meas_list = list(meas)
        meas_list[8] = int(value)
        measurement = meas_list[2:]
        # print(meas_list, measurement)
        if update_measurement(meas_list[0],measurement):
                    # MDDialog(
                    #     MDDialogHeadlineText(text="Изменение измерения",),
                    #     MDDialogSupportingText(text="Успешно",),
                    # ).open()
            print()
        else:
            MDDialog(
                MDDialogHeadlineText(text="Изменение измерения",),
                MDDialogSupportingText(text="Ошибка",),
            ).open()
