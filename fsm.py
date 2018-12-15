from transitions.extensions import GraphMachine

from utils import send_text_message
import requests
import datetime
from bs4 import BeautifulSoup

astro_chinese = ["牡羊座", "金牛座", "雙子座" ,"巨蟹座", "獅子座", "處女座", "天秤座", "天蠍座", "射手座", "摩羯座", "水瓶座", "雙魚座"]
astro_num = 0
date_str = datetime.datetime.now()

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_today(self, event):
        if event.get("message"):
            text = event['message']['text']
            birth = ""
            arg = ""
            try:
                birth = text.split(" ")[0]
                arg = text.split(" ")[1]
            except:
                return False
            try:
                cast_num = int(birth)
                # print(cast_num)
                if((cast_num>=101 and cast_num<=131) or (cast_num>=201 and cast_num<=229) or (cast_num>=301 and cast_num<=331) or (cast_num>=401 and cast_num<=430) or (cast_num>=501 and cast_num<=531) or (cast_num>=601 and cast_num<=630) or (cast_num>=701 and cast_num<=731) or (cast_num>=801 and cast_num<=831) or (cast_num>=901 and cast_num<=930) or (cast_num>=1001 and cast_num<=1031) or (cast_num>=1101 and cast_num<=1130) or (cast_num>=1201 and cast_num<=1231)):
                    if arg == '-t' :
                        self.decide_astro(cast_num)
                        return True
                    else :
                        return False
                else:
                    return False
            except:
                print("cast exception")
                return False
            # return text.lower() == 'go to state1'
        return False

    def is_going_to_hint(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '-hint'
        return False

    def is_going_to_detail(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '-detail'
        return False

    def is_going_to_init(self, event):
        if event.get("message"):
            text = event['message']['text']
            if text.lower() == '-exit':
                sender_id = event['sender']['id']
                send_text_message(sender_id, "請輸入:[Date] [-t|-n|-w|-m]\nDate:4位數生日日期\n-t:今日短評\n-n:明日運勢\n-w:本周運勢\n-m:本月運勢")
                return True
            else:
                return False
        return False

    def is_going_to_tomorrow(self, event):
        if event.get("message"):
            text = event['message']['text']
            birth = ""
            arg = ""
            try:
                birth = text.split(" ")[0]
                arg = text.split(" ")[1]
            except:
                return False
            try:
                cast_num = int(birth)
                if((cast_num>=101 and cast_num<=131) or (cast_num>=201 and cast_num<=229) or (cast_num>=301 and cast_num<=331) or (cast_num>=401 and cast_num<=430) or (cast_num>=501 and cast_num<=531) or (cast_num>=601 and cast_num<=630) or (cast_num>=701 and cast_num<=731) or (cast_num>=801 and cast_num<=831) or (cast_num>=901 and cast_num<=930) or (cast_num>=1001 and cast_num<=1031) or (cast_num>=1101 and cast_num<=1130) or (cast_num>=1201 and cast_num<=1231)):
                    if arg == '-n' :
                        self.decide_astro(cast_num)
                        return True
                    else :
                        return False
                else:
                    return False
            except:
                return False
            # return text.lower() == 'go to state1'
        return False

    def is_going_to_week(self, event):
        if event.get("message"):
            text = event['message']['text']
            birth = ""
            arg = ""
            try:
                birth = text.split(" ")[0]
                arg = text.split(" ")[1]
            except:
                return False
            try:
                cast_num = int(birth)
                if((cast_num>=101 and cast_num<=131) or (cast_num>=201 and cast_num<=229) or (cast_num>=301 and cast_num<=331) or (cast_num>=401 and cast_num<=430) or (cast_num>=501 and cast_num<=531) or (cast_num>=601 and cast_num<=630) or (cast_num>=701 and cast_num<=731) or (cast_num>=801 and cast_num<=831) or (cast_num>=901 and cast_num<=930) or (cast_num>=1001 and cast_num<=1031) or (cast_num>=1101 and cast_num<=1130) or (cast_num>=1201 and cast_num<=1231)):
                    if arg == '-w' :
                        self.decide_astro(cast_num)
                        return True
                    else :
                        return False
                else:
                    return False
            except:
                return False
            # return text.lower() == 'go to state1'
        return False

    def is_going_to_month(self, event):
        if event.get("message"):
            text = event['message']['text']
            birth = ""
            arg = ""
            try:
                birth = text.split(" ")[0]
                arg = text.split(" ")[1]
            except:
                return False
            try:
                cast_num = int(birth)
                if((cast_num>=101 and cast_num<=131) or (cast_num>=201 and cast_num<=229) or (cast_num>=301 and cast_num<=331) or (cast_num>=401 and cast_num<=430) or (cast_num>=501 and cast_num<=531) or (cast_num>=601 and cast_num<=630) or (cast_num>=701 and cast_num<=731) or (cast_num>=801 and cast_num<=831) or (cast_num>=901 and cast_num<=930) or (cast_num>=1001 and cast_num<=1031) or (cast_num>=1101 and cast_num<=1130) or (cast_num>=1201 and cast_num<=1231)):
                    if arg == '-m' :
                        self.decide_astro(cast_num)
                        return True
                    else :
                        return False
                else:
                    return False
            except:
                return False
            # return text.lower() == 'go to state1'
        return False

    def on_enter_state_today(self, event):
        global astro_num,astro_chinese,date_str
        print("I'm entering state_today")

        sender_id = event['sender']['id']
        send_text_message(sender_id, astro_chinese[astro_num] + " 今日短評:")

        url = "http://astro.click108.com.tw/daily_%s.php?iAstro=%s&iAcDay=%s" % (str(astro_num),str(astro_num),date_str.strftime("%Y-%m-%d"))
        resp = requests.get(url)
        # print(resp.status_code)
        soup = BeautifulSoup(resp.text, 'html.parser')
        today_brief_fortune = soup.find("div", {"class": "TODAY_WORD"})
        # print(today_brief_fortune.text)
        send_text_message(sender_id, today_brief_fortune.text)
        send_text_message(sender_id, "請輸入:[-detail|-hint|-exit]\n-detail:今日完整運勢\n-hint:今日幸運物\n-exit:結束查詢")

    def on_exit_state_today(self, event):
        print('Leaving state_today')

    def on_enter_state_hint(self, event):
        global astro_num,astro_chinese,date_str
        print("I'm entering state_hint")

        sender_id = event['sender']['id']
        send_text_message(sender_id, astro_chinese[astro_num] + " 今日幸運物:")
        
        url = "http://astro.click108.com.tw/daily_%s.php?iAstro=%s&iAcDay=%s" % (str(astro_num),str(astro_num),date_str.strftime("%Y-%m-%d"))
        resp = requests.get(url)
        # print(resp.status_code)
        soup = BeautifulSoup(resp.text, 'html.parser')
        lucky_item = soup.find("div", {"class": "TODAY_LUCKY"})
        split_line = lucky_item.text.strip().split("\n\n\n\n")
        lucky_item_str = "幸運數字:" + split_line[0] + "\n" + "幸運顏色:" + split_line[1] + "\n" +  "幸運方位:" + split_line[2] + "\n" + "幸運時辰:" + split_line[3] + "\n" + "幸運星座:" + split_line[4]
        # print(lucky_item_str)
        send_text_message(sender_id, lucky_item_str)
        send_text_message(sender_id, "請輸入:[-detail|-exit]\n-detail:今日完整運勢\n-exit:結束查詢")


    def on_exit_state_hint(self, event):
        print('Leaving state_hint')

    def on_enter_state_detail(self, event):
        global astro_num,astro_chinese,date_str
        print("I'm entering state_detail")

        sender_id = event['sender']['id']
        send_text_message(sender_id, astro_chinese[astro_num] + " 今日整體運勢:")
        url = "http://astro.click108.com.tw/daily_%s.php?iAstro=%s&iAcDay=%s" % (str(astro_num),str(astro_num),date_str.strftime("%Y-%m-%d"))
        resp = requests.get(url)
        # print(resp.status_code)
        soup = BeautifulSoup(resp.text, 'html.parser')
        detail_fortune = soup.find("div", {"class": "TODAY_CONTENT"})
        # print(detail_fortune.text)
        send_text_message(sender_id, detail_fortune.text)
        send_text_message(sender_id, "請輸入:[-hint|-exit]\n-hint:今日幸運物\n-exit:結束查詢")

    def on_exit_state_detail(self, event):
        print('Leaving state_detail')

    def on_enter_state_tomorrow(self, event):
        global astro_num,astro_chinese,date_str
        print("I'm entering state_tomorrow")

        sender_id = event['sender']['id']
        send_text_message(sender_id, astro_chinese[astro_num] + " 明日運勢:")

        url = "http://astro.click108.com.tw/daily_%s.php?iAcDay=%s&iAstro=%s&iType=4" % (str(astro_num),(date_str + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),str(astro_num))
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        tomo_brief_fortune = soup.find("div", {"class": "TODAY_WORD"})
        # print(tomo_brief_fortune.text)
        send_text_message(sender_id, tomo_brief_fortune.text)
        send_text_message(sender_id, "請輸入:[Date] [-t|-n|-w|-m]\nDate:4位數生日日期\n-t:今日短評\n-n:明日運勢\n-w:本周運勢\n-m:本月運勢")
        self.go_back()

    def on_exit_state_tomorrow(self):
        print('Leaving state_tomorrow')

    def on_enter_state_week(self, event):
        global astro_num,astro_chinese,date_str
        print("I'm entering state_week")

        sender_id = event['sender']['id']
        send_text_message(sender_id, astro_chinese[astro_num] + " 本周運勢:")

        url = "http://astro.click108.com.tw/daily_%s.php?iAcDay=%s&iAstro=%s&iType=1" % (str(astro_num),date_str.strftime("%Y-%m-%d"),str(astro_num))
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        week_brief_fortune = soup.find("div", {"class": "TODAY_WORD"})
        # print(week_brief_fortune.text)
        send_text_message(sender_id, week_brief_fortune.text.replace("\n\n",""))
        send_text_message(sender_id, "請輸入:[Date] [-t|-n|-w|-m]\nDate:4位數生日日期\n-t:今日短評\n-n:明日運勢\n-w:本周運勢\n-m:本月運勢")
        self.go_back()

    def on_exit_state_week(self):
        print('Leaving state_week')

    def on_enter_state_month(self, event):
        global astro_num,astro_chinese,date_str
        print("I'm entering state_month")

        sender_id = event['sender']['id']
        send_text_message(sender_id, astro_chinese[astro_num] + " 本月運勢:")
        url = "http://astro.click108.com.tw/daily_%s.php?iAcDay=%s&iAstro=%s&iType=2" % (str(astro_num),date_str.strftime("%Y-%m-%d"),str(astro_num))
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        month_brief_fortune = soup.find("div", {"class": "TODAY_WORD"})
        # print(month_brief_fortune.text)
        send_text_message(sender_id, month_brief_fortune.text.replace("\n\n",""))
        send_text_message(sender_id, "請輸入:[Date] [-t|-n|-w|-m]\nDate:4位數生日日期\n-t:今日短評\n-n:明日運勢\n-w:本周運勢\n-m:本月運勢")
        self.go_back()

    def on_exit_state_month(self):
        print('Leaving state_month')   

    def decide_astro(self, cast_num) :
        global astro_num
        if (cast_num>=120 and cast_num<= 218) :
            astro_num = 10
        elif (cast_num>=219 and cast_num<= 320) :
            astro_num = 11
        elif (cast_num>=321 and cast_num<= 419) :
            astro_num = 0
        elif (cast_num>=420 and cast_num<= 520) :
            astro_num = 1
        elif (cast_num>=521 and cast_num<= 621) :
            astro_num = 2
        elif (cast_num>=622 and cast_num<= 722) :
            astro_num = 3
        elif (cast_num>=723 and cast_num<= 822) :
            astro_num = 4
        elif (cast_num>=823 and cast_num<= 922) :
            astro_num = 5
        elif (cast_num>=923 and cast_num<= 1023) :
            astro_num = 6
        elif (cast_num>=1024 and cast_num<= 1122) :
            astro_num = 7
        elif (cast_num>=1123 and cast_num<= 1221) :
            astro_num = 8
        elif ((cast_num>=1222 and cast_num<= 1231) or (cast_num>=101 and cast_num<= 119) ) :
            astro_num = 9

