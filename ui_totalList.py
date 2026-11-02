import sys
import os
import pickle
from collections import OrderedDict
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QTableWidget, QMessageBox, QPushButton, QLabel, QTableWidgetItem, QHeaderView, QAbstractItemView
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

# Data Class
class RentDataTree:
    def __init__(self):
        self.data = OrderedDict()
    # Qtablewidget에 뿌릴 데이터 user_id 기반의 북데이터
    def add_rent(self, user_id:str, book_id:str, title:str, dt_start:str, dt_end:str, status: int = 0):
        self.data.setdefault(user_id, []).append({
            "book_id" : book_id,
            "title" : title,
            "dt_start" : dt_start,
            "dt_end" : dt_end,
            "status" : status
        })
    # user_id 기반의 북데이터를 Return 기능 + 다음 작업 진행
    def iter_flat(self):
        """아이디 기준으로 묶인 순서 그대로 (user_id, book_dict) 튜플을 반환"""
        for user_id, books in self.data.items():
            for book in books:
                yield user_id, book
    # Qtablewidget의 데이터가 텍스트로 실제 데이터는 bool 값으로 바꾸기 위함    
    def update_status(self, user_id: str, book_title: str, new_status: str):
        for book in self.data.get(user_id, []):
            if book["title"] == book_title :
                book["status"] = 1 if new_status == "대여중" else 0
                return True
        return False
