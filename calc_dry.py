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
from kivy.metrics import dp
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
from mydb import *
# from kivy.lang import Builder

class Info():
    pass


class CalcDryScreen(MDScreen):
    id = None
    current_record = None
    check_box_choise1 = "0"
    check_box_choise2 = "0"
    count = 0
    selection_widget = None
    screen_width = 1000
    screen_height = 1000
    density = 0
    sum_density = 0
    part = 0
    components = None
    sum_of_parts = 0
    num_components = 0

    def on_enter(self):
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height

        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]
        print(self.current_record)
        self.add_componentes()
#----------------------------------------------------
    def icon_del_click(self, instance):
        print(instance.id)
        delete_component(self.id, self.components[int(instance.id)][0])
        self.add_componentes()
#-------------------------------------------------------------------------------------------------------
    def add_componentes(self):
        self.components = fetch_components_by_record_id(self.id)
        self.num_components = len(self.components)
        self.sum_of_parts = 0
        self.sum_density = 0
        # print("Components = ", self.num_components)
        for comp in self.components:
            # print(comp)
            self.sum_of_parts += comp[4] 
            self.sum_density += comp[3] * comp[4] 

        print(self.sum_density)
        self.sum_density += 1.293 * (100 - self.sum_of_parts)
        self.sum_density = self.sum_density / 100
        self.ids.air_part.text =  "Объемная доля (%) = " + str(100 - self.sum_of_parts)
        self.ids.density.text =  f"Плотность смеси газов [b]р=[color=#FFA500]{self.sum_density:.3f}[/color][/b]  кг/м³"
        self.current_record[25] = self.sum_density
        self.update_record()

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
            self.selection_widget.height = 0
            parent_widget.add_widget(self.selection_widget)

        comp_height = 0
        add_spacing_pixels = dp(35)
        if platform == 'android':
            add_spacing_pixels = dp(120)
        

        for comp_number, comp in enumerate(self.components):
            layout = MDBoxLayout(
                    adaptive_height=True, orientation="horizontal", spacing=dp(30), padding=[dp(10), dp(20), dp(10), dp(20)],
                    theme_bg_color="Custom",
                    md_bg_color = (0.6, .8, .9, 1)
                    )
            
            layout1 = MDBoxLayout(
                    adaptive_height=True, orientation="vertical", spacing=dp(30), padding=[dp(10), dp(20), dp(10), dp(20)],
                    theme_bg_color="Custom",
                    md_bg_color = (0.6, .8, .9, 1)
                    )
            layout2 = MDBoxLayout(
                    adaptive_height=True, orientation="vertical", spacing=dp(30), padding=[dp(10), dp(20), dp(10), dp(20)],
                    theme_bg_color="Custom",
                    md_bg_color = (0.6, .8, .9, 1),
                    size_hint_x = 0.2
                    )
            icon_btn1 = MDIconButton(icon="trash-can-outline",
                                pos_hint={'center_y': .5},
                                id = str(comp_number),
                                )
            icon_btn1.bind(on_release=self.icon_del_click)
            layout2.add_widget(icon_btn1)

            label1 = MDLabel(font_style="Title", role="medium", text="Компонент " + str(comp_number + 2) + " - " + comp[2])
            label2 = MDLabel(font_style="Title", role="medium", text="Плотность " + str(comp_number + 2) + " (кг/м³) = " + "{:.3f}".format(comp[3]))
            label3 = MDLabel(font_style="Title", role="medium", text="Объемная доля " + str(comp_number + 2) + " (%) = " + "{:.3f}".format(comp[4]))
            
            layout1.add_widget(label1)
            layout1.add_widget(label2)
            layout1.add_widget(label3)

            layout.add_widget(layout1)
            layout.add_widget(layout2)

            self.selection_widget.add_widget(layout)
            comp_height = int(comp_height + label1.height + add_spacing_pixels)
            # print(comp_number, comp_height, label1.height)
            

        add_spacing_pixels = dp(5)
        if platform == 'android':
            add_spacing_pixels = dp(20)

        for child in parent_widget.children:
            total_height = total_height + child.height + add_spacing_pixels
            # print(child, child.height, )
        # print("1 ", total_height)
        parent_widget.height = total_height + comp_height

        
        list_item = MDBoxLayout(
                md_bg_color = get_color_from_hex("#C4C4FF"), 
                adaptive_height=True, 
                orientation="vertical", 
                spacing="30dp", padding=["20dp", "20dp", "20dp", "20dp"]) 

        label0 = MDLabel(text="[b]Добавление компоненты[/b]", font_style="Title", role="medium",markup = True, )  # Adjust the width as needed
        list_item.add_widget(label0)

        self.name_component = MDTextField() #text=str(self.current_record[14]), #pos_hint={"center_x": .5},
        
        text_name = "Компонент " + str(self.num_components + 2)
        self.name_component.add_widget(MDTextFieldHintText(text=text_name))
        list_item.add_widget(self.name_component)

        self.label1 = MDLabel(text="Плотность " + str(self.num_components + 2) + " (кг/м³) = [color=#FFA500]0[/color]", markup = True, font_style="Title", role="medium")  # Adjust the width as needed
        list_item.add_widget(self.label1)

        self.val1 = MDTextField()         #text=str(self.current_record[14]), #pos_hint={"center_x": .5},)
        self.val1.bind(on_text_validate=self.on_text_changed1)
        self.val1.add_widget(MDTextFieldHintText(text="Введите значение"))
        list_item.add_widget(self.val1)


        container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                #size_hint_x=None,
                #width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                adaptive_height=True,
                padding=["10dp", "20dp", "10dp", "20dp"],
                spacing="20dp",
            )
        self.check1 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=1, id=str(0), group='group')#size_hint_x=None, width=label_width,
        self.check2 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=0, id=str(1), group='group')#size_hint_x=None, width=label_width,
        self.check1.bind(active=self.on_checkbox_active1)
        self.check2.bind(active=self.on_checkbox_active1)

        label1 = MDLabel(text="кг/м³", font_style="Title", role="medium")
        label2 = MDLabel(text="мг/моль", font_style="Title", role="medium")  

        container.add_widget(self.check1)
        container.add_widget(label1)
        container.add_widget(self.check2)
        container.add_widget(label2)
        container.height = label1.height

        list_item.add_widget(container)

        self.label2 = MDLabel(text="Объемная доля " + str(self.num_components + 2) + " (%) = [color=#FFA500]0[/color]", markup = True, font_style="Title", role="medium")  # Adjust the width as needed
        list_item.add_widget(self.label2)

        self.val2 = MDTextField()#text=str(self.current_record[14]), #pos_hint={"center_x": .5},)
        self.val2.add_widget(MDTextFieldHintText(text="Введите значение"))
        self.val2.bind(on_text_validate=self.on_text_changed2)
        list_item.add_widget(self.val2)


        container1 = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                #size_hint_x=None,
                #width=label_width,  # Adjust the width as needed
                # theme_bg_color="Custom",
                adaptive_height=True,
                padding=["10dp", "20dp", "10dp", "20dp"],
                spacing="5dp",
            )
        # font_size_dp = 10        # font_size_pixels = dp(font_size_dp)        # font_size=font_size_pixels
        self.check3 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=1, id=str(0), group='group1')#size_hint_x=None, width=label_width,  
        self.check4 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=0, id=str(1), group='group1')#size_hint_x=None, width=label_width,
        self.check5 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=0, id=str(2), group='group1')#size_hint_x=None, width=label_width,
        self.check6 = MDCheckbox(pos_hint={'center_x': .1, 'center_y': .5}, active=0, id=str(3), group='group1')#size_hint_x=None, width=label_width,
        self.check3.bind(active=self.on_checkbox_active2)
        self.check4.bind(active=self.on_checkbox_active2)
        self.check5.bind(active=self.on_checkbox_active2)
        self.check6.bind(active=self.on_checkbox_active2)
        
        # label3 = MDLabel(text="кг/м³", font_size=font_size_dp) 
        label3 = MDLabel(text="%", font_style="Body", role="small")
        label4 = MDLabel(text="г/моль", font_style="Body", role="small")  
        label5 = MDLabel(text="ppm", font_style="Body", role="small")
        label6 = MDLabel(text="кПа", font_style="Body", role="small")  
        
        
        container1.add_widget(self.check3)
        container1.add_widget(label3)
        container1.add_widget(self.check4)
        container1.add_widget(label4)
        container1.add_widget(self.check5)
        container1.add_widget(label5)
        container1.add_widget(self.check6)
        container1.add_widget(label6)

        container1.height = label6.height
        list_item.add_widget(container1)

        widget1 = Widget()
        widget2 = Widget()
        button_add = MDButton(
            # text="Добавить",
            theme_text_color="Custom",
            # etext_color="white",
            md_bg_color=(0.3, 0.3, 0.6, 1),
            #on_release=self.show_alert_dialog,
            on_release=lambda *args: self.show_alert_dialog(),
            style="filled", 
        )
        b_text = MDButtonText(text="Добавить компонент")
        button_add.add_widget(b_text)

        container2 = MDBoxLayout(
                adaptive_height=True,
                padding=["10dp", "20dp", "10dp", "20dp"],
                spacing="5dp",
        )
        container2.add_widget(widget1)
        container2.add_widget(button_add)
        container2.add_widget(widget2)
        container2.height = button_add.height
        list_item.add_widget(container2)

        self.selection_widget.add_widget(list_item)

        # print(parent_widget.height)
        total_height = 0
        for child in list_item.children:
            total_height += child.height + add_spacing_pixels
        #     print(child, child.height)
        # print("self.selection_widget.height", self.selection_widget.height)
        # print("list_item.height", list_item.height)
        # print("total_height", total_height)
        parent_widget.height += total_height 
        print(parent_widget.height)


    def on_text_changed1(self, instance_textfield):
        print(instance_textfield.text)
        try:
            if float(self.val1.text) > 0:
                self.density = float(self.val1.text)
                print(self.density)
                if self.check_box_choise1 == "1":
                    self.density = self.density / 22.4
                print(self.density)    
                self.label1.text = "Плотность "  + str(self.num_components + 2) + f" (кг/м³) = [color=#FFA500]{self.density:.3f}[/color]"
            self.calc_part() 
        except:
            print("Error2")
            self.part = 0
        self.label2.text = "Объемная доля " + str(self.num_components + 2) + f" (%) = [color=#FFA500]{self.part:.3f}[/color]"

    def calc_part(self):
        self.part = float(self.val2.text)
        print(self.part)
        if self.check_box_choise2 == "1":
            self.part = self.part / (self.density * 10000)
        if self.check_box_choise2 == "2":
            self.part = self.part / 10000
        if self.check_box_choise2 == "3":
            self.part = self.part / 1.013

    def on_text_changed2(self, instance_textfield):
        print("on_text_changed2 ", instance_textfield.text)
        try:
            if float(self.val2.text) > 0:
                self.calc_part()  
        except:
            print("Error3")
            self.part = 0
        self.label2.text = "Объемная доля " + str(self.num_components + 2) + f" (%) = [color=#FFA500]{self.part:.3f}[/color]"

    def go_to_newrecods(self):
        print("go_to_newrecods")


    def show_alert_dialog(self):
        print("show_alert_dialog")
        if self.part + self.sum_of_parts > 100:
            MDDialog(
                MDDialogHeadlineText(text="Введено неправильное значение",),
                MDDialogSupportingText(text="Превышение максимально допустимого значения доли компонента",),
            ).open()
            return
        if len(self.name_component.text) == 0:
            MDDialog(
                MDDialogHeadlineText(text="Введено неправильное значение",),
                MDDialogSupportingText(text="Введите название компонета",),
            ).open()
            return
        if self.density > 10:
            MDDialog(
                MDDialogHeadlineText(text="Введено неправильное значение",),
                MDDialogSupportingText(text="Превышение максимально допустимого значения плотности",),
            ).open()
            return
        try:
            component_details = (self.name_component.text, self.density, self.part)
            add_component(self.id, component_details)
            
            print("save", component_details)
            self.add_componentes()
        except:
            print("Error float to str")
            text_err = "Введено неправильное значение"
            MDDialog(
                MDDialogHeadlineText(text="Ошибка сохранения записи",),
                MDDialogSupportingText(text=text_err,),
            ).open()

    def on_checkbox_active1(self, checkbox, value):
        if not self.check_box_choise1 == checkbox.id:
            # self.current_record[24] = checkbox
            self.check_box_choise1 = checkbox.id
            print(checkbox.id)
            try:
                self.density = float(self.val1.text)
                print(self.density)
                if checkbox.id == "1":
                    self.density = self.density / 22.4
                print(self.density)    
                self.label1.text = "Плотность " + str(self.num_components + 2) + f" (кг/м³) = [color=#FFA500]{self.density:.3f}[/color]"
                self.calc_part() 
            except:
                # self.part = 0
                print("Error4")
            self.label2.text = "Объемная доля " + str(self.num_components + 2) + f" (%) = [color=#FFA500]{self.part:.3f}[/color]"
    
    def on_checkbox_active2(self, checkbox, value):
        #print(checkbox.id, value)
        if not self.check_box_choise2 == checkbox.id:
            # self.current_record[24] = checkbox
            self.check_box_choise2 = checkbox.id
            print(checkbox.id)
            try:
                self.calc_part() 
            except:
                self.part = 0
                print("Error5")
            self.label2.text = "Объемная доля " + str(self.num_components + 2) + f" (%) = [color=#FFA500]{self.part:.3f}[/color]"
        
                
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
    