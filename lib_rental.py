import sys
import json
import os
import pickle                                                                               # 바이너리 형태로 암호화 하기 위해 사용
import datetime                                                                             # 책을 대여한 시점 시간을 구하기 위해 사용
from PySide6.QtWidgets import QApplication,QMainWindow,QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt, QFile
from PySide6.QtUiTools import QUiLoader



# 초기 파일 경로 변수
json_book_file = "./data/book.json" 
json_rent_file = "./data/rent.json"
json_user_file = "./data/user.json"

pickle_book_file = "./data/book.pkl"
pickle_rent_file = "./data/rent.pkl"
pickle_user_file = "./data/user.pkl"



def json_write(pickle_file, json_file):                                                  # 피클파일 제이슨 파일로 변환  처음 인자에 피클 파일 경로 두번째 인자에 josn파일 경로                                                   
    with open(pickle_file, "rb") as fr:                                                     # 피클파일 로드 
        pickle_data = pickle.load(fr)                                                       
        
    with open(json_file, "w", encoding="utf-8") as fw:
        json.dump(pickle_data, fw, ensure_ascii=False, indent=4)                         # 제이슨 파일로 피클데이터 저장 한글안깨지게, 들여쓰기 4칸

        

def file_load(file):                                                                        # 파일 로드 
    with open(file, "r", encoding="utf-8") as fr:
        return json.load(fr)
    

def file_save(value, file):                                                                 # 파일 값 저장
    with open(file, "w", encoding="utf-8") as fw:
        json.dump(value, fw, ensure_ascii=False, indent=4)
        
def pickle_save(value, pickle_file):                                                                    # 최종적으로 정보 피클에 저장
    with open(pickle_file, "wb") as fw:
        pickle.dump(value , fw)

        

