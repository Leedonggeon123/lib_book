import sys
import os
import pickle
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, QDialog, QTableWidget, QMessageBox, QTableView, QGridLayout, QLabel, QTableWidgetItem
from PySide6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QColor, QIcon, QPixmap
from PySide6.QtCore import QRegularExpression, Qt
from ui_data.ui_book_mgmt_combined import Ui_Form
# 도서 코드는 특정 책 코드. 그러니 갱신 X. 실제 도서 분류에는 코드가 따로 있는데 이러면 특정 코드에 추가할 수 있게 해야해. 지금은 넘어가. 다음에 유지보수 할 때 추가해봐.
# 나중에 전체 도서 개수 구하는 코드 만들어 보기 len().

# 메인 화면 만들고 stackedwidget만들고 이거 추가해 보기.

class BookInfoManagement(QWidget, Ui_Form):
    def __init__(self, return_main_page=None):
        super().__init__()
        self.setupUi(self)

        self.function_btn_name = ("도서 추가", "도서 수정", "도서 삭제")
        self.function_message = ("추가 하시겠습니까?", "수정 하시겠습니까?", "삭제 하시겠습니까?")
        self.hidden_book_data = None
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        os.makedirs(data_dir, exist_ok=True) # makedirs는 중간에 없는 폴더도 생성, exist_ok는 폴더가 이미 존재할 때 exist_ok가 False면 OS에러가 나고 True면 예외가 발생하지 않음.
        self.file_path = os.path.join(data_dir, "book.pkl")
        self.file_check() # 파일 확인
        self.book_info_list = self.load_pickle() # 도서 목록 불러오기
        
        self.add_widget_data(self.book_info_list) # QTableWidget에 데이터 추가
        self.return_main_page = return_main_page
        
        self.help_label.setStyleSheet("color: black; font-weight: bold;")
        self.help_label.setToolTip("코드: 도서코드\n제목: 도서제목\n작가: 작가\n출판사: 출판사\n내용: 내용\n각 구역에서만 검색 가능\n없으면 코드, 제목, 작가, 출판사에서 검색")
        self.help_label.setCursor(Qt.PointingHandCursor)
        self.book_list_tablewidget.itemSelectionChanged.connect(self.return_data) # 셀 클릭하면 그 항목 반환.
        self.book_list_tablewidget.itemDoubleClicked.connect(self.view_book_data) # 셀 더블클릭하면 책 정보 보여주기.
        
        # 도서 관리 화면 버튼
        self.book_info_cancel_btn.clicked.connect(self.main_page) # 메인화면으로
        self.add_book_btn.clicked.connect(lambda _checked: self.open_book_function_page(0)) # 도서 추가 버튼
        self.edit_book_btn.clicked.connect(lambda _checked: self.open_book_function_page(1)) # 도서 수정 버튼
        self.del_book_btn.clicked.connect(lambda _checked: self.open_book_function_page(2)) # 도서 삭제 버튼
        
        self.edit_book_page_cancel_btn.clicked.connect(self.book_management_page) # 도서 정보에서 취소 버튼
        
        # self.book_list_tablewidget.setStyleSheet("font-size: 16px;") # 글꼴 크기
        self.status_comboBox.addItems(["대여 가능", "대여 중"])
        self.search_lineEdit.returnPressed.connect(self.search_book) # 엔터 누르면 검색
        
        self.function_btn.clicked.connect(self.clicked_function_btn) # 기능 수행 버튼
    
    def view_book_data(self): # 도서 정보 확인.
        """셀 더블 클릭하면 정보 확인 기능
        """
        current_row = self.book_list_tablewidget.currentRow() # 현재 행 가져오기.
        target_data = self.book_list_tablewidget.item(current_row, 0) # 현재 행의 0번 열에 저장된 데이터 가져오기. 여기에는 book_id랑 도서 전체 정보 딕셔너리 데이터가 있어.
        if target_data is not None:
            hidden_book_data = target_data.data(Qt.ItemDataRole.UserRole) # target_data에 저장 된 UserRole 데이터를 가져와.
        self.title_lineEdit.setReadOnly(True)
        self.author_lineEdit.setReadOnly(True)
        self.publisher_lineEdit.setReadOnly(True)
        self.contents_textEdit.setReadOnly(True)
        self.status_comboBox.setEnabled(False)
        self.count_spinBox.setReadOnly(True)
        self.title_lineEdit.setText(hidden_book_data["title"])
        self.author_lineEdit.setText(hidden_book_data["author"])
        self.contents_textEdit.setText(hidden_book_data["contents"])
        self.publisher_lineEdit.setText(hidden_book_data["publisher"])
        rent = self.hidden_book_data["rent"]
        rent_cnt = self.hidden_book_data["rent_cnt"]
        if rent == 0:
            self.status_comboBox.setCurrentText("대여 가능")
        else:
            self.status_comboBox.setCurrentText("대여 중")
        self.count_spinBox.setValue(rent_cnt)
        self.function_btn.hide()
        self.edit_book_page_cancel_btn.setText("확인")
        self.stackedWidget.setCurrentWidget(self.edit_book_page)
        
    def return_data(self):
        """셀 클릭하면 클릭한 도서 정보 가져오는 기능

        Args:
            book_data (QTableWidgetItem): QTableWidgetItem 객체
        """
        current_row = self.book_list_tablewidget.currentRow() # 현재 행 가져오기.
        target_data = self.book_list_tablewidget.item(current_row, 0)
        # current_row = book_data.row() # QTableWidgetItem 객체의 행을 가져와. 그 행의 0번 열에 있는 데이터를 가져와야해서.
        # target_data = self.book_list_tablewidget.item(current_row, 0) # 어떤 열을 클릭했든 0번 열에 있는 setData로 저장한 값을 가져와야해서. QTableWidget의 현재 행 첫 번째 열에 저장 된 QTableWidgetItem 객체를 target_data에 넣어. QTableWidgetItem 객체에는 내가 저장한 book_id랑 setData로 저장한 row_data가 있어.
        if target_data is not None:
            self.hidden_book_data = target_data.data(Qt.ItemDataRole.UserRole) # target_data에 저장 된 UserRole 데이터를 가져와.
    
    def clicked_function_btn(self): # 수행 할 기능 경고 메시지
        """수행 할 기능 경고 메시지
        """
        # 스페이스바만 누르고 입력하는 것 방지.
        title = self.title_lineEdit.text().replace(" ", "")
        contents = self.contents_textEdit.toPlainText().replace(" ", "")
        author = self.author_lineEdit.text().replace(" ", "")
        publisher = self.publisher_lineEdit.text().replace(" ", "") # 스페이스바 만 입력하고 추가하는 거 방지.
        if self.function_arg == 0 or self.function_arg == 1:
            if not (title and contents and author and publisher): # 이거는 추가, 수정 일 때만.
                QMessageBox.information(self, "확인", "모든 항목을 채워주세요.")
                return
        answer = QMessageBox.question(self, "확인", self.function_message[self.function_arg])
        
        if answer == QMessageBox.StandardButton.Yes:
            self.perform_function()
            self.book_management_page()
        elif self.function_arg == 2: # 수정, 추가는 다시 수정하고 싶을 수도 있으니 뺌.
            self.book_management_page()
    
    def perform_function(self): # 기능 수행
        """기능 수행
        """
        if self.function_arg == 0: # 도서 추가
            title = self.title_lineEdit.text()
            author = self.author_lineEdit.text()
            publisher = self.publisher_lineEdit.text()
            contents = self.contents_textEdit.toPlainText()
            book_id = self.max_book_id() # int
            self.book_info_list.append(
                {"book_id" : f"B{book_id + 1:04d}", "title" : title, "contents" : contents, "author" : author, "publisher" : publisher, "rent" : 0, "rent_cnt" : 0}
                )
            self.save_pickle()
            self.add_widget_data(self.book_info_list)
        if self.function_arg == 1: # 도서 수정
            book_id = self.hidden_book_data["book_id"]
            title = self.title_lineEdit.text()
            author = self.author_lineEdit.text()
            publisher = self.publisher_lineEdit.text()
            contents = self.contents_textEdit.toPlainText()
            rent = self.status_comboBox.currentIndex()
            rent_cnt = int(self.count_spinBox.text())
            for idx, book_data in enumerate(self.book_info_list):
                if book_data["book_id"] == book_id:
                    self.book_info_list[idx] = {"book_id" : book_id, "title" : title, "contents" : contents, "author" : author, "publisher" : publisher, "rent" : rent, "rent_cnt" : rent_cnt}
            self.save_pickle()
            self.add_widget_data(self.book_info_list)
        if self.function_arg == 2: # 도서 삭제
            book_id = self.hidden_book_data["book_id"]
            for idx, book_data in enumerate(self.book_info_list):
                if book_data["book_id"] == book_id:
                    self.book_info_list.pop(idx)
            self.save_pickle()
            self.add_widget_data(self.book_info_list)
    # [{'book_id': 'B0001', 'title': '머리카락이 자라면 : 김현례 책', 'contents': '삐뚤...껴보길 바란다.', 'author': '김현례', 'publisher': '웅진주니어 : 웅진씽크빅', 'rent': 0, 'rent_cnt': 0}
    
    def max_book_id(self) -> int: # 제일 큰 도서 코드 찾는 기능
        """제일 큰 도서 코드 찾는 기능

        Returns:
            int: 최대 도서 코드 반환
        """
        if not self.book_info_list: # 도서가 하나도 없으면 0
            return 0
        
        book_id_values = []
        for idx in self.book_info_list:
            remove_b_num = idx["book_id"].lstrip("B")
            int_remove_b_num = int(remove_b_num)
            book_id_values.append(int_remove_b_num) # int가 추가 됨
        max_book_id_ = max(book_id_values) # int
        return max_book_id_ # int
    
    def refresh_book_list(self):
        self.book_info_list = self.load_pickle()
        self.add_widget_data(self.book_info_list)
    
    def add_widget_data(self, books_data): # QTableWidget에 데이터 추가, 매개변수 추가 이유: 검색한 결과 받아야 해서.
        """QTableWidget에 데이터 추가
        """
        self.book_list_tablewidget.setRowCount(len(books_data)) # 행을 만들어 줘야 보여.
        for row, row_data in enumerate(books_data):
            book_id = QTableWidgetItem(row_data["book_id"]) # book_id에 QTableWidgetItem
            book_id.setData(Qt.ItemDataRole.UserRole, row_data) # 내가 원하는 정보 QTableWidgetItem 객체에 저장. 그리고 book_id는 row, 0에 저장
            title = QTableWidgetItem(row_data["title"])
            author = QTableWidgetItem(row_data["author"])
            publisher = QTableWidgetItem(row_data["publisher"])
            contents = QTableWidgetItem(row_data["contents"])
            if row_data["rent"] == 0:
                rent = QTableWidgetItem("대여 가능")
            else:
                rent = QTableWidgetItem("대여 중")
            rent_cnt = QTableWidgetItem(str(row_data["rent_cnt"]))
            
            row_items = (book_id, title, author, publisher, rent, rent_cnt, contents)
            for col, data in enumerate(row_items):
                self.book_list_tablewidget.setItem(row, col, data)
    
    def search_book(self): # 도서 검색하면 그 도서만 찾아주는 기능
        """도서 검색하면 찾아주는 기능
        """
        item_list = []
        text = self.search_lineEdit.text().strip() # 양쪽 끝 삭제, 찾고 싶은 내용
        search_dict = {"코드:" : "book_id", "제목:" : "title", "작가:" : "author", "출판사:" : "publisher", "내용:" : "contents"}
        search_key = None
        
        for prefix, key in search_dict.items(): # 키워드 찾기.
            if text.startswith(prefix):
                keyword = text[len(prefix):].strip() 
                search_key = key
        
        if search_key is not None: # 키워드가 있으면
            for item in self.book_info_list:
                if keyword in item[search_key]:
                    item_list.append(item)
        
        else: # 키워드가 없으면
            for item in self.book_info_list:
                if text in item["book_id"]:
                    item_list.append(item)
                elif text in item["title"]:
                    item_list.append(item)
                elif text in item["author"]:
                    item_list.append(item)
                elif text in item["publisher"]:
                    item_list.append(item)
        self.add_widget_data(item_list)
        
    
    def main_page(self): # 나중에 메인화면이 생기면 그때 이동할 수 있게끔 수정해야해.
        """메인 화면으로
        """
        if self.return_main_page is not None:
            self.return_main_page()
            self.search_lineEdit.clear()
    
    def clicked_book_manage_btn(self): # 여기도 main_page랑 마찬가지로 나중에 수정해야해. 메인 화면에서 도서 관리 화면으로
        """메인 화면에서 도서 관리 화면으로
        """
        self.stackedWidget.setCurrentWidget(self.book_info_main_page)
    
    def open_book_function_page(self, arg): # 각 기능의 화면으로 전환
        """각 기능의 화면으로 전환

        Args:
            arg (int): 0:추가 1:수정 2:삭제
        """
        self.function_arg = arg
        if self.function_arg == 1 or self.function_arg == 2:
            if self.hidden_book_data is None:
                QMessageBox.information(self, "확인", "하나의 도서를 선택해주세요.")
                return
            self.title_lineEdit.setText(self.hidden_book_data["title"])
            self.author_lineEdit.setText(self.hidden_book_data["author"])
            self.contents_textEdit.setText(self.hidden_book_data["contents"])
            self.publisher_lineEdit.setText(self.hidden_book_data["publisher"])
            rent = self.hidden_book_data["rent"]
            rent_cnt = self.hidden_book_data["rent_cnt"]
            if rent == 0:
                self.status_comboBox.setCurrentText("대여 가능")
            else:
                self.status_comboBox.setCurrentText("대여 중")
            self.count_spinBox.setValue(rent_cnt)
        self.function_btn.setText(self.function_btn_name[arg])
        self.stackedWidget.setCurrentWidget(self.edit_book_page)
        self.status_comboBox.setEnabled(False)
        self.count_spinBox.setReadOnly(True)
        if arg == 2: # 도서 삭제면 편집 불가.
            self.title_lineEdit.setReadOnly(True)
            self.author_lineEdit.setReadOnly(True)
            self.publisher_lineEdit.setReadOnly(True)
            self.contents_textEdit.setReadOnly(True)
        self.search_lineEdit.clear()

    def book_management_page(self): # 도서 관리(추가,수정,삭제)화면에서 도서 관리 메인 화면으로
        """도서 관리(추가,수정,삭제)화면에서 도서 관리 메인 화면으로
        """
        self.stackedWidget.setCurrentWidget(self.book_info_main_page)
        self.title_lineEdit.setReadOnly(False)
        self.author_lineEdit.setReadOnly(False)
        self.publisher_lineEdit.setReadOnly(False)
        self.contents_textEdit.setReadOnly(False)
        self.status_comboBox.setEnabled(True)
        self.count_spinBox.setReadOnly(False)
        self.title_lineEdit.clear()
        self.author_lineEdit.clear()
        self.publisher_lineEdit.clear()
        self.contents_textEdit.clear()
        self.book_list_tablewidget.clearSelection()
        self.hidden_book_data = None
        self.function_btn.show() # 더블 클릭으로 도서 정보 확인한 다음에 다시 보여줘야해서.
        self.edit_book_page_cancel_btn.setText("취소") # 더블 클릭으로 도서 정보 확인한 다음에 다시 취소로 바꿔야해서.
    
    def file_check(self): # 파일이 있는지 확인 없으면 생성
        """파일이 있는지 확인 없으면 생성
        """
        if not os.path.exists(self.file_path):
            self.book_info_list = []
            self.save_pickle()
    
    def save_pickle(self): # 파일 쓰기 피클
        """도서 정보 피클 저장
        """
        with open(self.file_path, "wb") as fw:
            file = pickle.dumps(self.book_info_list)
            fw.write(file)
    
    def load_pickle(self): # 파일 로드 피클
        """도서 정보 피클 불러오기

        Returns:
            list: 도서 정보 목록
        """
        with open(self.file_path, "rb") as fr:
            file = fr.read()
            return pickle.loads(file)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookInfoManagement()
    window.show()
    sys.exit(app.exec())