import os
import sys
import pickle
from PySide6.QtCore import QFile, Qt, QRegularExpression
from PySide6.QtGui import QPixmap, QRegularExpressionValidator, QFont, QFontDatabase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QMainWindow, QMessageBox, QButtonGroup

# 파일 경로 문제를 해결하기 위한 함수 (수정됨)
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # 현재 main.py 파일이 있는 폴더 위치를 기준으로 경로 설정
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# 2. 회원가입 화면 클래스
class RegisterWindow(QMainWindow):

    def __init__(self, login_page_callback=None, main_page_callback=None):
        super().__init__()
        # self.login_window = login_window
        self.login_page_callback = login_page_callback
        self.main_page_callback = main_page_callback
        self.is_id_checked = False  # 아이디 중복검사 체크 플래그

        loader = QUiLoader()
        ui_path = get_resource_path("./ui_data/register.ui")
        ui_file = QFile(ui_path)
        
        if ui_file.open(QFile.ReadOnly):
            self.ui = loader.load(ui_file)
            ui_file.close()

            if self.ui:
                self.setCentralWidget(self.ui)
                self.setWindowTitle("회원가입")
                self.resize(self.ui.size())
                
                current_dir = os.path.dirname(os.path.abspath(__file__))
                data_dir = os.path.join(current_dir, "data")
                os.makedirs(data_dir, exist_ok=True) # makedirs는 중간에 없는 폴더도 생성, exist_ok는 폴더가 이미 존재할 때 exist_ok가 False면 OS에러가 나고 True면 예외가 발생하지 않음.
                self.file_path = os.path.join(data_dir, "user.pkl")
                self.file_check() # 파일 확인
                self.user_info_list = self.load_pickle() # 회원 목록 불러오기
                
                # 이메일 선택 추가
                self.ui.combo_email_domain.addItems(["never.com", "googol.com", "user.com"])
                idx = self.ui.combo_email_domain.currentIndex()
                self.email_suffix = self.ui.combo_email_domain.itemText(idx)
                
                # 성별 선택 확인
                self.gender_group = QButtonGroup(self.ui)
                self.gender_group.addButton(self.ui.radio_male)
                self.gender_group.addButton(self.ui.radio_female)

                
                # 아아디 패턴
                id_regex = QRegularExpression(r"^[A-Za-z0-9]{15}$")
                self.ui.input_id.setValidator(QRegularExpressionValidator(id_regex))
                # 이름 입력 한글만
                name_regex = QRegularExpression(r"^([가-힣]{2,4})$")
                self.ui.input_name.setValidator(QRegularExpressionValidator(name_regex))
                # 핸드폰 번호 숫자만
                tel_regex = QRegularExpression(r"^([0-9]{8})$")
                self.ui.input_phone.setValidator(QRegularExpressionValidator(tel_regex))
                # 주민 번호 숫자만 입력 하게.
                rrn1_regex = QRegularExpression(r"^([0-9]{6})$")
                rrn2_regex = QRegularExpression(r"^([0-9]{7})$")
                self.ui.input_rrn1.setValidator(QRegularExpressionValidator(rrn1_regex))
                self.ui.input_rrn2.setValidator(QRegularExpressionValidator(rrn2_regex))
                # 이메일 아이디 패턴만 가능 하게
                email_regex = QRegularExpression(r"^[A-Za-z0-9]{20}$") # 다른 사이트는 더 길수도 있으니 20.
                self.ui.input_email_prefix.setValidator(QRegularExpressionValidator(email_regex))
                
                # --- 기본 설정 (요구사항) ---
                # 등급: "일반"으로 고정 및 수정 불가(ReadOnly)
                if hasattr(self.ui, 'input_role'):
                    self.ui.input_role.setText("일반")
                    self.ui.input_role.setReadOnly(True)
                    
                # 아이디: 최대 15자리 제한 및 입력 변경시 중복검사 초기화
                if hasattr(self.ui, 'input_id'):
                    self.ui.input_id.setMaxLength(15)
                    self.ui.input_id.textChanged.connect(self.on_id_changed)
                
                # 2) 취소 버튼 -> 로그인 창으로 돌아가기
                if hasattr(self.ui, 'btn_cancel'):
                    self.ui.btn_cancel.clicked.connect(self.back_to_login)

                # 3) 중복검사 버튼
                if hasattr(self.ui, 'btn_check_id'):
                    self.ui.btn_check_id.clicked.connect(self.check_id_duplicate)

                # 4) 회원가입 실행 버튼
                if hasattr(self.ui, 'btn_submit'):
                    self.ui.btn_submit.clicked.connect(self.process_register)
        else:
            print(f"UI 파일을 찾을 수 없습니다: {ui_path}")
        
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
            list: 도서 정보 목록
        """
        with open(self.file_path, "rb") as fr:
            file = fr.read()
            return pickle.loads(file)
    
    def on_id_changed(self):
        """아이디 수정 시 중복검사 상태 초기화"""
        self.is_id_checked = False
    
    def check_id_duplicate(self):
        """아이디 중복 검사 기능"""
        if self.current_page == 1: # 정보수정은 아이디 변경X
            self.is_id_checked = True
            return
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
        if self.current_page == 0 and not self.is_id_checked:
            QMessageBox.warning(self, "경고", "아이디 중복검사를 진행해주세요.")
            return

        # 2) 비밀번호 검증 (최소 8자리 이상 & 비밀번호 확인 일치)
        pw = self.ui.input_pw.text() if hasattr(self.ui, 'input_pw') else ""
        pw_confirm = self.ui.input_pw_confirm.text() if hasattr(self.ui, 'input_pw_confirm') else ""

        if len(pw) < 8: # 비밀번호 확인
            QMessageBox.warning(self, "경고", "비밀번호는 최소 8자리 이상이어야 합니다.")
            return

        if pw != pw_confirm: # 비밀번호 매치 확인
            QMessageBox.warning(self, "경고", "비밀번호가 일치하지 않습니다.")
            return
        
        if self.ui.input_name.text() == "": # 이름 확인
            QMessageBox.warning(self, "경고", "이름을 입력해주세요.")
            return
        if len(self.ui.input_name.text()) < 2: # 이름 자리수 확인
            QMessageBox.warning(self, "경고", "이름을 입력해주세요.")
            return
        
        # 주민번호 자리수 확인
        if len(self.ui.input_rrn1.text()) != 6: # 앞자리
            QMessageBox.warning(self, "경고", "주민등록번호 앞자리가 올바르지 않습니다.")
            return
        if len(self.ui.input_rrn2.text()) != 7: # 뒷자리
            QMessageBox.warning(self, "경고", "주민등록번호 뒷자리가 올바르지 않습니다.")
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
        
        # 회원가입 시 전화 번호 자리수 확인.
        if len(self.ui.input_phone.text()) != 8:
            QMessageBox.warning(self, "경고", "핸드폰 번호 자리수가 올바르지 않습니다.")
            return
        
        # 4) 전화번호 '-' 입력 여부 체크
        if hasattr(self.ui, 'input_phone'):
            phone = self.ui.input_phone.text()
            if '-' in phone:
                QMessageBox.warning(self, "경고", "전화번호에 '-'를 제외하고 숫자만 입력해주세요.")
                return
        # 이메일 아이디 검사
        if not self.ui.input_email_prefix.text().isalnum():
            QMessageBox.warning(self, "경고", "이메일 아이디를 다시 입력해주세요.")
            return
        if self.current_page == 0: # 회원가입 버튼으로 이동
            # 회원가입 성공 처리
            QMessageBox.information(self, "성공", "회원가입이 완료되었습니다.")
            self.success_register()
            self.reset_input()
        if self.current_page == 1: # 회원정보 버튼으로 이동
            QMessageBox.information(self, "성공", "정보가 변경되었습니다.")
            self.success_register()
            self.reset_input()
    
    def current_page_check(self, arg):
        self.current_page = arg
    
    def return_page(self):
        current_page = self.stackedWidget.currentWidget()
        self.stackedWidget.setCurrentWidget(current_page)
    
    def reset_input(self):
        """입력 정보 초기화
        """
        self.ui.input_id.clear()
        self.ui.input_pw.clear()
        self.ui.input_pw_confirm.clear()
        self.ui.input_name.clear()
        self.ui.input_rrn1.clear()
        self.ui.input_rrn2.clear()
        self.ui.input_phone.clear()
        self.ui.input_email_prefix.clear()
        self.is_id_checked = False
    
    def success_register(self):
        """회원가입 성공시 정보 저장
        """
        # 회원가입 시 필요한 정보. 아이디, 비밀번호, 이름, 등급, 주민번호, 전화번호, 성별, 이메일
        user_pw = self.ui.input_pw.text() # 비밀번호
        name = self.ui.input_name.text() # 이름
        private_num = self.ui.input_rrn1.text() + "-" + self.ui.input_rrn2.text() # 주민번호
        email_prefix = self.ui.input_email_prefix.text() # 이메일
        tel_mid = self.ui.input_phone.text()[:4]
        tel_tail = self.ui.input_phone.text()[4:]
        tel = "010-" + tel_mid + "-" + tel_tail # 전화번호
        selected_gender = self.gender_group.checkedButton() # 성별 체크 확인
        if selected_gender.text() == "남": # 성별
            gender = "m"
        else:
            gender = "f"
        if self.current_page == 1:
            user_id = self.current_user["user_id"]
            role = self.current_user["role"]
            grade = self.current_user["grade"]
            over_cnt = self.current_user["over_cnt"]
            email_suffix = self.ui.combo_email_domain.currentText()
            update_user = {"user_id" : user_id, "pwd" : user_pw, "name" : name, "private_num" : private_num, "tel" : tel, "gender" : gender, "email" : f"{email_prefix}@{email_suffix}", "role" : role, "grade" : grade, "over_cnt" : over_cnt}
            for idx, user_data in enumerate(self.user_info_list):
                if user_data["user_id"] == user_id:
                    self.user_info_list[idx] = update_user
                    self.save_pickle()
                    self.current_user.update(update_user)
                    self.back_to_login()
                    return
        new_user = {"user_id" : self.user_id, "pwd" : user_pw, "name" : name, "private_num" : private_num, "tel" : tel, "gender" : gender, "email" : f"{email_prefix}@{self.email_suffix}", "role" : "u", "grade" : "n", "over_cnt" : 0}
        self.user_info_list.append(new_user)
        self.save_pickle()
        self.back_to_login()
    
    def set_current_user(self, current_user): # 현재 회원
        """로그인 한 회원

        Args:
            current_user (dict): 회원 정보
        """
        self.current_user = current_user
    
    def back_to_login(self):
        """회원가입 창을 닫고 로그인 창을 다시 표시"""
        # self.close()
        # self.login_window.show()
        if self.current_page == 0:
            if self.login_page_callback is not None:
                self.login_page_callback()
        
        if self.current_page == 1:
            if self.main_page_callback is not None:
                self.main_page_callback()
            


# 3. 로그인 화면 클래스
class LoginWindow(QMainWindow):

    def __init__(self, register_page_callback=None, main_page_callback=None):
        super().__init__()

        loader = QUiLoader()
        ui_path = get_resource_path("./ui_data/login.ui")
        ui_file = QFile(ui_path)
        
        self.register_page_callback = register_page_callback
        self.main_page_callback = main_page_callback
        
        if ui_file.open(QFile.ReadOnly):
            self.ui = loader.load(ui_file)
            ui_file.close()

            if self.ui:
                self.setCentralWidget(self.ui)
                self.setWindowTitle("로그인")
                self.resize(self.ui.size())
                self.ui.btn_login.clicked.connect(self.success_login)
                font_id = QFontDatabase.addApplicationFont("fonts/hy얕은샘물m-yoond1004.ttf")
                if font_id != -1:
                    font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
                    my_font = QFont(font_name, 48)
                self.ui.label_title.setFont(my_font)
                current_dir = os.path.dirname(os.path.abspath(__file__))
                data_dir = os.path.join(current_dir, "data")
                os.makedirs(data_dir, exist_ok=True) # makedirs는 중간에 없는 폴더도 생성, exist_ok는 폴더가 이미 존재할 때 exist_ok가 False면 OS에러가 나고 True면 예외가 발생하지 않음.
                self.file_path = os.path.join(data_dir, "user.pkl")
                self.file_check() # 파일 확인
                self.user_info_list = self.load_pickle() # 회원 목록 불러오기
                
                # 로그인 창의 '회원가입' 버튼 이벤트 연결
                if hasattr(self.ui, 'btn_register'):
                    self.ui.btn_register.clicked.connect(self.show_register_page)
            
        else:
            print(f"UI 파일을 찾을 수 없습니다: {ui_path}")
    
    def success_login(self):
        self.user_info_list = self.load_pickle()
        for user in self.user_info_list:
            if self.ui.lineEdit_id.text() == user["user_id"]:
                if self.ui.lineEdit_pw.text() == user["pwd"]:
                    QMessageBox.information(self, "확인", "로그인 성공!")
                    self.user = user
                    self.show_main_page()
                    return  
        QMessageBox.information(self, "확인", "아이디, 비밀번호를 확인해주세요.")
    
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
            list: 도서 정보 목록
        """
        with open(self.file_path, "rb") as fr:
            file = fr.read()
            return pickle.loads(file)
    
    def show_main_page(self):
        """모든 기능이 있는 메인 화면으로 이동
        """
        if self.main_page_callback is not None:
            self.main_page_callback(self.user)
    
    def show_register_page(self):
        """회원가입 창으로 이동
        """
        if self.register_page_callback is not None:
            self.register_page_callback(0)
    
    def open_register(self):
        """로그인 창을 숨기고 회원가입 창을 새로 생성하여 출력"""
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()


# --- 실행 영역 (이 부분이 있어야 창이 뜹니다) ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
    