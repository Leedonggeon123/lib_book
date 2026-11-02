import sys
import json
import os
import pickle                                                                                               # 바이너리 형태로 암호화 하기 위해 사용
import datetime                                                                                         # 책을 대여한 시점 시간을 구하기 위해 사용
from PySide6.QtWidgets import QApplication,QMainWindow,QTableWidgetItem, QMessageBox, QInputDialog
from PySide6.QtCore import Qt, QFile
from PySide6.QtUiTools import QUiLoader


json_book_file = "./data/book.json" 
json_rent_file = "./data/rent.json"
json_user_file = "./data/user.json"

pickle_book_file = "./data/book.pkl"
pickle_rent_file = "./data/rent.pkl"
pickle_user_file = "./data/user.pkl"

def file_load(file):                                                                        # 파일 로드 
    with open(file, "r", encoding="utf-8") as fr:
        return json.load(fr)


def file_save(value, file):                                                                 # 파일 값 저장
    with open(file, "w", encoding="utf-8") as fw:
        json.dump(value, fw, ensure_ascii=False, indent=4)

def json_write(pickle_file, json_file):                                                  # 피클파일 제이슨 파일로 변환  처음 인자에 피클 파일 경로 두번째 인자에 josn파일 경로                                                   
    with open(pickle_file, "rb") as fr:                                                     # 피클파일 로드 
        pickle_data = pickle.load(fr)                                                       
        
    with open(json_file, "w", encoding="utf-8") as fw:
        json.dump(pickle_data, fw, ensure_ascii=False, indent=4)          
    
def pickle_save(value, pickle_file):                                                                    # 최종적으로 정보 피클에 저장
    with open(pickle_file, "wb") as fw:
        pickle.dump(value , fw)

def load_pickle(file_path): # 파일 로드 피클
    """도서 정보 피클 불러오기

    Returns:
        list: 도서 정보 목록
    """
    with open(file_path, "rb") as fr:
        file = fr.read()
        return pickle.loads(file)


