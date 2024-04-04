from kaki.app import App 
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from mydb import *
from kivy.utils import platform
import math
from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget

if platform == 'android':
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        context = PythonActivity.mActivity
    except:
        print('Error11')

class TubeScreen(MDScreen):
    check_box_choise = 0
    id = 0

    def on_enter(self):
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height

        name =  App.get_running_app().current_record
        self.current_record = list(search_record(name))
        self.id = self.current_record[0]
        self.measures = fetch_records_by_record_id(self.id)
        self.record_name = name

        print(self.record_name)
        Pdr = 0
        Ppoln = 0
        Pct = 0
        Alfa = 0
        count_meas = 0
        try:
            for meas in self.measures:
                if meas[8] == 1: #in_calc
                    Pdr += math.sqrt(meas[2] * self.current_record[19])
                    Ppoln += meas[4]
                    Pct += meas[4] - (meas[2] * self.current_record[19])
                    if not self.current_record[18] == 0 and not meas[3] == 0:
                        Alfa += math.sqrt((meas[2]*self.current_record[19])/(meas[3]*self.current_record[18]))
                    count_meas += 1
            Pdr = (Pdr / count_meas) ** 2
            Ppoln = Ppoln / count_meas
            Pct = Pct / count_meas
            Alfa = Alfa / count_meas

            self.ids.box1.text2 = str(int(Pdr)) + " Па"
            self.ids.box2.text2 = str(int(Ppoln)) + " Па"
            self.ids.box3.text2 = str(int(Pct)) + " Па"
            # self.ids.box4.text2 = f"{Alfa:.2f}"


        except:
            print("Math error")
        Pgsnu = 0
        if self.current_record[23] == 0:
            Pgsnu = 1.293
        elif self.current_record[23] == 1:
            Pgsnu = self.current_record[21]
        elif self.current_record[23] == 2:
            Pgsnu = self.current_record[25]
        self.ids.box5.text2 = f"{Pgsnu:.2f}" + " г/м³"

        F = 0
        if self.current_record[24] == 0:
            F = 0
        elif self.current_record[24] == 1:
            F = self.current_record[22]
        elif self.current_record[24] == 2:
            F = self.current_record[26]

        Pgvlnu = (Pgsnu + F/1000)*0.804 / (0.804 + F/1000)
        self.ids.box6.text2 = f"{Pgvlnu:.2f}" + " г/м³"

        Pgvlru = Pgvlnu * 273 * (self.current_record[4] + Pct/1000) / (101.3 * (273 + self.current_record[5]))
        self.ids.box7.text2 = f"{Pgvlru:.2f}" + " кг/м³"

        # self.var1 = math.sqrt(2*Pdk/Pgvlru)
        Usr = math.sqrt(2 * Pdr / Pgsnu)
        self.ids.box8.text2 = f"{Usr:.2f}" + " м/с"

        if self.current_record[12] == 0:
            area = math.pi * (self.current_record[13] ** 2) / 4
        else:
            area = self.current_record[14] * self.current_record[15]
        Vgvlru = Usr * area
        self.ids.box9.text2 = f"{Vgvlru:.2f}" + " м³/с"

        Vgsru = Vgvlru * 0.804 / (0.804 + F/1000)
        self.ids.box10.text2 = f"{Vgsru:.2f}" + " м³/с"

        Vgsnu = Vgsru *273 * (self.current_record[4] + Pct/1000) / (101.3* (273 + self.current_record[5]))
        self.ids.box11.text2 = f"{Vgsnu:.2f}" + " м³/с"

        if platform == 'android':
            try:
                configuration = context.getResources().getConfiguration()
                font_scale = configuration.fontScale
                
                print("font_scale ", font_scale)
                if font_scale > 1.5:
                    self.ids.label_top.role = "small"
                    self.ids.label_top.font_style =  "Title"
                elif font_scale > 1.2:
                    self.ids.label_top.role = "medium"
                    self.ids.label_top.font_style =  "Hedline"
                else:
                    self.ids.label_top.role = "large"
                    self.ids.label_top.font_style = "Hedline"

            except Exception as e:
                print('Error get font_scale')
        
        if len(self.measures) > 0:
            Ut_mas = []
            for widget in self.ids.custom_widget_box.children[:]:
                if hasattr(widget, 'id') and widget.id == "table_item":
                    self.ids.custom_widget_box.remove_widget(widget)
            self.add_table_title()
            for point in range(0,self.current_record[17]):
                Ut = 0
                count_m = 0 
                for el in range(len(self.measures)):
                    # print("point", point, self.measures[el][7], point+1, self.measures[el][8])
                    if self.measures[el][7] == point+1 and self.measures[el][8] == 1 and not Pgvlru == 0: #совпадает номер точки и в расчете
                        Ut += math.sqrt(2 * self.measures[el][2] / Pgvlru)
                        count_m += 1
                if count_m > 0:
                    Ut = Ut / count_m
                    # print(point, count_m, Ut)
                    Ut_mas.append([point, Ut])
            
            # print(Ut_mas)
            for el in Ut_mas:
                self.add_card(el)

            #     if not self.current_record[19] ==0 and not meas[3] == 0 and meas[8] == 1:
            #         self.add_card(el, self.measures[el])
    

    def on_checkbox_active(self, checkbox):
        if not self.check_box_choise == checkbox:
            self.check_box_choise = checkbox
            print(self.check_box_choise)
                
#-----------------------------------------------------------------------------------------------------    
    def add_table_title(self):
        # print("add_title")
        label_texts = []
        label_texts.append(f"[color=#000000][b]Точка №[/b][/color]")
        label_texts.append(f"[color=#003333][b]Скорость в точке (м/с)[/b][/color]")
        # label_texts.append(f"[color=#0000FF][b]α в точке[/b][/color]")

        # list_item = MDListItem()       
        label_width = self.screen_width / 2.2

        list_item = MDBoxLayout(
                id = "table_item",
                # md_bg_color = get_color_from_hex("#C4C4FF"), 
                adaptive_height=True,
                # height=30,
                spacing="2dp", padding="5dp",) 
    
        containers = []
        for text in label_texts:
            container = MDBoxLayout(
                # md_bg_color=get_color_from_hex("#F00490"),
                # theme_bg_color="Custom",
                size_hint_x=None,
                adaptive_height=True,
                width=label_width,  # Adjust the width as needed
                padding=["5dp", "12dp", "5dp", "12dp"]
            )
            label = MDLabel(text=text, markup = True, font_style="Title", role="small", halign='center')  # Adjust the width as needed
            container.add_widget(label)
            containers.append(container)

        for el in containers:
            list_item.add_widget(el)
        # self.ids.custom_widget_box.height += list_item.height # + self.ids.custom_widget_box.spacing

        self.ids.custom_widget_box.add_widget(list_item)
#-----------------------------------------------------------------------------------------------------
    def add_card(self, Ut):
        label_texts = []
        print(Ut)
        label_texts.append(f"[color=#000000]{str(Ut[0]+1)}[/color]")
        label_texts.append(f"[color=#003333]{Ut[1]:.1f}[/color]")
        label_width = self.screen_width / 2.2
        
        # list_item = MDListItem()
        list_item = MDBoxLayout(
                id = "table_item",
                md_bg_color = get_color_from_hex("#C4C4FF"), 
                adaptive_height=True,  
                spacing="2dp", padding=["0dp", "20dp", "0dp", "20dp"]) 

        
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

        for el in containers:
            list_item.add_widget(el)
            #grid_layout.height += list_item.height + self.selection_widget.spacing

        self.ids.custom_widget_box.add_widget(list_item)
    

