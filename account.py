import flet as ft

# app
from utils import cntStyle, txtTitleLargeStyle, txtColorStyle, txtFldBorderColorStyle, show_snack_bar_warning
from sql_utils import db
from header_app import HeaderApp
from address import Address



class CrudAccount:

    # select client
    def select_from_client(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT * FROM cliente WHERE id=?", (idClient, ))
        client = cursor.fetchall()
        conn.close()
        return client


    # update client
    def update_cliente(self, idClient, phone, email, password):
        conn, cursor = db()
        cursor.execute("UPDATE cliente SET celular=?, email=?, senha=? WHERE id=?", (phone, email, password, idClient))
        conn.commit()
        conn.close()



class PersonalData(CrudAccount):

    def __init__(self, main):
        self.page = main.page
        self.main = main


    # set form personal data
    def set_form_personal_data(self):
        
        # get data from client
        client = self.select_from_client(self.main.env.idClient)

        # if not client
        if not client:
            return None

        # recno client 
        client = client[0]

        # password
        self.password = client['senha']

        # form personal data
        txtTitle = ft.Text('Dados Pessoais', **txtTitleLargeStyle)
        txtName = ft.Text(f'Nome: {client['nome']}', **txtColorStyle)
        txtCpf = ft.Text(f'Cpf: {client['cpf']}', **txtColorStyle)
        self.txtFldPhone = ft.TextField(label='Celular', value=client['celular'], input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9))(.)]", replacement_string=""), **txtFldBorderColorStyle)
        self.txtFldEmail = ft.TextField(label='Email', value=client['email'], **txtFldBorderColorStyle)
        self.txtFldPassword = ft.TextField(label='Senha', value=client['senha'], password=True, can_reveal_password=True, **txtFldBorderColorStyle)
        btnSave = ft.ElevatedButton(text='Salvar', on_click=self.on_click_button_save_personal_data)

        # row button save
        rowBtnSave = ft.Row([ft.Container(width=200), btnSave])

        # column personal data
        colPersonalData = ft.Column([txtTitle, txtName, txtCpf, self.txtFldPhone, self.txtFldEmail, self.txtFldPassword, rowBtnSave])
        
        # container personal data
        self.cntPersonalData = ft.Container(
                                    colPersonalData,
                                    padding=10,
                                    **cntStyle,
                                )

        # fields required
        self.requiredFieldsPersonalForm = {
            'Campo Celular dever ser informado!':self.txtFldPhone,
            'Campo Email deve ser informado!':self.txtFldEmail,
            'Campo Senha deve ser informado!':self.txtFldPassword
        }


    # get container
    def get(self):
        return self.cntPersonalData


    # on click button save personal data
    def on_click_button_save_personal_data(self, e):
        
        # verify required fields form personal
        for field in self.requiredFieldsPersonalForm:
            if not self.requiredFieldsPersonalForm[field].value:
                show_snack_bar_warning(self.page, field)
                self.requiredFieldsPersonalForm[field].focus()
                self.page.update()
                return None

        # update client
        self.update_cliente(self.main.env.idClient, self.txtFldPhone.value, self.txtFldEmail.value, self.txtFldPassword.value)

        # hidden form
        self.cntPersonalData.visible=False
        self.main.account.iconBtnPersonalData.selected=False
        
        # page update
        self.page.update()



class Account(HeaderApp, CrudAccount):

    def __init__(self, main):
        HeaderApp.__init__(self, main)
        self.page = main.page
        self.main = main

        # rows page
        self.row_header = ft.Row([self.cntHeaderMaster])
        self.row_body = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START)
        self.row_footer = ft.Row()

        # column master
        self.colMaster = ft.Column([self.row_header, self.row_body, self.row_footer])


    # clear page
    def clear(self):
        self.colData.controls.clear()
        self.address.clear()
        
        # set icons state selected == False
        self.iconBtnPersonalData.selected=False
        self.iconBtnAddress.selected=False
        self.iconBtnLogout.selected=False


    # get control master
    def get(self):
        return self.colMaster


    # show page
    def show(self):
        self.refresh()


    # refresh page
    def refresh(self):

        # start controls address
        self.address = Address(self)

        # start page Account
        self.set_page_body_account()


    # set page body account
    def set_page_body_account(self):

        # login
        self.iconBtnLogin = ft.IconButton(icon=ft.icons.LOGIN, on_click=self.on_click_icon_button_login)
        txtLogin = ft.Text('Login', **txtColorStyle)
        colLogin = ft.Column([self.iconBtnLogin, txtLogin], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # personal data
        self.iconBtnPersonalData = ft.IconButton(
                                        selected=False,
                                        icon=ft.icons.ACCOUNT_CIRCLE_OUTLINED,
                                        selected_icon=ft.icons.ACCOUNT_CIRCLE,
                                        on_click=self.on_click_icon_button_personal_data)
        txtPersonalData = ft.Text('Dados Pessoais', **txtColorStyle)
        colPersonalData = ft.Column([self.iconBtnPersonalData, txtPersonalData], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # address
        self.iconBtnAddress = ft.IconButton(
                                    selected=False,
                                    icon=ft.icons.LOCATION_ON_OUTLINED,
                                    selected_icon=ft.icons.LOCATION_ON_ROUNDED,
                                    on_click=self.on_click_icon_button_address)
        txtAddress = ft.Text('Endereço', **txtColorStyle)
        colAddress = ft.Column([self.iconBtnAddress, txtAddress], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER) 

        # logout
        self.iconBtnLogout = ft.IconButton(
                                    selected=False,
                                    icon=ft.icons.LOGOUT_OUTLINED,
                                    selected_icon=ft.icons.LOGOUT,
                                    on_click=self.on_click_icon_button_logout)
        txtLogout = ft.Text('Logout', **txtColorStyle)
        colLogout = ft.Column([self.iconBtnLogout, txtLogout], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        # columns icons
        colIcon = ft.Column([colLogin, colPersonalData, colAddress, colLogout], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
        self.colData = ft.Column()

        cntColIcon = ft.Container(colIcon, height=840, padding=10, **cntStyle)
        self.row_body.controls = [cntColIcon, self.colData]

        #
        self.page.update()


    # on click icon button login
    def on_click_icon_button_login(self, e):
        self.page.go('/login')


    # on click icon button personal
    def on_click_icon_button_personal_data(self, e):

        #
        self.iconBtnAddress.selected=False
        self.iconBtnLogout.selected=False
        e.control.selected = not e.control.selected

        if e.control.selected == True:
            self.personal = PersonalData(self.main)
            self.personal.set_form_personal_data()
            self.colData.controls = [self.personal.get()]
        else:
            self.colData.controls.clear()
        self.page.update()


    # on click icon button address
    def on_click_icon_button_address(self, e):
        self.iconBtnPersonalData.selected=False
        self.iconBtnLogout.selected=False
        e.control.selected = not e.control.selected
        
        if e.control.selected == True:
            self.colData.controls = [
                self.address.get_container_list_all_address(),
                self.address.get_container_form_address()
            ]
        else:
            self.colData.controls.clear()
        self.page.update()


    # on click icon button logout
    def on_click_icon_button_logout(self, e):
        self.iconBtnPersonalData.selected=False
        self.iconBtnAddress.selected=False
        e.control.selected = not e.control.selected
        
        #
        if e.control.selected == True:
            
            self.colData.controls.clear()
            self.iconBtnLogin.disabled=False
            
            # set client=1 (default)
            self.main.env.change_client()
        
        self.page.update()