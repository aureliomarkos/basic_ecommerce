import flet as ft

# app
from utils import MessageConfirm, validate_cep, cntStyle, txtTitleLargeStyle, txtFldBorderColorStyle, show_snack_bar_warning
from sql_utils import db


class CrudAddress:

    # select all address client from address
    def select_all_address_client_from_address(self, idCliente):
        conn, cursor = db()
        cursor.execute("SELECT id, rua, nro, bairro, cidade, estado, cep, complemento, principal FROM endereco WHERE id_cliente=? AND ativo=1 ORDER BY principal DESC", (idCliente,))
        address = cursor.fetchall()
        conn.close()
        return address


    # select address from address
    def select_address_from_address(self, idAddress):
        conn, cursor = db()
        cursor.execute("SELECT id, rua, nro, bairro, cidade, estado, cep, complemento, principal FROM endereco WHERE id=?", (idAddress,))
        address = cursor.fetchone()
        conn.close()
        return address


    # update address
    def update_address(self, idAddress, rua, nro, bairro, cidade, estado, cep, complemento):
        conn, cursor = db()
        cursor.execute("UPDATE endereco SET rua=?, nro=?, bairro=?, cidade=?, estado=?, cep=?, complemento=? WHERE id=?", (rua, nro, bairro, cidade, estado, cep, complemento, idAddress))
        conn.commit()
        conn.close()


    # insert new address
    def insert_into_address(self, rua, nro, bairro, cidade, estado, cep, complemento, idCliente):
        conn, cursor = db()
        cursor.execute("INSERT INTO endereco (id_cliente, rua, nro, bairro, cidade, estado, cep, complemento) VALUES (?,?,?,?,?,?,?,?)", (idCliente, rua, nro, bairro, cidade, estado, cep, complemento))
        idAddress = cursor.lastrowid
        conn.commit()
        conn.close()
        return idAddress


    # remove address
    def delete_from_address(self, idAddress):
        conn, cursor = db()
        cursor.execute("UPDATE endereco SET ativo=0 WHERE id=?", (idAddress, ))
        conn.commit()
        conn.close()


    # update default address
    def update_default_address(self, idAddress, idCliente):
        conn, cursor = db()
        cursor.execute("UPDATE endereco SET principal=0 WHERE id_cliente=?", (idCliente, ))
        conn.commit()
        cursor.execute("UPDATE endereco SET principal=1 WHERE id=?", (idAddress, ))
        conn.commit()
        conn.close()



