import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from demo_v2 import Demo
import threading
import time
import random

class MyThread(threading.Thread):
    def run(self):
        self.threadLife = True
        while self.threadLife:
            widget.update()
            form1.update()
            form2.update()
            time.sleep(0.1)
    def stop(self):
        self.threadLife = False

class MyWidget(QWidget):
    
    def __init__(self, form1, form2):
        super(MyWidget, self).__init__()
        
        self.form1 = form1
        self.form2 = form2
        
        self.createLayout()

        self.show()

    
    def createLayout(self):
        
        self.setWindowTitle("今晚吃什麼 ???")
        self.resize(300,100)

        self.initQuestion = QLabel("Which mode do you want ?")
        self.initQuestion.setAlignment(Qt.AlignCenter)
        self.mode1_btn = QPushButton("Mode 1")
        self.mode1_btn.clicked.connect(self.get_mode1_layout)
        self.mode2_btn = QPushButton("Mode 2")
        self.mode2_btn.clicked.connect(self.get_mode2_layout)

        init_layout = QGridLayout()
        init_layout.addWidget(self.initQuestion, 0, 1, 1, 4)
        init_layout.addWidget(self.mode1_btn, 1, 0, 4, 3)
        init_layout.addWidget(self.mode2_btn, 1, 3, 4, 3)

            
        ''' The query layout'''
#        self.send_query_btn = QPushButton("Send")
#        self.query_txt = QLineEdit()
#
#
#        query_layout = QHBoxLayout()
#        query_layout.addWidget(self.query_txt)
#        query_layout.addWidget(self.send_query_btn)

        ''' The selection layout '''
        

        
        hbox = QVBoxLayout()
        hbox.addWidget(self.initQuestion)
    
        self.setLayout(init_layout)
    
    def get_mode1_layout(self):
        self.close()

#        form1 = mode1()
#        form1.exec_()
        self.form1.show()
        self.form1.exec_()
        self.show()

    def get_mode2_layout(self):
        self.hide()
        self.form2.show()
        self.form2.exec_()
        self.show()

class mode1(QDialog):
    
    def __init__(self):
        super(mode1, self).__init__()
        self.resize(600, 650)
        
#        self.dialog = dialog

        self.find_rest = Demo()

        self.setWindowTitle("今晚吃什麼 ???")
        self.createLayout()
#        self.show()

    def createLayout(self):
        
        self.previous_btn = QPushButton(self)
        self.previous_btn.move(10, 620)
        self.previous_btn.setText("previous")
        self.previous_btn.clicked.connect(self.jump_to_main)
        
        self.send_query_btn = QPushButton("Send")
        self.send_query_btn.clicked.connect(self.get_restaurant_info)
        self.query_txt = QLineEdit()

        query_layout = QHBoxLayout()
        query_layout.addWidget(self.query_txt)
        query_layout.addWidget(self.send_query_btn)
#        query_layout.setAlignment(Qt.AlignTop)

        vbox = QVBoxLayout()
        vbox.addLayout(query_layout)
        
        self.img_label = []
        self.link_label = []
        self.result = []
        for i in range(5):
            
            self.img_label.append(QLabel())
            self.img_label[i].setFixedSize(150, 100)

            self.result.append(QLabel())
            self.result[i].setFixedSize(400, 40)
            
            self.link_label.append(QLabel())
            self.link_label[i].setFixedSize(400, 40)
            
            tmp = QVBoxLayout()
            tmp.addWidget(self.result[i])
            tmp.addWidget(self.link_label[i])
            
            hbox = QHBoxLayout()
            hbox.addWidget(self.img_label[i])
            hbox.addLayout(tmp)
            
            vbox.addLayout(hbox)
        
        
        vbox.setAlignment(Qt.AlignTop)

        self.setLayout(vbox)

    def get_restaurant_info(self):
        
        if len(self.query_txt.text()) == 0:
            self.show_message_box(0)
            return
        
        restaurant, address, trip_url, image_path = \
            self.find_rest.run_v1(self.query_txt.text())
        
        if len(restaurant) == 0:
            self.show_message_box(1)
            return
        
