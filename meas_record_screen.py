from kaki.app import App 
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.screen import MDScreen
from mydb import *
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivy.utils import platform
from kivymd.app import MDApp

class MeasRecordScreen(MDScreen):
    dialog = None
    warning =None
    date = ""
    time = ""
    current_record = None
    current_meas = None
    id = None
    n_points = 0

    def update_meas(self):
        print("update_meas")
        p1 = p2 = p3 = p4 = p5 = 0
        if self.id:
            measures = fetch_records_by_record_id(self.id)
            if len(measures):
                self.dialog = MDDialog(
                    MDDialogIcon(icon="trash-can",),
                    MDDialogHeadlineText(text="Вы уверены, что хотите изменить запись?",),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(MDButtonText(text="Нет"), style="text", on_release=lambda *args: self.dialog.dismiss()),
                        MDButton(MDButtonText(text="Да"), style="text", on_release=lambda *args: self.update_meas_accept()),
                        spacing="8dp",
                    ),
                    # -------------------------------------------------------------
                )
                self.dialog.open()
    
    def update_meas_accept(self):
        self.dialog.dismiss()
        if self.id:
            measures = fetch_records_by_record_id(self.id)
            if len(measures):
                try:
                    p1 = float(self.ids.p1.text)
                    p2 = float(self.ids.p2.text)
                    p3 = float(self.ids.p3.text)
                    p4 = 0 #float(self.ids.p4.text)
                    p5 = 0 #float(self.ids.p5.text)
                    n_point = int(self.ids.n_point.text)
                    in_calc = self.ids.in_calc.active
                    measurement_details = (measures[self.current_meas][0], p1, p2, p3, p4, p5, n_point, in_calc)
                    if n_point > self.n_points:
                        MDDialog(
                            MDDialogHeadlineText(text="Ошибка ввода номера рабочей точки",),
                            MDDialogSupportingText(text="Номер рабочей точки не может превышать общего количества рабочих точек",),
                        ).open()
                        return
                except:
                    MDDialog(
                        MDDialogHeadlineText(text="Ошибка сохранения измерения",),
                        MDDialogSupportingText(text="Введены неправильные числовые значения. Убедитесь, что вещественные числа введены в формате ХХХ.ХХХ",),
                    ).open()
                    return     
                if update_measurement(self.id, measurement_details):
                    MDDialog(
                        MDDialogHeadlineText(text="Изменение измерения",),
                        MDDialogSupportingText(text="Успешно",),
                    ).open()
                else:
                    MDDialog(
                        MDDialogHeadlineText(text="Изменение измерения",),
                        MDDialogSupportingText(text="Ошибка",),
            ).open()

    def delete_meas(self):
        print("delete_meas")
        if self.id:
            measures = fetch_records_by_record_id(self.id)
            if len(measures) > 0:
                self.dialog = MDDialog(
                    MDDialogIcon(icon="trash-can",),
                    MDDialogHeadlineText(text="Вы уверены, что хотите удалить запись?",),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(MDButtonText(text="Нет"), style="text", on_release=lambda *args: self.dialog.dismiss()),
                        MDButton(MDButtonText(text="Да"), style="text", on_release=lambda *args: self.delete_meas_accept()),
                        spacing="8dp",
                    ),
                    # -------------------------------------------------------------
                )
                self.dialog.open()
                
    def delete_meas_accept(self):
        self.dialog.dismiss()
        if self.id:
            measures = fetch_records_by_record_id(self.id)
            if len(measures) > 0:
                if delete_measurement(measures[self.current_meas][0], self.id):
                    MDDialog(
                        MDDialogHeadlineText(text="Удаление измерения",),
                        MDDialogSupportingText(text="Успешно",),
                    ).open()
                    measures = fetch_records_by_record_id(self.id)
                    if len(measures) > 0:
                        self.current_meas = 0
                        self.ids.total_meas.text = str(len(measures))
                        self.ids.n_record.text = str(self.current_meas + 1)
                        self.ids.p1.text = str(measures[self.current_meas][2])
                        self.ids.p2.text = str(measures[self.current_meas][3])
                        self.ids.p3.text = str(measures[self.current_meas][4])
                        # self.ids.p4.text = str(measures[self.current_meas][5])
                        # self.ids.p5.text = str(measures[self.current_meas][6])
                        self.ids.n_point.text = str(measures[self.current_meas][7])
                        self.ids.in_calc.active = measures[self.current_meas][8]
                    else:
                        self.ids.total_meas.text = "0"
                        self.ids.n_record.text = "0"
                        self.ids.p1.text = "0"
                        self.ids.p2.text = "0"
                        self.ids.p3.text = "0"
                        # self.ids.p4.text = "0"
                        # self.ids.p5.text = "0"
                        self.ids.n_point.text = "0"
                        self.ids.in_calc.active = False
                else:
                    MDDialog(
                        MDDialogHeadlineText(text="Удаление измерения",),
                        MDDialogSupportingText(text="Ошибка",),
                    ).open()

    def next_meas(self):
        measures = fetch_records_by_record_id(self.id)
        if measures and self.current_meas < (len(measures) - 1):
            self.current_meas = self.current_meas + 1
            self.ids.n_record.text = str(self.current_meas + 1)
            self.ids.p1.text = str(measures[self.current_meas][2])
            self.ids.p2.text = str(measures[self.current_meas][3])
            self.ids.p3.text = str(measures[self.current_meas][4])
            # self.ids.p4.text = str(measures[self.current_meas][5])
            # self.ids.p5.text = str(measures[self.current_meas][6])
            self.ids.n_point.text = str(measures[self.current_meas][7])
            self.ids.in_calc.active = measures[self.current_meas][8]

    def prev_meas(self):
        measures = fetch_records_by_record_id(self.id)
        if measures and self.current_meas > 0:
            self.current_meas = self.current_meas - 1
            self.ids.n_record.text = str(self.current_meas + 1)
            self.ids.p1.text = str(measures[self.current_meas][2])
            self.ids.p2.text = str(measures[self.current_meas][3])
            self.ids.p3.text = str(measures[self.current_meas][4])
            # self.ids.p4.text = str(measures[self.current_meas][5])
            # self.ids.p5.text = str(measures[self.current_meas][6])
            self.ids.n_point.text = str(measures[self.current_meas][7])
            self.ids.in_calc.active = measures[self.current_meas][8]

    def new_meas(self):
        print("New meas", self.ids.in_calc.active)
        p1 = p2 = p3 = p4 = p5 = 0
        try:
            p1 = float(self.ids.p1n.text)
            p2 = float(self.ids.p2n.text)
            p3 = float(self.ids.p3n.text)
            p4 = 0 #float(self.ids.p4n.text)
            p5 = 0 #float(self.ids.p5n.text)
            n_point = int(self.ids.n_point_n.text)
            in_calc = self.ids.in_calc_n.active
            measurement_details = (measures[self.current_meas][0], p1, p2, p3, p4, p5, n_point, in_calc)
            if n_point > self.n_points:
                MDDialog(
                    MDDialogHeadlineText(text="Ошибка ввода номера рабочей точки",),
                    MDDialogSupportingText(text="Номер рабочей точки не может превышать общего количества рабочих точек",),
                ).open()
                return

        except:
            MDDialog(
                MDDialogHeadlineText(text="Ошибка сохранения измерения",),
                MDDialogSupportingText(text="Введены неправильные числовые значения. Убедитесь, что вещественные числа введены в формате ХХХ.ХХХ",),
            ).open()
            return
        if self.id:
            if add_measurement(self.id, measurement_details):
                measures = fetch_records_by_record_id(self.id)
                if measures:
                    MDDialog(
                        MDDialogHeadlineText(text="Добавление измерения",),
                        MDDialogSupportingText(text="Успешно",),
                    ).open()
                    self.ids.total_meas.text = str(len(measures))
                    if self.current_meas == None: # если еще не было записей
                        self.ids.n_record.text = "1"
                        self.current_meas = 0
                        self.ids.p1.text = str(measures[0][2])
                        self.ids.p2.text = str(measures[0][3])
                        self.ids.p3.text = str(measures[0][4])
                        # self.ids.p4.text = str(measures[0][5])
                        # self.ids.p5.text = str(measures[0][6])
                        self.ids.n_point.text = str(measures[0][7])
                        self.ids.in_calc.active = measures[0][8]
                else:
                    MDDialog(
                        MDDialogHeadlineText(text="Добавление измерения",),
                        MDDialogSupportingText(text="Ошибка",),
                    ).open()

    def on_enter(self):
        self.screen_width = MDApp.get_running_app().root.width
        self.screen_height = MDApp.get_running_app().root.height
        if platform == 'android':
            self.ids.custom_widget_box.height = self.screen_height*2
        else:
            self.ids.custom_widget_box.height = self.screen_height*0.6

        name =  App.get_running_app().current_record
        current_record = search_record(name)
        self.id = current_record[0]
        self.n_points = current_record[17]
        self.ids.proba_name_bar.text = current_record[1]
        print("Edit meas for item:",current_record) 
        measures = fetch_records_by_record_id(self.id)
        if measures:
            self.ids.total_meas.text = str(len(measures))
            print(measures[0])
            self.ids.n_record.text = "1"
            self.current_meas = 0
            self.ids.p1.text = str(measures[0][2])
            self.ids.p2.text = str(measures[0][3])
            self.ids.p3.text = str(measures[0][4])
            self.ids.n_point.text = str(measures[0][7])
            self.ids.in_calc.active = measures[0][8]
            # self.ids.p4.text = str(measures[0][5])
            # self.ids.p5.text = str(measures[0][6])
        else:
            self.ids.total_meas.text = "0"
            self.ids.n_record.text = "0"
            self.ids.p1.text = "0"
            self.ids.p2.text = "0"
            self.ids.p3.text = "0"
            # self.ids.p4.text = "0"
            # self.ids.p5.text = "0"
            self.ids.n_point.text = "0"
            self.ids.in_calc.active = False