class Address(CrudAddress):


    def __init__(self, main):
        self.page = main.page
        self.parent = main      # address can call from account and checkout pages
        self.main = main.main   # main.py
        self.addressDefault=None

        # start list all address and form address
        self.set_container_list_all_address()
        self.set_container_form_address()


    # clear
    def clear(self):
        self.addressDefault=None


    # get container list address
    def get_container_list_all_address(self):
        return self.cntListAddress

    
    # get container form address
    def get_container_form_address(self):
        return self.cntFormAddress

    
    # refresh list address
    def refresh(self):
        
        # clear colRadio
        self.colRadio.clean()

        # set all radio options address
        self.set_all_radio_options_address()

        # if for page Checkout (crud in Checkout)
        if self.parent.__class__.__name__ == 'Checkout':
            self.main.account.clear()
            self.main.account.refresh()
        

    # set all radio options address
    def set_all_radio_options_address(self):

        # get all address client
        self.allAddress = self.select_all_address_client_from_address(self.main.env.idClient)

        #
        if not self.allAddress:
            self.radioGroupAddress.value=None
            self.iconBtnEditAddress.disabled=True
            self.iconBtnRemoveAddress.disabled=True
            self.iconBtnSetDefaultAddress.disabled=True
            self.page.update()
            return None

        # iter all address
        for idx, address in enumerate(self.allAddress):

            # address default
            varDefault=''
            if address['principal']:
                self.addressDefault=idx
                varDefault='(Default)'
            
            # 
            self.txtAddress = f'{address['rua']}, {address['nro']} {address['bairro']} {address['cidade']} {varDefault}'
            self.radioAddress = ft.Radio(value=idx, label=self.txtAddress, data=address['id'])
            self.colRadio.controls.append(self.radioAddress)

        # set address default
        if self.addressDefault:
            self.radioGroupAddress.value=self.addressDefault
        else:
            self.radioGroupAddress.value=0

        #
        self.page.update()


    # set container list address
    def set_container_list_all_address(self):
        
        # title
        txtTitleAdress = ft.Text('Endereço', **txtTitleLargeStyle)
  
        # radio group address
        self.radioGroupAddress = ft.RadioGroup()
        self.colRadio = ft.Column(width=500, height=380, scroll=ft.ScrollMode.ALWAYS)
        self.radioGroupAddress.content = self.colRadio

        # icons list address
        self.iconBtnNewAddress = ft.TextButton(text='Novo', icon=ft.icons.ADD_LOCATION_ROUNDED, tooltip='Adicionar Endereço', on_click=self.on_click_button_add_address)
        self.iconBtnEditAddress = ft.TextButton(text='Alterar', icon=ft.icons.EDIT, tooltip='Alterar endereço', on_click=self.on_click_button_edit_address)
        self.iconBtnRemoveAddress = ft.TextButton(text='Apagar', icon=ft.icons.DELETE_FOREVER, tooltip='Excluir endereço', on_click=self.on_click_button_remove_address)
        self.iconBtnSetDefaultAddress = ft.TextButton(text='Default', icon=ft.icons.LOCATION_ON, tooltip='Define endereço como principal', on_click=self.on_click_button_set_default_address)

        #
        rowIcons = ft.Row([self.iconBtnNewAddress, self.iconBtnEditAddress, self.iconBtnRemoveAddress, self.iconBtnSetDefaultAddress])
        cntRowIconsEditRemove = ft.Container(rowIcons)

        # 
        colAddress = ft.Column([txtTitleAdress, self.radioGroupAddress, cntRowIconsEditRemove])
        self.cntListAddress = ft.Container(colAddress, padding=10, **cntStyle)
        
        # set all address
        self.set_all_radio_options_address()


    # container form address
    def set_container_form_address(self):
        
        # title
        self.txtTitleAddress = ft.Text(**txtTitleLargeStyle)

        # text field for input data
        self.rua = ft.TextField(label='Rua', width=430, **txtFldBorderColorStyle)
        self.nro = ft.TextField(label="Nro", width=120, **txtFldBorderColorStyle)
        self.bairro = ft.TextField(label='Bairro', **txtFldBorderColorStyle)
        self.cidade = ft.TextField(label='Cidade', width=340, **txtFldBorderColorStyle)
        self.estado = ft.TextField(label='Estado', width=80, **txtFldBorderColorStyle)
        self.cep = ft.TextField(label='Cep', width=120, input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9-]", replacement_string=""), **txtFldBorderColorStyle)
        self.complemento = ft.TextField(label='Complemento', **txtFldBorderColorStyle)

        # required fields for form address
        self.requiredFieldsFormAddress={}
        self.requiredFieldsFormAddress['Rua deve ser informado!'] = self.rua
        self.requiredFieldsFormAddress['Número deve ser informado!'] = self.nro
        self.requiredFieldsFormAddress['Bairro deve ser informado!'] = self.bairro
        self.requiredFieldsFormAddress['Cidade deve ser informado!'] = self.cidade
        self.requiredFieldsFormAddress['Estado deve ser informado!'] = self.estado
        self.requiredFieldsFormAddress['Cep deve ser informado!'] = self.cep

        # buttons
        btnSaveChange = ft.ElevatedButton(text='Salvar', on_click=self.on_click_button_save_address)
        btnCloseCntEditAddress = ft.ElevatedButton('Fechar', on_click=self.on_click_button_close_form)
        rowButtons = ft.Row([ft.Container(width=230), btnSaveChange, btnCloseCntEditAddress])

        #
        rowNroBairro = ft.Row([self.nro, self.bairro])
        rowCidadeEstado = ft.Row([self.cidade, self.estado])
        rowCepComplemento = ft.Row([self.cep, self.complemento])
        
        #
        colEditAddress = ft.Column([self.txtTitleAddress, self.rua, rowNroBairro, rowCidadeEstado,  rowCepComplemento, rowButtons])
        self.cntFormAddress = ft.Container(
                                    colEditAddress,
                                    padding=10,
                                    offset=ft.transform.Offset(-2, 0),
                                    animate_offset=ft.animation.Animation(600),
                                    **cntStyle)


    # set values container edit address
    def set_values_form_address(self, address):
        self.rua.value = address['rua']
        self.nro.value = address['nro']
        self.bairro.value = address['bairro']
        self.cidade.value = address['cidade']
        self.estado.value = address['estado']
        self.cep.value = address['cep']
        self.complemento.value = address['complemento']
        self.cntFormAddress.offset = ft.transform.Offset(0, 0)
        self.page.update()

    
    # on click button add address
    def on_click_button_add_address(self, e):

        # set flag insert new address
        self.flagDataSet = 'Insert'
        self.txtTitleAddress.value = 'Novo Endereço'

        # disable container address
        self.cntListAddress.disabled=True

        # clear text fields form address
        self.rua.value = ""
        self.nro.value = ""
        self.bairro.value = ""
        self.cidade.value = ""
        self.estado.value = ""
        self.cep.value = ""
        self.complemento.value = ""

        # show form
        self.cntFormAddress.offset = ft.transform.Offset(0, 0)
        self.page.update()


    # on click button edit address
    def on_click_button_edit_address(self, e):

        # set flag edit address
        self.flagDataSet = 'Edit'
        self.txtTitleAddress.value = 'Alterar Endereço'

        # disable container address
        self.cntListAddress.disabled=True

        idAddress = int(self.radioGroupAddress.content.controls[int(self.radioGroupAddress.value)].data)
        address = self.select_address_from_address(idAddress=idAddress)
        self.set_values_form_address(address)


    # on click button remove address
    def on_click_button_remove_address(self, e):

        # message question
        address = self.radioGroupAddress.content.controls[int(self.radioGroupAddress.value)].label
        message = MessageConfirm(self.page, 'Excluir Endereço', f'Deseja Apagar endereço: {address}?')

        while message.dialogResponse == None:
            pass
        if message.dialogResponse == False:
            return None

        #
        idAddress = self.radioGroupAddress.content.controls[int(self.radioGroupAddress.value)].data
        self.delete_from_address(idAddress)
        self.refresh()


    # on click button set default address
    def on_click_button_set_default_address(self, e):
        idAddress = self.radioGroupAddress.content.controls[int(self.radioGroupAddress.value)].data

        # if radio choice principal
        if self.addressDefault == idAddress:
            return None

        # set default address
        self.addressDefault = idAddress

        #
        self.update_default_address(idAddress, self.main.env.idClient)
        self.refresh()


    # on click button save address
    def on_click_button_save_address(self, e):

        # verify required fields form address
        for field in self.requiredFieldsFormAddress:
            if not self.requiredFieldsFormAddress[field].value:
                show_snack_bar_warning(self.page, field)
                self.requiredFieldsFormAddress[field].focus()
                self.page.update()
                return None

        # validate cep
        if not validate_cep(self.cep.value):
            show_snack_bar_warning(self.page, 'Cep no formato inválido? (99999-999)')
            self.cep.focus()
            self.page.update()
            return None

        # if edit address
        if self.flagDataSet == 'Edit':
            self.update_address(
                    self.radioGroupAddress.content.controls[int(self.radioGroupAddress.value)].data,
                    self.rua.value,
                    self.nro.value,
                    self.bairro.value,
                    self.cidade.value,
                    self.estado.value,
                    self.cep.value,
                    self.complemento.value)

        # if new address
        elif self.flagDataSet == 'Insert':
            idAddress = self.insert_into_address(
                    self.rua.value,
                    self.nro.value,
                    self.bairro.value,
                    self.cidade.value,
                    self.estado.value,
                    self.cep.value,
                    self.complemento.value,
                    self.main.env.idClient)

        # enable container address
        self.cntListAddress.disabled=False

        # enable buttons 
        self.iconBtnEditAddress.disabled=False
        self.iconBtnRemoveAddress.disabled=False
        self.iconBtnSetDefaultAddress.disabled=False

        # hidden form address
        self.cntFormAddress.offset = ft.transform.Offset(-2, 0)
        self.refresh()
        self.page.update()


    # on click button close form
    def on_click_button_close_form(self, e):

        # enable container address
        self.cntListAddress.disabled=False

        # hiden form address
        self.cntFormAddress.offset = ft.transform.Offset(-2, 0)
        self.page.update()