class Confirm_Scrren(QMainWindow):                                           # 대여 확인 화면 (대여된 파일 보여주는) 
    def __init__(self, ui_file, main_page_callback=None):
        super().__init__()
        
        self.ui_file = ui_file
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(800, 600)
        self.setCentralWidget(ui_file)
        self.center_on_screen()
         

        self.main_page_callback = main_page_callback
        
        self.current_user = None
            
        ui_file.rent_over_btn.clicked.connect(self.rent_over_btn)               # 대여 연장 함수 호출  # 관리자 일시 버튼 가리기
        ui_file.btn_close.clicked.connect(self.cancel)
        ui_file.rent_give_btn.clicked.connect(self.book_return)
        self.all_check_count = 0                                                # 전체선택 한번시 전체선택 한번더 클릭시 전체해제
        ui_file.all_check_btn.clicked.connect(self.all_check)
                                                           # 로그인 정보 함수 호출


    def main_table(self): 
        book_data = file_load(json_book_file)
        rent_data = load_pickle(pickle_rent_file)
        
        
        user_id = self.current_user["user_id"]                                                                    # 아이디 정보를 받아 로직 처리        
        
        max_row = 0                                                                   
        for i in rent_data:                                                         # 대여 파일 안에 로그인한 유저 대여 전체 파일 횟수 찾기
            if user_id == i["user_id"]:
                max_row += 1
                                            
        max_col = 6                  
        self.ui_file.tableWidget.setRowCount(max_row)
        self.ui_file.tableWidget.setColumnCount(max_col)
        self.ui_file.tableWidget.setHorizontalHeaderLabels(["", "도서제목", "대여시작", "반납기간", "대여 상태", "북아이디"])
        
        row = 0                                                         # 행만 늘어나게
        for rent in rent_data:                                              # 대여 한 파일
            if user_id == rent["user_id"]:                          # 로그인한 아이디만
                for book in book_data:
                    if rent["book_id"] == book["book_id"]:          # 대여한 책과 북파일의 책이 같으면
                        self.ui_file.tableWidget.setItem(row, 1, QTableWidgetItem(book["title"]))
                        self.ui_file.tableWidget.setItem(row, 2, QTableWidgetItem(rent["date_start"]))
                        self.ui_file.tableWidget.setItem(row, 3, QTableWidgetItem(rent["date_end"]))
                        self.ui_file.tableWidget.setItem(row, 4, QTableWidgetItem("대여중"))
                        self.ui_file.tableWidget.setItem(row, 5, QTableWidgetItem(book["book_id"]))        
                        checkbox = QTableWidgetItem()
                        checkbox.setCheckState(Qt.Unchecked)
                        self.ui_file.tableWidget.setItem(row, 0, checkbox)
                        row += 1
        self.ui_file.tableWidget.setColumnHidden(5,True)                                                 # 북아이디 가리기 
                   
        

    
        

    
    
    def center_on_screen(self):                                                          # 창 헤더 없에고 고정 하는 코드 
        screen = QApplication.primaryScreen().geometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)

    
    def cancel(self):
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
        
    
    
    
    def rent_over_logic(self, value):                                                                       # 대여 연장 로직
        rent_data = file_load(json_rent_file)                                               # 대여한 파일 불러오기       
        user_data = file_load(json_user_file)
        
        normal_max = 7
        great_max = 14
        vip_max = 28
        
        user_id = self.current_user["user_id"]   # 로그인 한
        user_grade = self.current_user["grade"]   # 회원 등급 ("n", "g", "v" 등)
        user_role = self.current_user["role"] 
        
        
           
        for row in range(self.ui_file.tableWidget.rowCount()):                                                  # 대여파일 테이블 전체 행 계산
            if self.ui_file.tableWidget.item(row, 0).checkState() == Qt.Checked:                                # 대여파일 테이블에서 체크를 했다면
                book_id = self.ui_file.tableWidget.item(row, 5).text()                                          # 체크한 열의 책 아이디 받기
                for rent in rent_data:                                                                          # 대여파일 전체 반복문
                    if user_id == rent["user_id"]:                                                         # 대여파일전체에서 로그인한 유저 파일만 
                        if rent["book_id"] == book_id:                                                           # 체크한 책아이디와 대여한 책아이디가 같으면 (체크한것만)
                            if value == 0:                                                                      # 0을 입력하면 함수 종료
                                QMessageBox.information(self, "대여 연장", "연장 일수를 입력해주세요...")
                                return 
                            
                            if user_role == "l":                                                                        # 사서 직책일때
                                current_end_date = datetime.datetime.strptime(rent["date_end"], "%Y-%m-%d").date()             # 체크한 파일 현재시각 변수 대입   # 기존 파일에 반납일자를 데이트 타임으로 변경후 대입 시간제외 (.date())                                                                                      # 연장 날짜      
                                new_end_date = current_end_date + datetime.timedelta(days=value)                                        # 기존 파일 에서 연장한 날 만큼 더하기  
                                rent["date_end"] = str(new_end_date)                                                               # 문자 형태로 연장 날짜 대입     # 사서라서 바로 대입                                                                                              # 파일 전체에서 대여파일 하나 찾았다? 종료 다시 반복문
                                file_save(rent_data, json_rent_file)                                                        # 데이터 저장
                                pickle_save(rent_data, pickle_rent_file)
                                self.ui_file.tableWidget.setItem(row, 3, QTableWidgetItem(rent["date_end"]))                # 세이브 하면 테이블 위젯에 다시 보이게
                            
                            elif user_role == "u":                                                                      # 유저일때          # 이부분 공부하기
                                if user_grade == "n":                                                               # 로그인한 아이디가 일반등급일때                                                       # 생성자 변수에 대여일수 누적  
                                    start_date = datetime.datetime.strptime(rent["date_start"], "%Y-%m-%d").date()          # 대여 시작날짜   
                                    original_end = start_date + datetime.timedelta(days=7)                                  # 기본반납날짜 (end파일은 변경되어서 이게 기준) 유저입력과 비교하기 위해 사용
                                    current_end_date = datetime.datetime.strptime(rent["date_end"], "%Y-%m-%d").date()      #  불러온 파일을 통해 얼마나 연장했는지 확인                                                                                     # 연장 날짜      
                                    new_end_date = current_end_date + datetime.timedelta(days=value)                          # 새로운 연장날짜 기존파일 + 유저입력날짜 
                                    total_extension = (new_end_date - original_end).days                                    # 총 연장날짜   새로운연장날짜 - 기본반납날짜  = 기존파일 일수에서 유저입력값만 추가되는 
                                                                                                                                                                                                    
                                    if total_extension > normal_max:                                                         # 총 연장날짜가 7일 초과하면 
                                        QMessageBox.information(self, "대여 연장", f"해당 등급: {self.test_id_grade} 최대 연장 {normal_max}일 초과했습니다...")
                                        return
                                
                                    else:
                                        rent["date_end"] = str(new_end_date)                                            # 새로운 날짜 저장
                                        file_save(rent_data, json_rent_file)
                                        pickle_save(rent_data, pickle_rent_file)
                                        self.ui_file.tableWidget.setItem(row, 3, QTableWidgetItem(rent["date_end"]))  # 세이브 하면 테이블 위젯에 다시 보이게
                                
                                if user_grade == "g":
                                    start_date = datetime.datetime.strptime(rent["date_start"], "%Y-%m-%d").date()       # 대여한 날짜 
                                    original_end = start_date + datetime.timedelta(days=7)                               # 대여한 날짜 + 7일(기본 연장날짜)
                                    current_end_date = datetime.datetime.strptime(rent["date_end"], "%Y-%m-%d").date()     #  불러온 파일의 연장날짜 (최소 대여 시작 + 7일 이상) over_now_time                                                                                     # 연장 날짜      
                                    new_end_date = current_end_date + datetime.timedelta(days=value)                          # 불러온 파일의 날짜 + 유저 입력값 over_time   
                                    total_extension = (new_end_date - original_end).days                                                     

                            
                                    if total_extension > great_max:
                                        QMessageBox.information(self, "대여 연장", f"해당 등급: {self.test_id_grade} 최대 연장 {great_max}일 초과했습니다...")
                                        return
                                    
                                    else:
                                        rent["date_end"] = str(new_end_date)                               # 현재 반납날자 파일에 유저 입력날짜 더하기 
                                        file_save(rent_data, json_rent_file)
                                        pickle_save(rent_data, pickle_rent_file)
                                        self.ui_file.tableWidget.setItem(row, 3, QTableWidgetItem(rent["date_end"]))
                                    
                                if user_grade == "v":
                                    start_date = datetime.datetime.strptime(rent["date_start"], "%Y-%m-%d").date()       # 대여한 날짜 
                                    original_end = start_date + datetime.timedelta(days=7)                               # 대여한 날짜 + 7일(기본 연장날짜)
                                    current_end_date = datetime.datetime.strptime(rent["date_end"], "%Y-%m-%d").date()     #  불러온 파일의 연장날짜 (최소 대여 시작 + 7일 이상) over_now_time                                                                                     # 연장 날짜      
                                    new_end_date = current_end_date + datetime.timedelta(days=value)                          # 불러온 파일의 날짜 + 유저 입력값 over_time   
                                    total_extension = (new_end_date - original_end).days    
                                    
                                    if total_extension > vip_max:
                                        QMessageBox.information(self, "대여 연장", f"해당 등급: {self.test_id_grade} 최대 연장 {vip_max}일 초과했습니다...")
                                        return
                                    
                                    else:
                                        rent["date_end"] = str(new_end_date)                               # 현재 반납날자 파일에 유저 입력날짜 더하기 
                                        file_save(rent_data, json_rent_file)
                                        pickle_save(rent_data, pickle_rent_file)
                                        self.ui_file.tableWidget.setItem(row, 3, QTableWidgetItem(rent["date_end"]))
                                        
        return                      
    
    
    
    
    def rent_over_btn(self):
        rent_data = file_load(json_rent_file)  
        book_data = file_load(json_book_file)
        
        user_id = self.current_user["user_id"]   # 로그인 한 아아디
        
        
        check_count = 0
        for row in range(self.ui_file.tableWidget.rowCount()):                                                  # 대여파일 테이블 전체 행 계산
            if self.ui_file.tableWidget.item(row, 0).checkState() == Qt.Checked:                                # 대여파일 테이블에서 체크를 했다면
                check_count = 1                                                                                 # 체크를 했다면                        
                book_id = self.ui_file.tableWidget.item(row, 5).text()                                          # 체크한 북아이디 정보 
                for rent in rent_data:                                                                          # 내 아이디 대여파일 부분 확인                                                                                          
                    if user_id == rent["user_id"]:                                                     # 로그인한 아이디랑 대여파일 유저 아이디랑 같으면 (내아이디만)
                        if rent["book_id"] == book_id:                                                  # 체크한 북아이디와 대여파일의 북아이디가 같으면                                      
                            for book in book_data:
                                if book["book_id"] == book_id:                                          # 북파일 전체에서 아이디가 내가 체크한 아이디와 같으면
                                    if book["rent"] == 0:                                                   # 그 북 아이디의 대여상태가 0이면                                                      
                                        QMessageBox.information(self, "대여 연장", "이미 반납완료된 책입니다.")
                                        return
        
        
        if check_count == 0:
            QMessageBox.information(self, "대여 연장", "연장할 책이 없습니다. 체크표시를 해주세요.")
            return
            
        
        value, ok = QInputDialog.getInt(self, "대여 연장", "연장 일수 입력", 0, 0, 100)  # 0(시작시 입력숫자) 0(최소 숫자) 100(최대숫자)                # ok(확인 버튼 관한거)
        if ok:
            self.rent_over_logic(value)        # 연장 로직호출 

    
    def book_return(self):
        rent_data = file_load(json_rent_file)                                               # 대여한 파일 불러오기 
        book_data = file_load(json_book_file)                                                   # 값을 진짜 대여상태로 바꾸기 위해 책 파일 로드
        user_data = file_load(json_user_file)
        remove_rents = []
   
        user_id = self.current_user["user_id"]   # 로그인 한
        
        for row in range(len(user_data)):
            if user_id == user_data[row]["user_id"]:        # 로그인한 아이디와 유저파일 전체에서 유저파일을 찾으면 열이 같다면
                user_id_row = row                                  # 로그인 열 대입  # 피클 파일에만 있어서 로드 해야함


        check_status = 0 
        for row in range(self.ui_file.tableWidget.rowCount()):             # 테이블 행 전체 개수                                     # 대여파일 테이블 전체 행 계산
            if self.ui_file.tableWidget.item(row, 0).checkState() == Qt.Checked:        # 체크박스를 체크한부분만
                
                book_id = self.ui_file.tableWidget.item(row, 5).text()      # 책 아이디 
                for rent in rent_data:
                    if user_id == rent["user_id"]:                      # 대여파일 아이디와 로그인아이디 같다면
                        if rent["book_id"] == book_id:                  # 대여파일 책 아이디와 체크한 북아이디 정보가 같다면    
                            for book in book_data:
                                if book["book_id"] == book_id:          # 북파일의 책id 가 체크한 book id가 같다면
                                    book["rent"] = 0                        # 북대여 0으로 변경 
                                    remove_rents.append(rent)                 # 체크한 데이터만 삭제
        
                check_status = 1                                        # 체크가 되면 1로 변경
                          
        if check_status == 0:                                                # 체크 안했으면
            QMessageBox.information(self, "도서 반납", "반납할 책이 없습니다....    체크표시를 해주세요.")
            return                
        
        
        for rent in remove_rents:               # 선택한거 지우기
            rent_data.remove(rent)
        file_save(book_data, json_book_file)
        file_save(rent_data, json_rent_file)        # 파일 지우기
        pickle_save(book_data, pickle_book_file)            # 피클파일 저장
        pickle_save(rent_data, pickle_rent_file)
        self.main_table()                               # 메인테이블 호출 테이블 최신화
      
        
                                      
                          

if __name__ == "__main__":
    app = QApplication(sys.argv)                  # 처음 랜달 스크린 띄우는 코드 
    loader = QUiLoader()
    ui_file = QFile("./ui_data/confirm.ui")                     # ui 파일 경로
    window = loader.load(ui_file)                           # ui파일 불러오기
    window.close()
    screen = Confirm_Scrren(window)                              # 클래스 인자에 ui파일
    screen.show()
    app.exec()