class Rental_Screen(QMainWindow):                                   # 나중에 상속받은 정보로 대여할때 유저정보이용해서 대여 파일 대입
    def __init__(self, ui_file, main_page_callback=None):
        super().__init__()
        
        folder = os.path.dirname(pickle_book_file)                                              # 상위폴더만 추출
        if not os.path.exists(folder):                                                           # 상위폴더가 없으면 
            os.makedirs(folder)                                                                 # 폴더 경로 전체 생성
                                                                
        if not os.path.exists(pickle_book_file):                                          # 피클 파일 없으면 경고창 + 강제종료 
            QMessageBox.critical(self, "파일 없음", "피클 책 파일이 없습니다. (또는 폴더에 파일 없음)")
            exit(0)
        if not os.path.exists(pickle_rent_file):
            QMessageBox.critical(self, "파일 없음", "피클 대여 파일이 없습니다. (또는 폴더에 파일 없음)")
            exit(0)
        if not os.path.exists(pickle_user_file):
            QMessageBox.critical(self, "파일 없음", "피클 유저 파일이 없습니다. (또는 폴더에 파일 없음)")   
            exit(0)   
           
                                                                    # 피클 파일이 있으면 
        if not os.path.exists(json_book_file):                              # 제이슨 폴더,파일 없으면 생성
            json_write(pickle_book_file, json_book_file)
            
        if not os.path.exists(json_rent_file):                                                         
            json_write(pickle_rent_file, json_rent_file)
        
        
        if not os.path.exists(json_user_file):
            json_write(pickle_user_file, json_user_file)
        
        
        self.ui_file = ui_file
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(800, 600)
        self.setCentralWidget(ui_file)
        self.center_on_screen()
        self.main_page_callback = main_page_callback
        
        book_data = file_load(json_book_file)                                               # 제이슨 파일 로드 
        
        self.current_user = None                                                            # 처음에 로그인을 안하면 none값
        
                               
        
        
        ui_file.btn_close.clicked.connect(self.cancel)   # 취소 버튼 
        ui_file.rent_btn.clicked.connect(self.rent_btn)   # 대여 신청 버튼
        self.all_check_count = 0                                 # 한번클릭하면 전체 한번더 클릭하면 해제 (반복)
        ui_file.all_check.clicked.connect(self.all_check)
        
        max_row = len(book_data)                                   # 전체 행 개수
        max_col = 5                                                     # 체크박스로 +1칸
        ui_file.tableWidget.setRowCount(max_row) 
        ui_file.tableWidget.setColumnCount(max_col)
        ui_file.tableWidget.setHorizontalHeaderLabels(["", "도서제목", "작가", "출판사", "대여 상태"])  # 테이블 위젯 헤더 기능 
        
    def add_widget_data(self):
        book_data = file_load(json_book_file)
        row = 0 # 행만 늘어나게
        for i in book_data:   # 책 데이터  
            self.ui_file.tableWidget.setItem(row, 1, QTableWidgetItem(i["title"]))                # 인덱스 i로 호출하고 1열에 제목 고정 # 디자이너에서 테이블 읽기모드 변경 
            self.ui_file.tableWidget.setItem(row, 2, QTableWidgetItem(i["author"]))          # 인덱스 i로 호출하고 2열에 작가 고정
            self.ui_file.tableWidget.setItem(row, 3, QTableWidgetItem(i["publisher"]))             # 인덱스 i로 호출하고 3열에 출판사 고정
            if i["rent"] == 0:                                                                  # 파일의 값이 0이면 대여 가능 출력
                self.ui_file.tableWidget.setItem(row, 4, QTableWidgetItem("대여가능"))            # 숫자가 안나와서 문자열로 변경
            else:
                self.ui_file.tableWidget.setItem(row, 4, QTableWidgetItem("대여중"))
            checkbox = QTableWidgetItem()                                                    # 반복적으로 대입      
            checkbox.setCheckState(Qt.Unchecked)                                         # 테이블에 체크박스 추가 # 체크되지 않은 상태 
            self.ui_file.tableWidget.setItem(row, 0, checkbox)                                   # 체크 박스 생성
            row += 1                                                                    # 책 데이터 다 호출하기 위해 행 +1 증가  
        self.ui_file.tableWidget.itemDoubleClicked.connect(self.detail_widget)
        
    

    
    
    
    
    def center_on_screen(self):                                                          # 창 헤더 없에고 고정 하는 코드 
        screen = QApplication.primaryScreen().geometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    def cancel(self):                                                                       # 취소 함수
        if self.main_page_callback is not None:
            self.main_page_callback()
    
    def all_check(self):
        
        if self.all_check_count == 0:
            for row in range(self.ui_file.tableWidget.rowCount()):      # 테이블 전체 행
                checkbox = QTableWidgetItem()
                checkbox.setCheckState(Qt.Checked)
                self.ui_file.tableWidget.setItem(row, 0, checkbox)   # 체크된 상태로 바꿔라           
            self.all_check_count += 1
        
        else:
            for row in range(self.ui_file.tableWidget.rowCount()):      # 테이블 전체 행
                checkbox = QTableWidgetItem()
                checkbox.setCheckState(Qt.Unchecked)                # 체크 해제 
                self.ui_file.tableWidget.setItem(row, 0, checkbox)   # 체크해제 상태로 바꿔라           
            self.all_check_count = 0
                
    
    def detail_widget(self, item):                                   # 아이템을 이용해 조건문으로 제목을 클릭했을때
        if item.column() == 1:                              # 1번을 클릭 (제목) # (item 테이블 위젯 아이템을  클릭한 행을 불러오는) 
            book_data = file_load(json_book_file)
            row = item.row()                           # 클릭한 행 불러오기
            title = book_data[row]["title"]                 # 클릭한 행을 통해 책 파일 목록에서 목록별로 추출
            author = book_data[row]["author"]
            info = book_data[row]["contents"]
            publi = book_data[row]["publisher"]
            loader = QUiLoader()
            ui_file = QFile("./ui_file/detail.ui")
            detail_ui = loader.load(ui_file)                    # 경로 불러오기
            
            
            detail_ui.title_text.setText(title)             # 내용 쓰기
            detail_ui.author_text.setText(author)
            detail_ui.info_text.setText(info)
            detail_ui.publi_text.setText(publi)
            
            
            detail_ui.cancel_btn.clicked.connect(self.detail_close)     # 확인 버튼 누르면 슬롯호출
                
            self.detail_ui = detail_ui                      # 셀프로 메인윈도우로 이용 불러오기 
            self.detail_ui.show()                           # 그걸 띄워라 
    
    
    
    def detail_close(self):
        self.detail_ui.close()                      # 현재 세부내용 창을 꺼라 
    
    
    def rent_btn(self):
        normal_max_rent = 6
        great_max_rent = 10
        vip_max_rent = 15
        total_rent = 0
        
        json_write(pickle_user_file, json_user_file)
        rent_data = file_load(json_rent_file)                                               # 대여한 파일 불러오기 
        book_data = file_load(json_book_file)                                                   # 값을 진짜 대여상태로 바꾸기 위해 책 파일 로드
        user_data = file_load(json_user_file)
        
        
        user_id = self.current_user["user_id"]   # 로그인 한
        user_grade = self.current_user["grade"]   # 회원 등급 ("n", "g", "v" 등)
        user_role = self.current_user["role"] 
        
        for row in range(len(user_data)):
            if user_id == user_data[row]["user_id"]:        # 로그인한 아이디와 유저파일 전체에서 유저파일을 찾으면 열이 같다면
                user_id_row = row                                  # 로그인 열 대입  # 피클 파일에만 있어서 로드 해야함
        
        
        
        
        
        for row in range(self.ui_file.tableWidget.rowCount()):                                         # 테이블에 모든 행을 숫자라서 레인지 사용 반복문
            if self.ui_file.tableWidget.item(row, 0).checkState() == Qt.Checked:                                        # 테이블위젯의 아이템 반복문 열 0(체크박스) 가 체크되어있으면
                dict_rent = {"book_id": book_data[row]["book_id"],                                  # 체크된 열을 통해 리스트 안에 딕셔너리 생성(책id,유저아이디,대여한 시간)               
                "user_id" : user_data[user_id_row]["user_id"],                            
                "date_start" : str(datetime.datetime.now().date()),                                        # 현재시각 문자열로 대입 .dete() 날짜만 
                "date_end": str(datetime.datetime.now().date() + datetime.timedelta(days=7))}               # 현재시각 + 7일 추가 (1주일)  실행한 시점에서 더하기                    
                
                for i in rent_data:                                                                     # 중복검사 반복문
                    if dict_rent["book_id"] == i["book_id"]:                                         # 대여파일에 대여한 책이랑 체크한 책이 같으면 (중복)   
                        QMessageBox.information(self, "대여 정보" ,"이미 대여중인 책입니다")
                        return     
                
                rent_data.append(dict_rent)                                                             # 대여 파일 어펜드 뒤에추가되서 원본 데이터랑 안겹침 #일단 위치옮기니깐 원하는대로 됌
                book_data[row]["rent"] = 1                                                         # 체크한 부분의 열의 대여를 대여중으로
                book_data[row]["rent_cnt"] += 1
                rent_count = 0 
                for i in rent_data:
                    if user_id == i["user_id"]:                                           # 사용자 아이디랑 대여한 파일의 아이디랑 같을때만 
                        rent_count += 1
                        if user_grade == "n":                                                                     # 테스트 로그인 아이디가 일반등급이면                                                          
                            if rent_count > normal_max_rent:                                                        # 대여 횟수가 6회 초과면
                                QMessageBox.information(self, "대여 정보", f"해당 등급:{user_grade}은 최대 대여횟수 {normal_max_rent}회 입니다! \n 다시 체크해주세요...")
                                return 
                        
                        if user_grade == "g":
                            if rent_count > great_max_rent:                                                             # 대여횟수 10회 초과면
                                QMessageBox.information(self, "대여 정보", f"해당 등급:{user_grade}은 최대 대여횟수 {great_max_rent}회 입니다! \n 다시 체크해주세요...")
                                return
                        
                        if user_grade == "v":
                            if rent_count > vip_max_rent:
                                QMessageBox.information(self, "대여 정보", f"해당 등급:{user_grade}은 최대 대여횟수 {vip_max_rent}회 입니다! \n 다시 체크해주세요...")
                                return
                                
                total_rent += 1                                     # 반복할수록 책 권수 증가
                
        
        
        if total_rent == 0:                                                                                                    # 아무것도 입력안하면 메세지후 종료(체크를 안해서 반복문에 안들어가면)
            QMessageBox.information(self, "대여 정보", "대여한 책이 없습니다...")
            return
        
        QMessageBox.information(self, "대여 정보", f"총 대여한 책 {total_rent}권 입니다. ")                     # 메세지박스로 데이터 값 출력
        file_save(rent_data, json_rent_file)                                                                 # 대여한 파일 저장                         
        file_save(book_data, json_book_file)                                                               # 대여상태로 저장  
        pickle_save(rent_data, pickle_rent_file)                                                                    # 피클 파일에도 저장
        pickle_save(book_data, pickle_book_file)
        
        row = 0 # 행만 늘어나게
        for i in book_data:    
            if i["rent"] == 0:                                                                  # 파일의 값이 0이면 대여 가능 출력
                self.ui_file.tableWidget.setItem(row, 4, QTableWidgetItem("대여가능"))            # 숫자가 안나와서 문자열로 변경
            else:
                self.ui_file.tableWidget.setItem(row, 4, QTableWidgetItem("대여중"))
            row += 1    
        return
            

    
    
    
    
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)                  # 처음 대여 신청 스크린 띄우는 코드 
    loader = QUiLoader()
    ui_file = QFile("./ui_data/lib.ui")                     # ui 파일 경로
    window = loader.load(ui_file)                           # ui파일 불러오기
    window.close()
    screen = Rental_Screen(window)                              # 클래스 인자에 ui파일
    screen.show()
    app.exec()