# 화면 클래스
class RentListPage(QWidget):
    COL_USER_ID = 0
    COL_TITLE = 1
    COL_STATUS = 2
    COL_DT_START = 3
    COL_DT_END = 4
    
    rent_list = []
    book_list = []
    
    def __init__(self, main_page_callback=None):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "../data")
        self.file_rent = os.path.join(data_dir, "rent.pkl")
        self.file_book = os.path.join(data_dir, "book.pkl")
        self.main_page_callback = main_page_callback
        self.book_tree = self.make_data()
        self._search_keyword = ""
        
        main_layout = QVBoxLayout(self)

        # 타이틀
        title_label = QLabel("전체 회원 도서 목록")
        title_label.setFont(QFont("", 14, QFont.Bold))
        main_layout.addWidget(title_label)

        # 찾기        
        find_layout = QHBoxLayout()
        find_layout.addStretch()
        
        self.find_label = QLabel("도서 찾기")
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("도서명 입력")
        self.find_btn = QPushButton("찾기")
        self.find_btn_clear = QPushButton("초기화")
        self.find_btn.clicked.connect(self.bookSearch)
        self.find_btn_clear.clicked.connect(self.bookSearchClear)
        
        find_layout.addWidget(self.find_label, stretch=1)
        find_layout.addWidget(self.find_edit, stretch=7)
        find_layout.addWidget(self.find_btn, stretch=1)
        find_layout.addWidget(self.find_btn_clear, stretch=1)
        main_layout.addLayout(find_layout)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["아이디", "도서 제목", "대여 상태","대여일", "반납일"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        main_layout.addWidget(self.table)

        # 하단 버튼 영역
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.btn_return = QPushButton("도서 반납")
        self.btn_return.setCursor(Qt.PointingHandCursor)
        self.btn_return.setStyleSheet("""
            QPushButton {
                background-color: #5a4633; color: white;
                border: none; padding: 8px 16px; border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #8a6b4a; }
        """)
        self.btn_main = QPushButton("돌아가기")
        bottom_layout.addWidget(self.btn_return)
        bottom_layout.addWidget(self.btn_main)
        self.btn_return.clicked.connect(self.return_book)
        self.btn_main.clicked.connect(self.comebackMain)

        main_layout.addLayout(bottom_layout)
        self.refresh_table()
    def refresh_data(self):
        self.book_tree = self.make_data()
        self.refresh_table()
    # 메인 돌아가기
    def comebackMain(self):
        if self.main_page_callback is not None:
            self.main_page_callback()
    # 찾기 영역의 도서명 기반 찾기
    def bookSearch(self):
        keyword = self.find_edit.text()
        self._search_keyword = keyword
        self.refresh_table()
        
        if keyword.strip() and self.table.rowCount() == 0:
            QMessageBox.information(self, "검색 결과 없음", f"'{keyword}' 와 일치하는 도서 없습니다.")
    # 찾기 영역의 초기화
    def bookSearchClear(self):
        self.find_edit.clear()
        self._search_keyword = ""
        self.refresh_table()
    # Qtablewidget 화면 다시 출력    
    def refresh_table(self):
        all_rows = list(self.book_tree.iter_flat())
        
        keyword = self._search_keyword.strip()
        if keyword:
            rows = [
                (user_id, book) for user_id, book in all_rows
                if keyword in book["title"].lower()
            ]
        else:
            rows = all_rows
        
        self.table.clearSpans()
        self.table.setRowCount(len(rows))

        # 아이디별 시작 행, 개수 계산 (병합용)
        span_info = {}  # user_id -> (start_row, count)
        for row_idx, (user_id, book) in enumerate(rows):
            if user_id not in span_info:
                span_info[user_id] = [row_idx, 0]
            span_info[user_id][1] += 1

        for row_idx, (user_id, book) in enumerate(rows):
            id_item = QTableWidgetItem(user_id)
            id_item.setTextAlignment(Qt.AlignCenter)
            title_item = QTableWidgetItem(book["title"])
            status = book["status"]
            if status :
                status_item = QTableWidgetItem("대여중")
            else :
                status_item = QTableWidgetItem("대여 가능")
            status_item.setTextAlignment(Qt.AlignCenter)
            dt_start_item = QTableWidgetItem(book["dt_start"])
            dt_end_item = QTableWidgetItem(book["dt_end"])

            # 대여 상태에 따라 색상 표시
            if status:
                status_item.setForeground(Qt.red)
            else:
                status_item.setForeground(Qt.darkGreen)

            self.table.setItem(row_idx, self.COL_USER_ID, id_item)
            self.table.setItem(row_idx, self.COL_TITLE, title_item)
            self.table.setItem(row_idx, self.COL_STATUS, status_item)
            self.table.setItem(row_idx, self.COL_DT_START, dt_start_item)
            self.table.setItem(row_idx, self.COL_DT_END, dt_end_item)

        # 같은 아이디 셀 병합
        for user_id, (start_row, count) in span_info.items():
            if count > 1:
                self.table.setSpan(start_row, self.COL_USER_ID, count, 1)
    # 화면에서 사용할 데이터 생성
    def make_data(self):
        data_tree = RentDataTree()
        
        self.rent_list = self.load_rent()
        self.book_list = self.load_book()
        
        book_lookup = {b["book_id"] : b  for b in self.book_list}
        
        for rent in self.rent_list:
            book = book_lookup.get(rent["book_id"])
            if  book is not None:
                title = book["title"]
                status = book.get("rent")
            else :
                title = "알수없음"
                status = 0
            data_tree.add_rent(
                user_id = rent["user_id"],
                book_id = rent["book_id"],
                title = title,
                dt_start = rent.get("date_start", ""),
                dt_end = rent.get("date_end", ""),
                status = status,
            )
        return data_tree
    # 데이터 처리 후 book 관련 데이터 저장    
    def save_book_pickle(self): # 파일 쓰기 피클
        """도서 정보 피클 저장
        """
        with open(self.file_book, "wb") as fw:
            file = pickle.dumps(self.book_list)
            fw.write(file)
    # 데이터 처리 후 rent 관련 데이터 저장
    def save_rent_pickle(self): # 파일 쓰기 피클
        """도서 정보 피클 저장
        """
        with open(self.file_rent, "wb") as fw:
            file = pickle.dumps(self.rent_list)
            fw.write(file)
    # 렌트 관련 데이터를 파일에서 수집
    def load_rent(self): # rent 파일 로드 피클
        """피클 불러오기

        Returns:
            list: 목록
        """
        with open(self.file_rent, "rb") as fr:
            file = fr.read()
            return pickle.loads(file)
    # 도서 관련 데이터를 파일에서 수집
    def load_book(self): # rent 파일 로드 피클
        """피클 불러오기

        Returns:
            list: 목록
        """
        with open(self.file_book, "rb") as fr:
            file = fr.read()
            return pickle.loads(file)        
    # 도서 반납시 데이터 처리
    def return_book(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "알림", "반납할 도서를 선택해주세요.")
            return

        row = selected_rows[0].row()

        # 병합된 셀에서는 QTableWidgetItem이 병합 시작 행에만 존재하므로 보정
        userId = self.user_id_for_row(row)
        bookTitle = self.table.item(row, self.COL_TITLE).text()
        current_status = self.table.item(row, self.COL_STATUS).text()
        bookId = ""

        datas = list(self.book_tree.iter_flat())
        for (user_id, book_data) in datas:
            if user_id == userId and book_data["title"] == bookTitle:
                bookId = book_data["book_id"]

        if current_status == "대여 가능":
            QMessageBox.information(self, "알림", "이미 반납된 도서입니다.")
            return

        new_status = "대여 가능"
        success = self.book_tree.update_status(userId, bookTitle, new_status)

        if success:
            QMessageBox.information(self, "완료", f"'{bookTitle}' 도서가 반납 처리되었습니다.")
            self.dataUpdate()
            self.dataDelete(userId, bookId)
            self.book_tree = self.make_data()
            self.refresh_table()
        else:
            QMessageBox.critical(self, "오류", "반납 처리에 실패했습니다.")
    # User_id 병합으로 인해 아이디 컬럼이 없는 행이 있을 수 있어 행의위로 올라가며 값을 찾음
    def user_id_for_row(self, row: int):
        for r in range(row, -1, -1):
            item = self.table.item(r, self.COL_USER_ID)
            if item is not None and item.text():
                return item.text()
        return ""
    # rent data 삭제
    def dataDelete(self, user_id : str, book_id : str):
        for idx, rent in enumerate(self.rent_list):
            if rent["user_id"] == user_id and rent["book_id"] == book_id:
                del self.rent_list[idx]
                    
        self.save_rent_pickle()
    
    # 렌트, 북의 수정된 데이터를 확인해 파일 저장
    def dataUpdate(self):
        datas = list(self.book_tree.iter_flat())
        for book in self.book_list:
            for idx, (user_id, book_data) in enumerate(datas):
                if book_data["book_id"] == book["book_id"]:
                    book["rent"] = book_data["status"]
                    
        self.save_book_pickle()
        self.rent_list = self.load_rent()
        self.book_list = self.load_book()