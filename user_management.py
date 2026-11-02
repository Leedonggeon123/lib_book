import sys
import os
import pickle
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QDialog, QTableWidget, QMessageBox, QTableView, QGridLayout, QLabel, QTableWidgetItem
from PySide6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QColor, QIcon, QPixmap
from PySide6.QtCore import QRegularExpression, Qt, QFile
from ui_data.ui_user_mgmt_page import Ui_Form
from PySide6.QtUiTools import QUiLoader

# 파일 경로 문제를 해결하기 위한 함수 (수정됨)
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # 현재 main.py 파일이 있는 폴더 위치를 기준으로 경로 설정
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path) 

class RegisterDialog(QDialog):
    def __init__(self, ui_path, user:str = None, parent=None):
        super().__init__(parent)
        self.is_id_checked = False

        loader = QUiLoader()
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly):
            raise IOError(f"Cannot open {ui_path}: {ui_file.errorString()}")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        os.makedirs(data_dir, exist_ok=True) # makedirs는 중간에 없는 폴더도 생성, exist_ok는 폴더가 이미 존재할 때 exist_ok가 False면 OS에러가 나고 True면 예외가 발생하지 않음.
        self.file_path = os.path.join(data_dir, "user.pkl")
        self.user_info_list = self.load_pickle() # 회원 목록 불러오기
        
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.ui.setWindowFlags(Qt.Widget)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)
        self.resize(self.ui.size())        
        self.ui.gb_grade.show()
        # 이메일 선택 추가
        self.ui.combo_email_domain.addItems(["never.com", "googol.com", "user.com"])

        # register.ui 안의 위젯은 self.ui.xxx 로 접근
        self.ui.btn_check_id.clicked.connect(self.check_id_duplicate)
        self.ui.btn_submit.clicked.connect(self.process_register)
        self.ui.btn_cancel.clicked.connect(self.reject)


    def get_user_data(self):
        """다이얼로그가 accept 된 후 입력값을 딕셔너리로 반환"""
        gender = "m" if self.ui.radio_male.isChecked() else "f"
        role = "l" if self.ui.rbt_lib.isChecked() else "u"
        grade = "v" if self.ui.rbt_lib.isChecked() else "n"
        email = f"{self.ui.input_email_prefix.text()}@{self.ui.combo_email_domain.currentText()}"
        return {
            "user_id": self.ui.input_id.text(),
            "pwd" : self.ui.input_pw.text(),
            "name" : self.ui.input_name.text(),
            "grade" : grade,  # input_role은 readOnly로 "일반" 고정이므로
            "private_num" : self.ui.input_rrn1.text() + str("-") + self.ui.input_rrn2.text(),
            "tel" : "010-" + self.ui.input_phone.text()[:4]+str("-")+self.ui.input_phone.text()[4:],
            "role" : role,
            "gender" : gender,
            "email" : email,
        }
    
    def on_id_changed(self):
        """아이디 수정 시 중복검사 상태 초기화"""
        self.is_id_checked = False
    
    def file_check(self): # 파일이 있는지 확인 없으면 생성
        """파일이 있는지 확인 없으면 생성
        """
        if not os.path.exists(self.file_path):
            self.user_info_list = []
            self.save_pickle()
    
    def save_pickle(self): # 파일 쓰기 피클
        """회원 정보 피클 저장
        """
        with open(self.file_path, "wb") as fw:
            file = pickle.dumps(self.user_info_list)
            fw.write(file)

    def load_pickle(self): # 파일 로드 피클
        """회원 정보 피클 불러오기

        Returns:
            list: 정보 목록
        """
        with open(self.file_path, "rb") as fr:
            file = fr.read()
            return pickle.loads(file)

    def check_id_duplicate(self):
        """아이디 중복 검사 기능"""
        if not hasattr(self.ui, 'input_id'):
            return

        user_id = self.ui.input_id.text().strip()

        if not user_id:
            QMessageBox.warning(self, "경고", "아이디를 입력해주세요.")
            return

        # 영문 및 숫자 조합 체크 (한글, 공백 방지)
        if not user_id.isalnum():
            QMessageBox.warning(self, "경고", "아이디는 한글/공백 없이 영문과 숫자만 사용 가능합니다.")
            return
        
        for id in self.user_info_list:
            if user_id == id["user_id"]:
                QMessageBox.warning(self, "확인", "이미 있는 아이디입니다.")
                return
        
        # TODO: 실제 파일이나 DB 조회 로직 작성 위치
        self.is_id_checked = True
        QMessageBox.information(self, "확인", "사용 가능한 아이디입니다.")
        self.user_id = self.ui.input_id.text() # 회원가입 버튼 눌렀을 때 가져오는 것 보다 사용가능 확인 했을 때 가져오는게 중복 검사 누르고 아이디 바꾼다음 가입하는 것 방지할 수 있을 것 같아.

    def process_register(self):
        """회원가입 버튼 클릭 시 유효성 검사 및 처리"""
        # 1) 아이디 중복검사 확인
        if not self.is_id_checked:
            QMessageBox.warning(self, "경고", "아이디 중복검사를 진행해주세요.")
            return

        # 2) 비밀번호 검증 (최소 8자리 이상 & 비밀번호 확인 일치)
        pw = self.ui.input_pw.text() if hasattr(self.ui, 'input_pw') else ""
        pw_confirm = self.ui.input_pw_confirm.text() if hasattr(self.ui, 'input_pw_confirm') else ""

        if len(pw) < 8:
            QMessageBox.warning(self, "경고", "비밀번호는 최소 8자리 이상이어야 합니다.")
            return

        if pw != pw_confirm:
            QMessageBox.warning(self, "경고", "비밀번호가 일치하지 않습니다.")
            return

        # 3) 주민번호 검증 (뒷자리 첫글자로 성별 자동 체크)
        if hasattr(self.ui, 'input_rrn2'):
            rrn2 = self.ui.input_rrn2.text().strip()
            if rrn2 and rrn2[0] in ['1', '3']:
                if hasattr(self.ui, 'radio_male'):
                    self.ui.radio_male.setChecked(True)
            elif rrn2 and rrn2[0] in ['2', '4']:
                if hasattr(self.ui, 'radio_female'):
                    self.ui.radio_female.setChecked(True)
            else:
                QMessageBox.warning(self, "경고", "주민등록번호 뒷자리(성별 번호)가 올바르지 않습니다.")
                return

        # 4) 전화번호 '-' 입력 여부 체크
        if hasattr(self.ui, 'input_phone'):
            phone = self.ui.input_phone.text()
            if '-' in phone:
                QMessageBox.warning(self, "경고", "전화번호에 '-'를 제외하고 숫자만 입력해주세요.")
                return

        # 회원가입 성공 처리
        if self.ui.btn_submit.text() == "회원 수정":
            QMessageBox.information(self, "성공", "회원 정보가 수정되었습니다.")
        else : 
            QMessageBox.information(self, "성공", "회원 정보가 추가되었습니다.")
        self.success_register()
        
    def success_register(self):
        self.accept()