#        image_path = "./tmp.jpg"
        src = "https://www.tripadvisor.com.tw"
        for i in range(5):
            if i > (len(restaurant)-1):
                self.img_label[i].setVisible(False)
                self.result[i].setVisible(False)
                self.link_label[i].setVisible(False)
                continue
            scaledImg = QPixmap(image_path[i]).scaled(self.img_label[i].width(),
                                                      self.img_label[i].height(),
                                                      Qt.KeepAspectRatio)
            self.img_label[i].setPixmap(scaledImg)
            self.img_label[i].setVisible(True)
            
            self.result[i].setText("店名：{} \n地址：{}".format(
                                   restaurant[i] ,address[i]))
            self.result[i].setVisible(True)
            
            url = src + trip_url[i]
            
            urlLink = '''<a href="{url}" style="color:#0000ff;"><b>See it on TripAdvisor</b></a>'''.format(url=url)
            self.link_label[i].setText(urlLink)
            self.link_label[i].setOpenExternalLinks(True)
            self.link_label[i].setVisible(True)

    def show_message_box(self, type):
        if type == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
    
            msg.setText("You need to enter something")
            msg.setInformativeText("ex:火鍋")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
        
            msg.exec_()
        elif type == 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            
            msg.setText("We not found any matching")
            msg.setInformativeText("You should enter something else")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            
            msg.exec_()

    def jump_to_main(self):
        self.close()

