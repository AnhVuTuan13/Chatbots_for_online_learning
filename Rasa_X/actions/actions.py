# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import  pandas as pd
import numpy as np

from datetime import  datetime, time
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

## Biến Cần dùng
timeStart=""
timeEnd=""
set_timeStart=time()
set_timeEnd=time()

class cancel_time(Action):

    def name(self) -> Text:
        return "action_cancel_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #So Sanh Time
        global timeStart,timeEnd,set_timeStart,set_timeEnd
        if  (timeStart != "")  &  (timeEnd != ""):
            timeStart = ""
            timeEnd = ""
            set_timeStart = time()
            set_timeEnd = time()
            dispatcher.utter_message(text="Thời gian điểm danh đã được đặt lại thành công ")
            dispatcher.utter_message(responses="utter_Time_point_list")
        else:
            dispatcher.utter_message(text=" Chưa cài đặt thời gian điểm danh !")
            dispatcher.utter_message(text="Start:" + timeStart + " - End: " + timeEnd)
        return []


class Get_Time_point_List(Action):

    def name(self) -> Text:
        return "action_Get_Time_point_List"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #So Sanh Time
        print("---------------action_Get_Time_point_List------------------")
        global timeStart,timeEnd,set_timeStart,set_timeEnd
        if  (timeStart != "")  &  (timeEnd != ""):
            dispatcher.utter_message(text="THời Gian đã đươc cài đặt rồi : Start:" +timeStart +" - End: "+timeEnd)
            dispatcher.utter_message(text="Để đặt lại thời gian điểm danh vui lòng nhắn : đặt lại diểm danh")
        else :
            try:
                print(tracker.latest_message['entities'])
                timeStart = tracker.latest_message['entities'][0]['value']
                print(timeStart)
                timeEnd = tracker.latest_message['entities'][1]['value']
                print(timeEnd)
                set_timeStart = time(int(timeStart.split(':')[0]), int(timeStart.split(':')[1]))
                print(set_timeStart)
                set_timeEnd = time(int(timeEnd.split(':')[0]), int(timeEnd.split(':')[1]))
                print(set_timeEnd)
            except:
                dispatcher.utter_message(text="Không Nhận được thời gian bắt đầu và kết thúc! ")
                dispatcher.utter_message(text="Vui Lòng Nhập đúng cú pháp để tránh lỗi! ")
                return []
            if(set_timeStart >= set_timeEnd):
                timeStart=""
                timeEnd=""
                dispatcher.utter_message(text="Không được để Thời gian bắt đầu Lớn hơn hoặc bằng thời gian kết thúc !!")
                dispatcher.utter_message(text="Vui Lòng Đặt lại Thời Gian !!!")
                dispatcher.utter_message(responses ="utter_Time_point_list")
            else:
                dispatcher.utter_message(text="Bạn Đã Đặt Thời gian thành công!")
                dispatcher.utter_message(text="Start:" +timeStart+" - End: "+timeEnd)

        return []


class Point_List(Action):

    def name(self) -> Text:
        return "action_Point_List"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global timeStart,timeEnd,set_timeStart,set_timeEnd
        print("---------------action_Point_List------------------")
        print(timeStart)
        print(timeEnd)
        print(set_timeStart)
        print(set_timeEnd)
        if (timeStart == "") & (timeEnd == ""):
            dispatcher.utter_message(text="Thời Gian Điểm danh chưa được dài đặt !")
            dispatcher.utter_message(responses="utter_Time_point_list")
        else:
            time_now=datetime.now().strftime("%H:%M")
            print(time_now)
            set_time_now = time(int(time_now.split(':')[0]), int(time_now.split(':')[1]))
            print(set_time_now)
            if(set_time_now < set_timeStart):
                dispatcher.utter_message(text="Chưa đến thời gian diểm danh!")
                dispatcher.utter_message(text="Thơi gian điểm danh là: Start:" + timeStart + " - End: " + timeEnd)
            elif (set_time_now > set_timeEnd):
                dispatcher.utter_message(text="Đã quá thời gian điểm danh!!")
            else:
                # opent file xlsx - convert 'Ma So SV' to String
                data = pd.read_excel(r"\DataSave\FileDiemDanh.xlsx", converters={'Mã số SV': str})
                # set col[Ma So SV ] to index
                data = data.set_index('Mã số SV')
                # get date now to add col
                date_now = datetime.now().strftime('%Y-%m-%d')
                if date_now not in data.columns:
                    data[date_now] = np.nan
                data.head()
                # get value fish entities
                try:
                    student_id = tracker.latest_message['entities'][0]['value']
                except:
                    dispatcher.utter_message("Không Xác định được Mã Sinh Viên")
                    return []
                if student_id in data.index:
                    data.loc[student_id, date_now] = "x"
                    text_urter = data.loc[student_id]['Họ và tên đệm'] + " " + data.loc[student_id]['Tên']
                    data.to_excel(r"\DataSave\FileDiemDanh.xlsx")
                    dispatcher.utter_message(
                        "Sinh Viên :" + text_urter + " - " + student_id + ". Đã Điểm Danh Thành Công")
                else:
                    dispatcher.utter_message("Sinh viên không có trong danh sách")
        return []
