import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, QDialog, QTableWidget, QMessageBox, QTableView, QGridLayout, QLabel, QTableWidgetItem
from PySide6.QtGui import QRegularExpressionValidator, QStandardItemModel, QStandardItem, QColor, QIcon, QPixmap, QMovie, QFontDatabase, QFont
from PySide6.QtCore import QRegularExpression, Qt, QFile, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from ui_data.ui_main_menu import Ui_MainWindow
from PySide6.QtUiTools import QUiLoader
from book_management import BookInfoManagement
from lib_rental import Rental_Screen
from user_management import UserEditPage
from login_register_mainpage import LoginWindow, RegisterWindow, get_resource_path
from lib_confirm import Confirm_Scrren
from ui_data.ui_totalList import RentListPage

class LibMainWindow(QMainWindow, Ui_MainWindow):
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # main_page 내부에서 label_gif 위젯 찾기
        label_gif_widget = getattr(
            self, "main_page", self
        ).findChild(QLabel, "label_gif")

        if label_gif_widget:

            # 부모 위젯(main_page 또는 centralwidget) 크기 기준으로 중앙 위치(x, y) 계산
            parent_widget = label_gif_widget.parentWidget()
            if parent_widget:
                p_width = parent_widget.width()
                p_height = parent_widget.height()

                x = (p_width - label_gif_widget.width()) // 2
                y = (p_height - label_gif_widget.height()) // 2

                # 라벨 위치 이동
                label_gif_widget.move(x, y)
    
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # --- QLabel에 GIF 애니메이션 연결 ---
        # 1. QMovie 객체 생성
        self.movie = QMovie("ui_data/library_animation.gif")
        
        # 2. objectName이 "label_gif"인 QLabel 찾기
        label_gif_widget = self.findChild(QLabel, "label_gif")
        
        # 3. 라벨을 찾았으면 Movie 연결 후 재생
        if label_gif_widget:
            label_gif_widget.setMovie(self.movie)
            self.movie.start()
        else:
            print("Warning: label_gif를 찾을 수 없습니다.")
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.center_on_screen()
        # 배경 음악.
        self.bgm_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.bgm_player.setAudioOutput(self.audio_output)
        music_path = get_resource_path("sound/Remini.mp3")
        self.bgm_player.setSource(QUrl.fromLocalFile(music_path))
        self.audio_output.setVolume(0.2)
        self.bgm_player.setLoops(QMediaPlayer.Infinite)
        self.bgm_player.play()
        # 버튼 클릭 소리
        self.click_sound = QSoundEffect(self)
        sound_path = get_resource_path("sound/Click.wav")
        self.click_sound.setSource(QUrl.fromLocalFile(sound_path))
        self.click_sound.setVolume(0.5)
        
        loader = QUiLoader()
        lib_ui_file = QFile("./ui_data/lib.ui")
        confirm_ui_file = QFile("./ui_data/confirm.ui")
        if lib_ui_file.open(QFile.ReadOnly):
            lib_window = loader.load(lib_ui_file)
            lib_ui_file.close()
        if confirm_ui_file.open(QFile.ReadOnly):
            confirm_window = loader.load(confirm_ui_file)
            confirm_ui_file.close()
            
        self.login_page = LoginWindow(self.show_register_page, self.login_success)
        self.register_page = RegisterWindow(self.show_login_page, self.show_main_page)
        self.rental_screen = Rental_Screen(lib_window, self.show_main_page)
        self.confirm_screen= Confirm_Scrren(confirm_window, self.show_main_page)
        self.book_info_page = BookInfoManagement(self.show_main_page)
        self.user_edit_page = UserEditPage(self.show_main_page)
        self.rental_list_page = RentListPage(self.show_main_page)
        
        self.stackedWidget.addWidget(self.login_page)
        self.stackedWidget.addWidget(self.register_page)
        self.stackedWidget.addWidget(self.rental_screen)
        self.stackedWidget.addWidget(self.confirm_screen)
        self.stackedWidget.addWidget(self.book_info_page)
        self.stackedWidget.addWidget(self.user_edit_page)
        self.stackedWidget.addWidget(self.rental_list_page)
        
        self.btn_logout.clicked.connect(self.logout_check)
        # 소리 관련
        click_buttons = [
        self.btn_logout,
        self.btn_exit,
        self.btn_rent,
        self.btn_check_rent,
        self.btn_manage_book,
        self.btn_manage_user,
        
        self.login_page.ui.btn_login,
        self.login_page.ui.btn_register,
        
        self.register_page.ui.btn_cancel,
        self.register_page.ui.btn_check_id,
        self.register_page.ui.btn_submit,
        
        self.book_info_page.book_info_cancel_btn,
        self.book_info_page.add_book_btn,
        self.book_info_page.edit_book_btn,
        self.book_info_page.del_book_btn,
        
        self.user_edit_page.add_user_pushButton,
        self.user_edit_page.edit_user_pushButton,
        self.user_edit_page.del_user_pushButton,
        self.user_edit_page.cnacel_pushButton,
        
        self.rental_screen.ui_file.btn_close,
        self.rental_screen.ui_file.rent_btn,
        self.rental_screen.ui_file.all_check,
        
        self.confirm_screen.ui_file.rent_over_btn,
        self.confirm_screen.ui_file.btn_close,
        self.confirm_screen.ui_file.rent_give_btn,
        self.confirm_screen.ui_file.all_check_btn,
        
        self.rental_list_page.find_btn_clear,
        self.rental_list_page.find_btn,
        self.rental_list_page.btn_return,
        self.rental_list_page.btn_main
        ]
        for button in click_buttons:
            button.clicked.connect(self.play_click_sound)
        
        # 기능 관련
        self.lbl_user_icon.clicked.connect(lambda _checked: self.show_register_page(1))
        self.btn_exit.clicked.connect(self.close_program) # 프로그램 종료
        self.btn_rent.clicked.connect(self.show_rental_page) # 대여 화면
        self.btn_check_rent.clicked.connect(self.show_confirm_page) # 개인 대여 목록 화면
        self.btn_manage_book.clicked.connect(self.show_books_list_page) # 도서 관리 화면
        self.btn_manage_user.clicked.connect(self.show_user_list_page) # 회원 관리 화면
        self.btn_rent_list.clicked.connect(self.show_rental_list_page) # 대여 목록 화면
        self.show_login_page() # 프로그램 시작하면 바로 로그인 화면으로 이동
    
    def play_click_sound(self):
        self.click_sound.play()
    
    def logout_check(self):
        answer = QMessageBox.question(self, "확인", "로그아웃 하시겠습니까?")
        if answer == QMessageBox.StandardButton.No:
            return
        self.show_login_page()
    
    def login_success(self, user_data): # 로그인 성공 시
        self.current_user = user_data
        self.rental_screen.current_user = self.current_user                                 # 클래스 생성자 변수로 이용
        self.confirm_screen.current_user = self.current_user
        self.confirm_screen.main_table()
        if self.current_user["role"] == "a":
            self.lbl_user_icon.setText(f"[관리자]\n[ID: {self.current_user["user_id"]}]")
        elif self.current_user["role"] == "l":
            self.lbl_user_icon.setText(f"[등급: 사서]\n[ID: {self.current_user["user_id"]}]")
        else:
            if self.current_user["grade"] == "v":
                self.lbl_user_icon.setText(f"[등급: VIP]\n[ID: {self.current_user["user_id"]}]")
            elif self.current_user["grade"] == "g":
                self.lbl_user_icon.setText(f"[등급: 우수]\n[ID: {self.current_user["user_id"]}]")
            elif self.current_user["grade"] == "n":
                self.lbl_user_icon.setText(f"[등급: 일반]\n[ID: {self.current_user["user_id"]}]")
        self.apply_permission() # 권한 확인
        self.show_main_page() # 메인 화면으로
    
    def apply_permission(self):
        role = self.current_user["role"]
        if role == "a": # 관리자는 책 삭제 가능, 강제 반납 가능, 회원 관리, 대여 불가. 등급은 없고 관리자
            self.rental_screen.ui_file.rent_btn.hide() # 도서 목록 도서 대여 버튼 보이기
            self.confirm_screen.ui_file.rent_give_btn.hide() # 대여 목록 반납 버튼 보이기
            self.confirm_screen.ui_file.rent_over_btn.hide() # 대여 목록 연장 버튼 보이기
        elif role == "l": # 강제 반납 불가능, 책 추가, 수정 가능, 무조건 VIP, 연체 상관 없음. 등급은 사서. 대여 현황 파악. / 사서는 책 삭제 불가능 O
            self.btn_manage_user.hide() # 회원 관리 숨기기
            self.book_info_page.del_book_btn.hide()
            self.rental_list_page.btn_return.hide()
        elif role == "u": # 대여, 개인 대여 현황 확인.
            self.btn_manage_user.hide()
            self.btn_manage_book.hide()
            self.btn_rent_list.hide()
    
    def show_register_page(self, arg): # 0 회원가입 버튼, 1은 회원정보 확인 버튼
        """회원가입 화면으로 이동
        """
        if arg == 0:
            self.register_page.ui.btn_submit.setText("회원 가입")
            self.lbl_title.show()
            self.lbl_title.setText("회원가입📚")
            self.lbl_user_icon.hide()
            self.lbl_user_icon.hide()
            self.btn_logout.hide()
            self.btn_exit.show()
            
        if arg == 1:
            self.register_page.set_current_user(self.current_user)
            self.register_page.ui.btn_submit.setText("정보 변경")
            self.register_page.ui.input_id.setText(self.current_user["user_id"])
            self.register_page.ui.input_id.setReadOnly(True)
            self.register_page.ui.input_pw.setText(self.current_user["pwd"])
            self.register_page.ui.input_pw_confirm.setText(self.current_user["pwd"])
            self.register_page.ui.input_name.setText(self.current_user["name"])
            private_num = self.current_user["private_num"].split("-")
            self.register_page.ui.input_rrn1.setText(private_num[0])
            self.register_page.ui.input_rrn2.setText(private_num[1])
            tel = self.current_user["tel"].split("-")
            self.register_page.ui.input_phone.setText(tel[1] + tel[2])
            self.register_page.ui.gb_grade.hide()
            if self.current_user["gender"] == "m":
                self.register_page.ui.radio_male.setChecked(True)
            else:
                self.register_page.ui.radio_female.setChecked(True)
            email = self.current_user["email"].split("@")
            self.register_page.ui.input_email_prefix.setText(email[0])
            idx = self.register_page.ui.combo_email_domain.findText(email[1])
            if idx >= 0:
                self.register_page.ui.combo_email_domain.setCurrentIndex(idx)
        
        self.register_page.current_page_check(arg)
        self.stackedWidget.setCurrentWidget(self.register_page)
    
    def show_login_page(self):
        """로그인 화면으로 이동
        """
        # 헤더 숨기기
        self.lbl_title.hide()
        self.lbl_user_icon.hide()
        self.lbl_user_icon.hide()
        self.btn_logout.hide()
        self.btn_exit.hide()
        # 각 버튼 보이기
        self.btn_manage_user.show() # 회원 관리 버튼 보이기
        self.btn_manage_book.show() # 도서 관리 버튼 보이기
        self.btn_rent_list.show() # 전체 대여 목록 보이기
        self.book_info_page.del_book_btn.show() # 도서 삭제 보이기
        self.rental_list_page.btn_return.show() # 도서 강제 반납 보이기
        self.rental_screen.ui_file.rent_btn.show() # 도서 목록 도서 대여 버튼 보이기
        self.confirm_screen.ui_file.rent_give_btn.show() # 대여 목록 반납 버튼 보이기
        self.confirm_screen.ui_file.rent_over_btn.show() # 대여 목록 연장 버튼 보이기
        self.register_page.ui.input_id.setReadOnly(False)
        # 로그인 입력창 비우기
        self.login_page.ui.lineEdit_id.clear()
        self.login_page.ui.lineEdit_pw.clear()
        self.register_page.reset_input()
        self.register_page.ui.gb_grade.hide()
        # 로그인 페이지로
        self.stackedWidget.setCurrentWidget(self.login_page)
    
    def show_rental_page(self):
        """도서대여 화면으로 이동
        """
        self.rental_screen.add_widget_data()
        if self.current_user["role"] == "a":
            self.rental_screen.ui_file.rent_btn.hide()
        else:
            self.rental_screen.ui_file.rent_btn.show()
        self.lbl_title.setText("도서 대여")
        self.stackedWidget.setCurrentWidget(self.rental_screen)
    
    def show_rental_list_page(self):
        """대여 목록 화면으로 이동
        """
        self.lbl_title.setText("대여 목록")
        self.rental_list_page.refresh_data()
        self.stackedWidget.setCurrentWidget(self.rental_list_page)
    
    def show_confirm_page(self):
        """개인 대여 확인 화면으로 이동
        """
        # self.confirm_screen.add_widget_data()
        self.lbl_title.setText("대여 확인")
        self.confirm_screen.main_table()
        self.stackedWidget.setCurrentWidget(self.confirm_screen)
    
    def show_main_page(self):
        """메인 화면으로 이동
        """
        self.lbl_title.show()
        self.lbl_title.setText(u"\U0000b3c4\U0000c11c\U0000ad00 \U0001f4d8")
        self.lbl_user_icon.show()
        self.btn_logout.show()
        self.lbl_user_icon.show()
        self.btn_exit.show()
        if hasattr(self, "current_user"):
            self.apply_permission()
        self.stackedWidget.setCurrentWidget(self.main_page)
        # 2. 화면이 완전히 전환되어 위젯이 그려진 후(0.05초 뒤) GIF 로드 및 재생
        from PySide6.QtCore import QTimer
        QTimer.singleShot(50, self.load_main_gif)
        
    def load_main_gif(self):
            """GIF 로드 및 재생 전용 메서드"""
            # main_page 내부에서 label_gif 위젯 찾기
            label_gif_widget = self.main_page.findChild(QLabel, "label_gif")
            
            # 만약 main_page 직속이 아니라 전체 window에서 찾아야 한다면 아래 줄 사용:
            if not label_gif_widget:
                label_gif_widget = self.findChild(QLabel, "label_gif")
            
            if label_gif_widget:
                # 절대 경로로 GIF 위치 지정
                current_dir = os.path.dirname(os.path.abspath(__file__))
                gif_path = os.path.join(current_dir, "ui_data", "library_animation.gif")
                
                # 파일이 실제 존재하는지 체크
                if not os.path.exists(gif_path):
                    print(f"오류: GIF 파일을 찾을 수 없습니다. 경로를 확인하세요 -> {gif_path}")
                    return
    
                # 기존 애니메이션 중지 및 메모리 정리
                if hasattr(self, 'movie') and self.movie:
                    self.movie.stop()
                
                label_gif_widget.setFixedSize(811, 536)
                    
                self.movie = QMovie(gif_path)
                label_gif_widget.setMovie(self.movie)
                
                self.movie.setScaledSize(label_gif_widget.size())
    
                self.movie.start()
                
                label_gif_widget.lower()
                #처음 로드될 때도 위치를 중앙으로 한번 잡아줌 
                self.resizeEvent(None)
                # print("GIF 애니메이션 재생 시작 성공!")
            else:
                print("Warning: label_gif 위젯을 찾을 수 없습니다. Qt Designer의 objectName을 확인하세요.")
    
    def show_books_list_page(self):
        """도서 관리 화면으로 이동
        """
        self.lbl_title.setText("도서 관리")
        self.book_info_page.search_lineEdit.clear()
        self.book_info_page.refresh_book_list()
        self.stackedWidget.setCurrentWidget(self.book_info_page)
    
    def show_user_list_page(self):
        """회원 관리 화면으로 이동
        """
        self.lbl_title.setText("회원 관리")
        self.user_edit_page.refresh_table()
        self.stackedWidget.setCurrentWidget(self.user_edit_page)
    
    def close_program(self):
        self.close()
    
    def center_on_screen(self):
        """화면 중앙에 배치
        """
        screen = QApplication.primaryScreen().geometry()

        window_size = self.geometry()

        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2

        self.move(x, y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibMainWindow()
    window.show()
    sys.exit(app.exec())