class mode2(QDialog):
    
    def __init__(self):
        super(mode2, self).__init__()
        self.resize(800, 650)
        
        #        self.dialog = dialog
        self.find_rest = Demo()
        self.setWindowTitle("今晚吃什麼 ???")
        self.createLayout()
    #        self.show()
    
    def createLayout(self):
        
        self.previous_btn = QPushButton(self)
        self.previous_btn.move(10, 620)
        self.previous_btn.setText("previous")
        self.previous_btn.clicked.connect(self.jump_to_main)
        
        self.random_btn = QPushButton("我真的不知道吃什麼")
        self.random_btn.setFixedSize(200, 30)
        self.random_btn.clicked.connect(self.random_suggest)
        
        self.service_type = QLabel("服務態度")
        self.service_combo = QComboBox()
        self.service_combo.addItem("請選擇")
        self.service_combo.addItem("服務好")
        self.service_combo.addItem("沒差")
        self.service_combo.setFixedSize(120, 25)
        service_layout = QHBoxLayout()
        service_layout.addWidget(self.service_type)
        service_layout.addWidget(self.service_combo)
    
        self.rest_type = QLabel("餐廳種類")
        self.rest_combo = QComboBox()
        self.rest_combo.addItem("請選擇")
        self.rest_combo.addItem("中式")
        self.rest_combo.addItem("日式")
        self.rest_combo.addItem("韓式")
        self.rest_combo.addItem("美式")
        self.rest_combo.addItem("下午茶")
        self.rest_combo.addItem("brunch")
        self.rest_combo.addItem("隨意都可以")
        self.rest_combo.setFixedSize(120, 25)
        rest_layout = QHBoxLayout()
        rest_layout.addWidget(self.rest_type)
        rest_layout.addWidget(self.rest_combo)
        
        self.worth_type = QLabel("CP值")
        self.worth_combo = QComboBox()
        self.worth_combo.addItem("請選擇")
        self.worth_combo.addItem("CP值高")
        self.worth_combo.addItem("不在意")
        self.worth_combo.setFixedSize(120, 25)
        worth_layout = QHBoxLayout()
        worth_layout.addWidget(self.worth_type)
        worth_layout.addWidget(self.worth_combo)
        
        self.region_type = QLabel("用餐地區")
        self.region_combo = QComboBox()
        self.region_combo.addItem("請選擇")
        self.region_combo.addItem("北投區")
        self.region_combo.addItem("士林區")
        self.region_combo.addItem("內湖區")
        self.region_combo.addItem("中山區")
        self.region_combo.addItem("大同區")
        self.region_combo.addItem("松山區")
        self.region_combo.addItem("南港區")
        self.region_combo.addItem("信義區")
        self.region_combo.addItem("大安區")
        self.region_combo.addItem("中正區")
        self.region_combo.addItem("萬華區")
        self.region_combo.addItem("文山區")
        self.region_combo.addItem("隨意都可以")
        self.region_combo.setFixedSize(120, 25)
        region_layout = QHBoxLayout()
        region_layout.addWidget(self.region_type)
        region_layout.addWidget(self.region_combo)
        
        self.vegetarian_type = QLabel("素食")
        self.vegetarian_combo = QComboBox()
        self.vegetarian_combo.addItem("請選擇")
        self.vegetarian_combo.addItem("是")
        self.vegetarian_combo.addItem("否")
        self.vegetarian_combo.setFixedSize(120, 25)
        vegetarian_layout = QHBoxLayout()
        vegetarian_layout.addWidget(self.vegetarian_type)
        vegetarian_layout.addWidget(self.vegetarian_combo)
        
        self.pet_type = QLabel("寵物友善")
        self.pet_combo = QComboBox()
        self.pet_combo.addItem("請選擇")
        self.pet_combo.addItem("是")
        self.pet_combo.addItem("否")
        self.pet_combo.setFixedSize(120, 25)
        pet_layout = QHBoxLayout()
        pet_layout.addWidget(self.pet_type)
        pet_layout.addWidget(self.pet_combo)
        
        self.sender_btn = QPushButton("開始推薦!!")
        self.sender_btn.setFixedSize(100, 30)
        self.sender_btn.clicked.connect(self.get_restaurant_info)

        choice_layout = QVBoxLayout()
        choice_layout.addWidget(self.random_btn)
        choice_layout.addLayout(service_layout)
        choice_layout.addLayout(rest_layout)
        choice_layout.addLayout(worth_layout)
        choice_layout.addLayout(region_layout)
        choice_layout.addLayout(vegetarian_layout)
        choice_layout.addLayout(pet_layout)
        choice_layout.addWidget(self.sender_btn)
        choice_layout.setAlignment(Qt.AlignTop)
        
        vbox = QVBoxLayout()
        self.img_label = []
        self.link_label = []
        self.result = []
        for i in range(5):
            
            self.img_label.append(QLabel())
            self.img_label[i].setFixedSize(150, 100)
            
            self.result.append(QLabel())
            self.result[i].setFixedSize(400, 40)
            
            self.link_label.append(QLabel())
            self.link_label[i].setFixedSize(400, 40)
            
            tmp = QVBoxLayout()
            tmp.addWidget(self.result[i])
            tmp.addWidget(self.link_label[i])
            
            hbox = QHBoxLayout()
            hbox.addWidget(self.img_label[i])
            hbox.addLayout(tmp)
            
            vbox.addLayout(hbox)
        
        layout = QHBoxLayout()
        layout.addLayout(choice_layout)
        layout.addLayout(vbox)
    
        self.setLayout(layout)
            
    def get_restaurant_info(self):

        if self.service_combo.currentIndex() == 0:
            self.show_message_box(combo_box = self.service_type.text())
        elif self.rest_combo.currentIndex() == 0:
            self.show_message_box(combo_box = self.rest_type.text())
        elif self.worth_combo.currentIndex() == 0:
            self.show_message_box(combo_box = self.worth_type.text())
        elif self.region_combo.currentIndex() == 0:
            self.show_message_box(combo_box = self.region_type.text())
        elif self.pet_combo.currentIndex() == 0:
            self.show_message_box(combo_box = self.pet_type.text())
        elif self.vegetarian_combo.currentIndex() == 0:
            self.show_message_box(combo_box = self.vegetarian_type.text())
                
        else:
            
            if self.service_combo.currentIndex() == len(self.service_combo)-1:
                service = None
            else:
                service = str(self.service_combo.currentText())
            if self.rest_combo.currentIndex() == len(self.rest_combo)-1:
                category = None
            else:
                category = str(self.rest_combo.currentText())
            if self.worth_combo.currentIndex() == len(self.worth_combo)-1:
                worth = None
            else:
                worth = str(self.worth_combo.currentText())
            if self.region_combo.currentIndex() == len(self.region_combo)-1:
                region = None
            else:
                region = str(self.region_combo.currentText())
            if self.vegetarian_combo.currentIndex() == len(self.vegetarian_combo)-1:
                vege = None
            else:
                vege = self.vegetarian_type.text()
            if self.pet_combo.currentIndex() == len(self.pet_combo)-1:
                pet = None
            else:
                pet = self.pet_type.text()
            
            print (service)
            print (category)
            print (worth)
            print (region)
            print (vege)
            print (pet)
            
            restaurant, address, trip_url, image_path = \
                        self.find_rest.run_v2(district=region,
                                              category=category,
                                              pet=pet,
                                              cp=worth,
                                              service=service,
                                              vege=vege)
            if len(restaurant) == 0:
                self.show_message_box(type=1)
                return
            
            