class UserEditPage(QWidget, Ui_Form):
    def __init__(self, main_page_callback=None, func_page_callback=None):
        super().__init__()
        self.setupUi(self)
        self.selectFlag = False
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_dir, "data")
        os.makedirs(data_dir, exist_ok=True) # makedirs는 중간에 없는 폴더도 생성, exist_ok는 폴더가 이미 존재할 때 exist_ok가 False면 OS에러가 나고 True면 예외가 발생하지 않음.
        self.file_path = os.path.join(data_dir, "user.pkl")
        self.file_check() # 파일 확인
        self.user_info_list = self.load_pickle() # 회원 목록 불러오기
        
        self.main_page_callback = main_page_callback
        self.func_page_callback = func_page_callback
        
        self.user_list_tableWidget.cellClicked.connect(self.checkSelectWidget)
        self.add_user_pushButton.clicked.connect(self.show_add_page)
        self.edit_user_pushButton.clicked.connect(self.show_edit_page)
        self.del_user_pushButton.clicked.connect(self.show_del_page)
        self.cnacel_pushButton.clicked.connect(self.show_main_page)
        self.add_widget_data(self.user_info_list)
        
    def add_widget_data(self, users_data): # QTableWidget에 데이터 추가, 매개변수 추가 이유: 검색한 결과 받아야 해서.
        """QTableWidget에 데이터 추가
        """
        row = 0
        for row_data in users_data:
            
            if (row_data["user_id"] == "admin"):
                continue
            
            user_id = QTableWidgetItem(row_data["user_id"]) # book_id에 QTableWidgetItem
            user_id.setData(Qt.ItemDataRole.UserRole, row_data) # 내가 원하는 정보 QTableWidgetItem 객체에 저장. 그리고 book_id는 row, 0에 저장
            if (row_data["grade"] == "v"):
                grade_data = "VIP"
            elif (row_data["grade"] == "g"):
                grade_data = "우수"
            elif (row_data["grade"] == "n"):
                grade_data = "일반"
                
            if row_data["role"] == "l":
                role_data = "사서"
            elif row_data["role"] == "u":
                role_data = "사용자"
                
            grade = QTableWidgetItem(grade_data)
            role = QTableWidgetItem(role_data)
            name_ = row_data["name"]
            name = name_[0] + "**"
            name = QTableWidgetItem(name)
            tel = QTableWidgetItem(row_data["tel"])
            email = QTableWidgetItem(row_data["email"])
            
            self.user_list_tableWidget.insertRow(row)
            self.user_list_tableWidget.setItem(row, 0, user_id)
            # self.user_list_tableWidget.setItem(row, 1, grade)
            self.user_list_tableWidget.setItem(row, 1, role)
            self.user_list_tableWidget.setItem(row, 2, name)
            self.user_list_tableWidget.setItem(row, 3, tel)
            self.user_list_tableWidget.setItem(row, 4, email)
            row += 1
        self.user_list_tableWidget.setRowCount(row) # 행을 만들어 줘야 보여.
        self.selectFlag = False
    
    def checkSelectWidget(self):
        self.selectFlag = True
    
    # 페이지 이동 메서드
    def show_main_page(self):
        """메인 화면으로 이동
        """
        if self.main_page_callback is not None:
            self.main_page_callback()
        
    def show_add_page(self):
        """기능 화면으로 이동
        """
        ui_path = get_resource_path("./ui_data/register.ui")
        dialog = RegisterDialog(ui_path, self)
        dialog.setWindowTitle("회원 추가")   
        dialog.ui.btn_submit.setText("회원 추가")
        
        if (dialog.exec()):
            new_user = dialog.get_user_data()
            self.user_info_list.append(new_user)
            self.save_pickle()
            
            # 테이블 갱신
            self.user_list_tableWidget.setRowCount(0)
            self.add_widget_data(self.user_info_list)
    
    def refresh_table(self):
        self.user_list_tableWidget.setRowCount(0)
        self.user_info_list = self.load_pickle()
        self.add_widget_data(self.user_info_list)
    
    def show_edit_page(self):
        """기능 화면으로 이동
        """
        if (self.selectFlag):
            self.currnum = self.user_list_tableWidget.currentRow() + 1
            self.user_data = self.user_info_list[self.currnum]
                            
            ui_path = get_resource_path("./ui_data/register.ui")
            dialog = RegisterDialog(ui_path, self.user_data, self)
            
            dialog.setWindowTitle("회원 수정")   
            dialog.ui.btn_submit.setText("회원 수정")
            dialog.is_id_checked = True
            dialog.ui.input_id.setText(self.user_data["user_id"])
            dialog.ui.input_id.setEnabled(False)
            dialog.ui.input_pw.setText(self.user_data["pwd"])
            dialog.ui.input_pw_confirm.setText(self.user_data["pwd"])
            dialog.ui.input_name.setText(self.user_data["name"])
            dialog.ui.input_name.setEnabled(False)
            if self.user_data["role"] == "l":
                dialog.ui.rbt_lib.setChecked(True)
            elif self.user_data["role"] == "u":
                dialog.ui.rbt_user.setChecked(True)
            rrn1 = 0
            rrn2 = 0
            rrn1 = self.user_data["private_num"].split("-")[0]
            rrn2 = self.user_data["private_num"].split("-")[1]
            dialog.ui.input_rrn1.setText(rrn1)
            dialog.ui.input_rrn2.setText(rrn2)
            dialog.ui.input_rrn1.setEnabled(False)
            dialog.ui.input_rrn2.setEnabled(False)
            tel_num = self.user_data["tel"].split("-")
            tel_mid = str(tel_num[1])
            tel_tail = str(tel_num[2])
            dialog.ui.input_phone.setText(tel_mid + tel_tail)
            if self.user_data["gender"] == "m":
                dialog.ui.radio_male.setChecked(True)
            else :
                dialog.ui.radio_female.setChecked(True)
            dialog.ui.input_email_prefix.setText(self.user_data["email"].split("@")[0])
                            
            if (dialog.exec()):
                updt_user = dialog.get_user_data()
                self.updtUserData(updt_user)
                self.selectFlag = False

        else : 
            QMessageBox.warning(self, "경고", "회원을 선택해 주세요")
            return
    
    def updtUserData(self, userData:dict):
        for data in self.user_info_list:
            if data["user_id"] == userData["user_id"]:
                data["tel"] = "010-" + userData["tel"][4:8] + "-" + userData["tel"][9:]
                data["gender"] = userData["gender"]
                data["email"] = userData["email"]
                data["grade"] = userData["grade"]
                data["role"] = userData["role"]
                data["pwd"] = userData["pwd"]
        self.save_pickle()
        
        # 테이블 갱신
        self.user_list_tableWidget.setRowCount(0)
        self.add_widget_data(self.user_info_list)
                
    def show_del_page(self):
        """기능 화면으로 이동
        """
        if (self.selectFlag):
            self.currnum = self.user_list_tableWidget.currentRow() + 1
            self.user_data = self.user_info_list[self.currnum]
            
            msgbox = QMessageBox.warning(self, "경고", f"{self.user_data["user_id"]} 회원을 삭제하시겠습니까?", QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            
            if (msgbox == QMessageBox.Ok):
                for idx, data in enumerate(self.user_info_list):
                    if data["user_id"] == self.user_data["user_id"]:
                        del self.user_info_list[idx]
                print("delete data")
                
                self.save_pickle()
        
                # 테이블 갱신
                self.user_list_tableWidget.setRowCount(0)
                self.add_widget_data(self.user_info_list)
            else:
                print("cancel")
            
        else : 
            QMessageBox.warning(self, "경고", "회원을 선택해 주세요")
            return
        
    def file_check(self): # 파일이 있는지 확인 없으면 생성
        """파일이 있는지 확인 없으면 생성
        """
        if not os.path.exists(self.file_path):
            self.user_info_list = []
            self.save_pickle()
    
    def save_pickle(self): # 파일 쓰기 피클
        """ 정보 피클 저장
        """
        with open(self.file_path, "wb") as fw:
            file = pickle.dumps(self.user_info_list)
            fw.write(file)
    
    def load_pickle(self): # 파일 로드 피클
        """ 정보 피클 불러오기

        Returns:
            list: 도서 정보 목록
        """
        with open(self.file_path, "rb") as fr:
            file = fr.read()
            return pickle.loads(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserEditPage()
    window.show()
    sys.exit(app.exec())
