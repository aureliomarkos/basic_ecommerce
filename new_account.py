import flet as ft

# app
from utils import validate_cpf, validate_email, cntStyle, txtTitleLargeStyle, txtFldBorderColorStyle, show_snack_bar_warning
from sql_utils import db



class CrudNewAccount:
    

    # insert new account
    def insert_into_client(self, name, cpf, phone, email, senha):
        conn, cursor = db()
        cursor.execute("INSERT INTO cliente (nome, vendedor_nome, cpf, celular, email, senha) VALUES (?,?,?,?,?,?)", (name, 'Vendedor: '+name, cpf, phone, email, senha))
        lastrowid = cursor.lastrowid
        conn.commit()
        conn.close()
        return lastrowid


    # verify exist cpf
    def select_cpf_from_client(self, cpf):
        conn, cursor = db()
        cursor.execute("SELECT cpf FROM cliente WHERE cpf=?", (cpf,))
        cpf = cursor.fetchone()
        conn.close()
        return cpf


    # verify exist email
    def select_email_from_client(self, email):
        conn, cursor = db()
        cursor.execute("SELECT email FROM cliente WHERE email=?", (email,))
        email = cursor.fetchone()
        conn.close()
        return email


class NewAccount(CrudNewAccount):
    

    def __init__(self, main):
        self.page = main.page
        self.main = main

        # text fields required
        self.requiredFieldsFormNewAccount = {}
        
        # controls
        self.txtTitle = ft.Text(value='Nova Conta', **txtTitleLargeStyle)
        self.name = ft.TextField(label='Nome', height=40, prefix_icon=ft.icons.ACCOUNT_CIRCLE, **txtFldBorderColorStyle)
        self.phone = ft.TextField(label='Celular', height=40, prefix_icon=ft.icons.PHONE, input_filter=ft.InputFilter(regex_string='[0-9.)(]'), **txtFldBorderColorStyle)
        self.cpf = ft.TextField(label='Cpf', color=ft.colors.BLUE_800, height=40, input_filter=ft.InputFilter(regex_string='[0-9.-]'))
        self.email = ft.TextField(label='E-mail', height=40, prefix_icon=ft.icons.EMAIL, keyboard_type=ft.KeyboardType.EMAIL, **txtFldBorderColorStyle)
        self.senha = ft.TextField(label='Senha', height=40, prefix_icon=ft.icons.PASSWORD, password=True, can_reveal_password=True, **txtFldBorderColorStyle)
        self.btnAddClient = ft.ElevatedButton(text='Cadastrar', color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_800, width=200, on_click=self.on_click_btn_add_client)
        self.btnAddClient.style = ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=10))

        # container
        txtTitle = ft.Container(self.txtTitle, padding=10, alignment=ft.alignment.center)
        self.cntName = ft.Container(self.name, padding=10)
        self.cntPhone = ft.Container(self.phone, padding=10)
        self.cntCpf = ft.Container(self.cpf, padding=10)
        self.cntEmail = ft.Container(self.email, padding=10)
        self.cntSenha = ft.Container(self.senha, padding=10)
        self.cntBtnAddClient = ft.Container(self.btnAddClient, alignment=ft.alignment.center, padding=10)

        # text fields required
        self.requiredFieldsFormNewAccount['Nome deve ser informado!'] = self.name
        self.requiredFieldsFormNewAccount['Número celular deve ser informado!'] = self.phone
        self.requiredFieldsFormNewAccount['Cpf deve ser informado!'] = self.cpf
        self.requiredFieldsFormNewAccount['Email deve ser informado!'] = self.email
        self.requiredFieldsFormNewAccount['Senha deve ser informado!'] = self.senha

        # column Master
        colMaster = ft.Column([
                                txtTitle,
                                self.cntName,
                                self.cntPhone,
                                self.cntCpf,
                                self.cntEmail,
                                self.cntSenha,
                                self.cntBtnAddClient])

        # container Master
        self.cntMaster = ft.Row([ft.Container(
                                    colMaster,
                                    width=300,
                                    margin=ft.margin.only(top=200),
                                    **cntStyle)],
                                    alignment=ft.MainAxisAlignment.CENTER)


    # get container Master
    def get(self):
        return self.cntMaster


    # on click button add client
    def on_click_btn_add_client(self, e):
        
        # required fields
        for field in self.requiredFieldsFormNewAccount:
            if not self.requiredFieldsFormNewAccount[field].value:
                show_snack_bar_warning(self.page, field)
                self.requiredFieldsFormNewAccount[field].focus()
                self.page.update()
                return None

        # validate cpf
        if not validate_cpf(self.cpf.value):
            show_snack_bar_warning(self.page, 'Cpf inválido deve estar no formato: "999.999.999-99"!')
            self.cpf.focus()
            self.page.update()
            return None

        # exist cpf?
        if self.select_cpf_from_client(self.cpf.value):
            show_snack_bar_warning(self.page, 'Cpf já existe em nossa base de dados!')
            self.cpf.focus()
            self.page.update()
            return None

        # validate email
        if not validate_email(self.email.value):
            show_snack_bar_warning(self.page, 'Email inválido!')
            self.email.focus()
            self.page.update()
            return None

        # exist email?
        if self.select_email_from_client(self.email.value):
            show_snack_bar_warning(self.page, 'Email já existe em nossa base de dados!')
            self.email.focus()
            self.page.update()
            return None

        # insert new client
        idClient = self.insert_into_client(self.name.value, self.cpf.value, self.phone.value, self.email.value, self.senha.value)

        # save login in side client
        self.main.env.change_client(idClient=idClient, clientName=self.name.value)

        # clear form fields
        self.name.value = ""
        self.phone.value = ""
        self.cpf.value = ""
        self.email.value = ""
        self.senha.value = ""