#            image_path = "./tmp.jpg"
            src = "https://www.tripadvisor.com.tw"
            for i in range(5):
                scaledImg = QPixmap(image_path[i]).scaled(self.img_label[i].width(),
                                                          self.img_label[i].height(),
                                                          Qt.KeepAspectRatio)
                self.img_label[i].setPixmap(scaledImg)
                
                self.result[i].setText("店名：{} \n地址：{}".format(
                                    restaurant[i] ,address[i]))
#                self.result[i].setText(restaurant[i]+"\n"+address[i])
                url = src + trip_url[i]

                urlLink = '''<a href="{url}" style="color:#0000ff;"><b>See it on TripAdvisor</b></a>'''.format(url=url)
                self.link_label[i].setText(urlLink)
                self.link_label[i].setOpenExternalLinks(True)
                
    def random_suggest(self):
        category = ["中式", "日式", "韓式", "美式", "下午茶", "brunch"]
        random.seed(time.time())
        index = random.randint(0, 5)
        
        restaurant, address, trip_url, image_path = self.find_rest.run_v2(category=category[index])
        
#        image_path = "./tmp.jpg"
        src = "https://www.tripadvisor.com.tw"
        for i in range(5):
            scaledImg = \
                QPixmap(image_path[i]).scaled(self.img_label[i].width(),
                                           self.img_label[i].height(),
                                           Qt.KeepAspectRatio)
            self.img_label[i].setPixmap(scaledImg)
            
            self.result[i].setText("店名：{} \n地址：{}".format(
                                        restaurant[i] ,address[i]))
#            self.result[i].setText(restaurant[i]+"\n"+address[i])

            url = src + trip_url[i]

            urlLink = '''<a href="{url}" style="color:#0000ff;"><b>See it on TripAdvisor</b></a>'''.format(url=url)
            self.link_label[i].setText(urlLink)
            self.link_label[i].setOpenExternalLinks(True)

    def show_message_box(self, combo_box=None, type=None):
        if type == 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            
            msg.setText("We not found any matching")
            msg.setInformativeText("You should make your choice different")
            msg.setWindowTitle("Alert")
            msg.setStandardButtons(QMessageBox.Ok)
            
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            
            msg.setText("You have some blank did not make choice")
            msg.setInformativeText(combo_box+"還沒做選擇喔")
            msg.setWindowTitle("Alert")
#            msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QMessageBox.Ok)
            
            msg.exec_()

    def jump_to_main(self):
        self.close()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    form1 = mode1()
    form2 = mode2()
    
    widget = MyWidget(form1, form2)
    
    t = MyThread()
    t.setDaemon(True)
    t.start()
    
    app.exec_()
    
    t.stop()
    t.join()
#    sys.exit(app.exec_())
