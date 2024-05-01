import flet as ft


# app
from utils import validate_email, cntStyle, show_snack_bar_warning
from sql_utils import db



# crud table client
class CrudLogin:
    
    # select client
    def select_from_client(self, email, password):
        conn, cursor = db()
        cursor.execute("SELECT * FROM cliente WHERE email=? AND senha=?", (email, password))
        client = cursor.fetchall()
        conn.close()
        return client



# class login app
class Login(CrudLogin):
    
    
    def __init__(self, main):
        self.page = main.page
        self.main = main

        # text fields required
        self.requiredFieldsFormLogin = {}

        # controls
        txtLogin = ft.Text(value='Login', color=ft.colors.BLUE_800, size=30)
        cntTxtLogin = ft.Container(txtLogin, alignment=ft.alignment.center)
        self.email = ft.TextField(label='E-mail', prefix_icon=ft.icons.EMAIL, color=ft.colors.BLUE_800, height=40, autofocus=True)
        self.password = ft.TextField(label='Senha', prefix_icon=ft.icons.PASSWORD, color=ft.colors.BLUE_800, height=40, password=True, can_reveal_password=True)
        btnLogin = ft.ElevatedButton(text='Conectar', color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_800, width=200, on_click=self.on_click_btn_login)
        cntBtnLogin = ft.Container(btnLogin, alignment=ft.alignment.center)
        
        btnLogin.style = ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=10))
        
        self.cbConnected = ft.Checkbox(label='Mantenha-me conectado', disabled=True)

        btnNewAccount = ft.ElevatedButton(text='Criar Conta', color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_800, width=200, on_click=self.on_click_btn_new_account)
        cntBtnNewAccount = ft.Container(btnNewAccount, alignment=ft.alignment.center)
        
        btnNewAccount.style = ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=10))

        # text field required
        self.requiredFieldsFormLogin["Campo e-mail deve ser informado?"] = self.email
        self.requiredFieldsFormLogin["Campo senha deve ser informado?"] = self.password

        # column 
        colLogin = ft.Column([cntTxtLogin, self.email, self.password, cntBtnLogin, cntBtnNewAccount, self.cbConnected], spacing=30)

        # container master
        self.cntMaster = ft.Row([
                            ft.Container(colLogin,
                                         width=300,
                                         margin=ft.margin.only(top=200),
                                         padding=10,
                                         **cntStyle)],
                                         alignment=ft.MainAxisAlignment.CENTER,
                                         )

    
    # get container master login
    def get(self):
        return self.cntMaster

   
    # on click button login
    def on_click_btn_login(self, e):

        # verify text field required
        for field in self.requiredFieldsFormLogin:
            if not self.requiredFieldsFormLogin[field].value:
                show_snack_bar_warning(self.page, field)
                self.requiredFieldsFormLogin[field].focus()
                self.page.update()
                return None


        # validate email
        if not validate_email(self.email.value):
            show_snack_bar_warning(self.page, 'Email inválido!')
            self.email.focus()
            self.page.update()
            return None


        # select client
        client = self.select_from_client(self.email.value, self.password.value)

        if client:

            client = client[0]

            # change client for app
            self.main.env.change_client(idClient=client['id'], clientName=client['nome'])

        else:
            show_snack_bar_warning(self.page, 'Senha incorreta.')
            self.email.focus()
            self.page.update()

    
    # on click button new account
    def on_click_btn_new_account(self, e):
        self.page.go('/new_account')


