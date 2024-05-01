import flet as ft

# app
from utils import convert_image_base64, MessageConfirm, cntStyle, txtColorStyle, txtFldBorderColorStyle, txtTitleLargeStyle, txtLabelSmallStyle, show_snack_bar_warning
from sql_utils import db
from header_app import HeaderApp

# label for controls category
SWITCH_ACTIVE, ICON_EDIT, ID_CATEGORY, DESCRIPTION = range(4)



class CrudSell:
    

    # select imagem add 
    def select_image_add_from_app(self):
        conn, cursor = db()
        cursor.execute("SELECT imagem FROM app WHERE nome='image_add_64.png'")
        imagem = cursor.fetchone()[0]
        conn.close()
        return imagem


    # select product where description
    def select_product_from_view_product(self, idSeller, descriptionProduct):
        conn, cursor = db()
        cursor.execute("SELECT * FROM view_produto WHERE id_vendedor=? AND descricao LIKE ? AND situacao != 'Inativo' ORDER BY descricao", (idSeller, descriptionProduct + '%'))
        products = cursor.fetchall()
        conn.close()
        return products


    # select all products
    def select_all_product_from_view_product(self, idSeller):
        conn, cursor = db()
        cursor.execute("SELECT * FROM view_produto WHERE id_vendedor=? AND situacao != 'Inativo' ORDER BY descricao", (idSeller,))
        allProducts = cursor.fetchall()
        conn.close()
        return allProducts


    # select product description
    def select_product_description(self, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT id_produto FROM produto_descricao WHERE id_produto=?", (idProduct, ))
        prodDesc = cursor.fetchone()
        conn.close()
        return prodDesc

    
    # insert product in table product
    def insert_product_into_product(self, idSeller, description, qtty, unit, price, image, idCategory, situation, condition, observation):
        conn, cursor = db()
        cursor.execute("INSERT INTO produto (id_vendedor, descricao, qtde, unidade, preco, imagem, id_categoria, condicao, situacao, observacao) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (idSeller, description, qtty, unit, price, image, idCategory, condition, situation, observation))
        lastRowId = cursor.lastrowid
        conn.commit()
        conn.close()
        return lastRowId


    # insert product into product_description
    def insert_product_into_product_description(self, idProduct, description, imagem_0, imagem_1, imagem_2, imagem_3, imagem_4):
        conn, cursor = db()
        cursor.execute("INSERT INTO produto_descricao(id_produto, descricao, imagem_0, imagem_1, imagem_2, imagem_3, imagem_4) VALUES(?,?,?,?,?,?,?)",
                       (idProduct, description, imagem_0, imagem_1, imagem_2, imagem_3, imagem_4))
        conn.commit()
        conn.close()


    # update product
    def update_product(self, idProduct, description, qtty, unit, price, image, idCategory, condition, situation, observation):
        conn, cursor = db()
        cursor.execute("UPDATE produto SET descricao=?, qtde=?, unidade=?, preco=?, imagem=?, id_categoria=?, condicao=?, situacao=?, observacao=? WHERE id=?",
                       (description, qtty, unit, price, image, idCategory, condition, situation, observation, idProduct))
        conn.commit()
        conn.close()


    # update description product
    def update_description_product(self, idProduct, description, image_0, image_1, image_2, image_3, image_4):
        conn, cursor = db()
        cursor.execute("UPDATE produto_descricao SET descricao=?, imagem_0=?, imagem_1=?, imagem_2=?, imagem_3=?,  imagem_4=? WHERE id_produto=?",
                       (description, image_0, image_1, image_2, image_3, image_4, idProduct))
        conn.commit()
        conn.close()

    
    # delete product from product
    def update_situation_product_from_product(self, idProduct):
        conn, cursor = db()
        cursor.execute("UPDATE produto SET situacao = 'Inativo' WHERE id=?", (idProduct, ))
        conn.commit()
        conn.close()


    # select all category from table category
    def select_all_from_category(self):
        conn, cursor = db()
        cursor.execute("SELECT id, descricao, ativo FROM categoria WHERE ativo=1 ORDER BY descricao")
        allCategory = cursor.fetchall()
        conn.close()
        return allCategory


    # select description from category
    def select_description_from_category(self, description):
        conn, cursor = db()
        cursor.execute("SELECT id FROM categoria WHERE LOWER(descricao)=?", (description, ))
        idDescription = cursor.fetchone()
        conn.close()
        return idDescription


    # select description from category
    def select_all_from_category_like_description(self, description):
        conn, cursor = db()
        cursor.execute("SELECT id, descricao, ativo FROM categoria WHERE LOWER(descricao) LIKE ? ORDER BY descricao", (description + '%', ))
        allDescription = cursor.fetchall()
        conn.close()
        return allDescription


    # insert into category
    def insert_into_category(self, description):
        conn, cursor = db()
        cursor.execute("INSERT INTO categoria (descricao) VALUES (?)", (description,))
        lastRowId = cursor.lastrowid
        conn.commit()
        conn.close()
        return lastRowId


    # update description category
    def update_description_category(self, idCategory, description):
        conn, cursor = db()
        cursor.execute("UPDATE categoria SET descricao=? WHERE id=?", (description, idCategory))
        conn.commit()
        conn.close()


    # update category active
    def update_active_category(self, idCategory, bool):
        conn, cursor = db()
        cursor.execute("UPDATE categoria SET ativo=? WHERE id=?", (bool, idCategory))
        conn.commit()
        conn.close()



class GetCategory(CrudSell):

    def __init__(self, main):
        self.page = main.page
        self.main = main

        # text field category
        self.txtFldDescription = ft.TextField(label='Descrição da Categoria',
                                              width=450,
                                              on_change=self.on_change_text_field_description_category,
                                              on_submit=self.on_click_button_search_category,
                                              **txtFldBorderColorStyle
                                              )

        # buttons
        self.buttonSearch = ft.IconButton(icon=ft.icons.SEARCH, disabled=True, tooltip='Localizar Categoria', on_click=self.on_click_button_search_category)
        self.buttonAdd = ft.IconButton(icon=ft.icons.ADD, disabled=True, tooltip='Inserir Categoria', on_click=self.on_click_button_add_category)
        self.buttonSave = ft.IconButton(icon=ft.icons.SAVE, disabled=True, tooltip='Salvar Categoria', visible=False, on_click=self.on_click_button_save_category)
        self.buttonCancel = ft.IconButton(icon=ft.icons.CANCEL, tooltip='Cancelar Alteração', visible=False, on_click=self.on_click_button_cancel)
        self.buttonRefresh = ft.IconButton(icon=ft.icons.REFRESH, disabled=True, tooltip='Selecionar todas Categorias.', on_click=self.refresh)
        self.buttonClose = ft.IconButton(icon=ft.icons.EXIT_TO_APP, tooltip='Sair', on_click=self.on_click_button_close)

        # row display controls
        rowActions = ft.Container(ft.Row([self.txtFldDescription, self.buttonSearch, self.buttonAdd, self.buttonSave, self.buttonCancel, self.buttonRefresh, self.buttonClose], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                          padding=10,
                                          **cntStyle)

        # column show description category
        self.colCategory = ft.Column(height=300, scroll=ft.ScrollMode.ALWAYS)
        self.cntColDescription = ft.Container(self.colCategory, **cntStyle)

        # set values from table category
        self.set_values_category()

        # all controls
        cntAllControls = ft.Container(ft.Column([rowActions, self.cntColDescription], tight=True), width=640, padding=10)
        
        # bottom sheet
        self.bottomSheet = ft.BottomSheet(cntAllControls, open=True)
        self.page.overlay.append(self.bottomSheet)
        self.page.update()


    # refresh data category
    def refresh(self, e):
        self.buttonRefresh.disabled=True
        self.set_values_category()


    # set values category
    def set_values_category(self, values=None):

        # clear controls colCategory
        self.colCategory.controls.clear()

        # select all recno from table category
        if values: category = values
        else: category = self.select_all_from_category()

        #
        for idx, cat in enumerate(category):
            self.set_controls_row_category(idx, cat)


    # set controls row category
    def set_controls_row_category(self, index, category):

        # controls
        if category['ativo']:
            flagDisabled=False
            switchActive = ft.Switch(label='Ativo', data=index, width=100, value=True, on_change=self.on_change_switch_active)
        else:
            flagDisabled=True
            switchActive = ft.Switch(label='Inativo', data=index, width=100, value=False, label_position=ft.LabelPosition.LEFT, on_change=self.on_change_switch_active)

        #
        iconEdit = ft.IconButton(icon=ft.icons.EDIT, data=index, disabled=flagDisabled, on_click=self.on_click_button_edit_category)
        txtBtnIdCategory = ft.TextButton(f"{category['id']:4}", data=index, disabled=flagDisabled, on_click=self.on_click_text_button_description)
        txtBtnDescription = ft.TextButton(category['descricao'], data=index, disabled=flagDisabled, on_click=self.on_click_text_button_description)

        # rowCellCateg 
        rowCategory = ft.Row([switchActive, iconEdit, txtBtnIdCategory, txtBtnDescription], spacing=0)
        self.colCategory.controls.append(rowCategory)

        #
        self.page.update()


    # on change switch active
    def on_change_switch_active(self, e):
        
        # control index
        index = e.control.data

        # control
        switch = e.control

        # if True
        if switch.value:
            
            # change switch
            switch.label = 'Ativo'
            switch.label_position = ft.LabelPosition.RIGHT

            # enable controls
            self.colCategory.controls[index].controls[ICON_EDIT].disabled=False
            self.colCategory.controls[index].controls[DESCRIPTION].disabled=False
            self.colCategory.controls[index].controls[ID_CATEGORY].disabled=False
            self.update_active_category(self.colCategory.controls[index].controls[ID_CATEGORY].text, True)

        # if False
        else:

            # change switch
            switch.label = 'Inativo'
            switch.label_position = ft.LabelPosition.LEFT

            # disable controls
            self.colCategory.controls[index].controls[ICON_EDIT].disabled=True
            self.colCategory.controls[index].controls[DESCRIPTION].disabled=True
            self.colCategory.controls[index].controls[ID_CATEGORY].disabled=True
            self.update_active_category(self.colCategory.controls[index].controls[ID_CATEGORY].text, False)
        #
        self.page.update()


    # on_click_button_search_category
    def on_click_button_search_category(self, e):
        
        # enable button refresh category
        self.buttonRefresh.disabled=False

        # select all description where like
        allDescription = self.select_all_from_category_like_description(self.txtFldDescription.value.lower())

        if allDescription:
            self.set_values_category(allDescription)
            self.page.update()


    # on click button add category
    def on_click_button_add_category(self, e):

        #
        idCategory = self.insert_into_category(self.txtFldDescription.value)
        description = self.txtFldDescription.value
        index = len(self.colCategory.controls)
        self.set_controls_row_category(index, {'id':idCategory, 'descricao':description, 'ativo':True})
        self.txtFldDescription.value = ""
        self.buttonAdd.disabled=True
        self.page.update()


    # on click button save
    def on_click_button_save_category(self, e):

        # config control
        self.txtFldDescription.bgcolor = "#e8eff7"
        self.txtFldDescription.color = ft.TextStyle(color=ft.colors.BLACK)
        self.txtFldDescription.border = ft.colors.BLUE_800
        
        # config buttons
        self.buttonAdd.visible=True
        self.buttonSearch.visible=True
        self.buttonSave.visible=False
        self.buttonSave.disabled=True
        self.buttonCancel.visible=False
        self.colCategory.disabled = False

        # update description in table category
        idCategory = self.colCategory.controls[self.indexEditCategory].controls[ID_CATEGORY].text
        description = self.txtFldDescription.value
        self.update_description_category(idCategory, description)

        # change control description category
        self.colCategory.controls[self.indexEditCategory].controls[DESCRIPTION].text = self.txtFldDescription.value
        self.txtFldDescription.value = ""
        self.txtFldDescription.focus()

        # 
        self.page.update()


    # on click button cancel
    def on_click_button_cancel(self, e):

        # config control
        self.txtFldDescription.bgcolor = "#e8eff7"
        self.txtFldDescription.color = ft.TextStyle(color=ft.colors.BLACK)
        self.txtFldDescription.border = ft.colors.BLUE_800
        self.txtFldDescription.value = ""
        self.txtFldDescription.focus()

        # config buttons
        self.buttonAdd.visible=True
        self.buttonSearch.visible=True
        self.buttonSave.visible=False
        self.buttonCancel.visible=False
        self.colCategory.disabled=False

        #
        self.page.update()        


    # on click button edit category
    def on_click_button_edit_category(self, e):

        # control index
        index = e.control.data

        # set index global used
        self.indexEditCategory = index

        # set value in text field description
        self.txtFldDescription.bgcolor = ft.colors.BLUE_800
        self.txtFldDescription.color = ft.TextStyle(color=ft.colors.WHITE)
        self.txtFldDescription.border = ft.colors.TRANSPARENT
        self.txtFldDescription.value = self.colCategory.controls[index].controls[DESCRIPTION].text
        self.txtFldDescription.focus()

        # config buttons
        self.buttonAdd.visible=False
        self.buttonSearch.visible=False
        self.buttonSave.visible=True
        self.buttonCancel.visible=True
        self.colCategory.disabled=True

        #
        self.page.update()        


    # on click text button description
    def on_click_text_button_description(self, e):
        
        # control index
        index = e.control.data

        # set description in control
        self.main.txtFldCategoryDescription.value = self.colCategory.controls[index].controls[DESCRIPTION].text
        self.main.idCategory = self.colCategory.controls[index].controls[ID_CATEGORY].text

        # close bottom sheet
        self.bottomSheet.open=False
        self.page.update()


    # on change text field category
    def on_change_text_field_description_category(self, e):

        # if not value is control
        if not self.txtFldDescription.value:
            self.txtFldDescription.suffix_text=""
            self.buttonAdd.disabled=True
            self.buttonSave.disabled=True
            self.buttonSearch.disabled=True
            self.page.update()
            return None

        # enabled button search category
        self.buttonSearch.disabled=False

        # set fonte size in suffix text
        self.txtFldDescription.suffix_style = ft.TextStyle(size=9, weight='bold')
        
        # if was exist this category
        idCategory = self.select_description_from_category(self.txtFldDescription.value.lower())
        
        #
        if idCategory:
            self.txtFldDescription.suffix_text = "JÁ CADASTRADA."
            self.buttonAdd.disabled=True
            self.buttonSave.disabled=True
        #
        else:
            self.buttonAdd.disabled=False
            self.buttonSave.disabled=False

            #
            allDescription = self.select_all_from_category_like_description(self.txtFldDescription.value.lower())
            if allDescription:
                
                if len(allDescription) == 1:
                    self.txtFldDescription.suffix_text = f"{len(allDescription)} OCORRÊNCIA."
                else:
                    self.txtFldDescription.suffix_text = f"{len(allDescription)} OCORRÊNCIAS."

            else:
                self.txtFldDescription.suffix_text = "NENHUMA OCORRÊNCIA."
                self.buttonSearch.disabled=True

        #
        self.page.update()


    # on click button close
    def on_click_button_close(self, e):
        self.bottomSheet.open=False
        self.bottomSheet.update()



class Sell(HeaderApp, CrudSell):

    def __init__(self, main):
        HeaderApp.__init__(self, main)
        self.page = main.page
        self.main = main
        
        # rows
        self.row_header = ft.Row([self.cntHeaderMaster])
        self.row_body = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.row_footer = ft.Row()

        # column master
        self.colMaster = ft.Column([self.row_header, self.row_body, self.row_footer])


    def get(self):
        return self.colMaster
    
    
    # show controls
    def show(self):
        self.set_data_table_product()
        self.set_form_product()
        self.refresh()


    # clear items in page sell
    def clear(self):
        self.row_body.controls.clear()
        self.row_footer.controls.clear()
        self.page.update()


    # refresh page
    def refresh(self, descriptionProduct=None):
        self.clear()
        self.set_values_data_table_product()
        self.row_body.controls.append(self.cntDataTableProduct)
        self.page.update()


    # set data table product
    def set_data_table_product(self):

        # title for card data table produto
        txtTitle = ft.Text("Produtos", **txtTitleLargeStyle)

        # search product
        iconRefreshDataTableProduct  = ft.IconButton(icon=ft.icons.REFRESH, tooltip="Todos Produtos", icon_color=ft.colors.BLUE_500, on_click=self.on_click_button_refresh_data_table_product) 
        iconSearchProduct = ft.IconButton(icon=ft.icons.SEARCH, tooltip="Localizar Produto", on_click=self.on_click_button_search_product)
        self.searchProduct = ft.TextField(label="Descrição do Produto", height=40, autofocus=True, on_submit=self.on_click_button_search_product, **txtFldBorderColorStyle)

        # data column
        self.colActions = ft.DataColumn(ft.Text("Ações", **txtColorStyle))
        self.colId = ft.DataColumn(ft.Text("ID", **txtColorStyle))
        self.colDescription = ft.DataColumn(ft.Text("Descrição", **txtColorStyle))
        self.qtde = ft.DataColumn(ft.Text('Qtde', **txtColorStyle))
        self.colUnit = ft.DataColumn(ft.Text("Unidade", **txtColorStyle))
        self.colPrice = ft.DataColumn(ft.Text("Preço", **txtColorStyle), numeric=True)
        self.colCategoryDescription = ft.DataColumn(ft.Text("Categoria", **txtColorStyle))
        self.colCondition = ft.DataColumn(ft.Text('Condição', **txtColorStyle))
        self.colSituation = ft.DataColumn(ft.Text('Situação', **txtColorStyle))
        self.colObservation = ft.DataColumn(ft.Text("Observação", **txtColorStyle))

        # data table
        self.dtProduct = ft.DataTable()
        self.dtProduct.columns = ([self.colActions, self.colId, self.colDescription, self.colSituation, self.qtde, self.colUnit,
                                    self.colPrice, self.colCategoryDescription, self.colCondition, self.colObservation])
        self.dtProduct.border_radius = 2
        self.dtProduct.border = ft.border.all(1, color=ft.colors.BLUE_900)
        self.dtProduct.vertical_lines=ft.border.BorderSide(1, color=ft.colors.BLUE_900)
        self.dtProduct.horizontal_lines=ft.border.BorderSide(1, color=ft.colors.BLUE_900)
        self.dtProduct.heading_row_height = 25
        self.dtProduct.data_row_max_height = 35

        # buttons card data table
        self.btnInsert = ft.ElevatedButton(text="Incluir Product", on_click=self.on_click_button_insert_product)

        # row
        row0 = ft.Row([txtTitle])
        row1 = ft.Row([self.searchProduct, iconSearchProduct])
        row2 = ft.Row([self.dtProduct], scroll=ft.ScrollMode.ALWAYS, width=1580) 
        row3 = ft.Row([iconRefreshDataTableProduct, self.btnInsert], alignment=ft.MainAxisAlignment.END)

        # col 
        colDataTable = ft.Column([row0, row1, ft.Column([row2], height=700, scroll=ft.ScrollMode.AUTO), row3])

        # container card data table
        self.cntDataTableProduct = ft.Container(colDataTable, padding=10, **cntStyle)


    # set values data table product
    def set_values_data_table_product(self, descriptionProduct=None):
        
        if descriptionProduct:
            allProducts = self.select_product_from_view_product(self.main.env.idClient, descriptionProduct)
        else:
            # get all products
            allProducts = self.select_all_product_from_view_product(self.main.env.idClient)

        # clear data in dataTable Produto
        self.dtProduct.rows.clear()


        # insert values in dataTable Produto
        for product in allProducts:

            # change color if not Active
            colorDescription = None
            if product['situacao'] != 'Ativo':
                colorDescription = ft.colors.RED_800


            # change color if qtty = 0
            colorQtty = None
            if product['qtde'] == 0:
                colorQtty = ft.colors.RED_800

            # set values
            self.dtProduct.rows.append( ft.DataRow(
                                            cells=[
                                                ft.DataCell(
                                                ft.Row([
                                                        ft.IconButton(icon="edit", data=product, tooltip="Alterar Produto", on_click=self.on_click_icon_edit_product),
                                                        ft.IconButton(icon="delete", data=product, tooltip="Excluir Produto", on_click=self.on_click_button_delete_product),
                                                ])),
                                                ft.DataCell(ft.Text(product["id"])),
                                                ft.DataCell(ft.Text(product["descricao"])),
                                                ft.DataCell(ft.Text(product["situacao"], color=colorDescription)),
                                                ft.DataCell(ft.Text(product["qtde"], color=colorQtty)),
                                                ft.DataCell(ft.Text(product["unidade"])),
                                                ft.DataCell(ft.Text(f'R$ {product["preco"]:>10.2f}'.replace('.', ','), width=120)),
                                                ft.DataCell(ft.Text(product["descricao_categoria"])),
                                                ft.DataCell(ft.Text(product["condicao"])),
                                                ft.DataCell(ft.Text(product["observacao"])),                                                
                                            ]))

        # page update
        self.page.update()


    # form product
    def set_form_product(self):

        # primary key
        self.id = None
        self.idCategory = None

        # default title
        self.formTitle = ft.Text('Incluir Produto', **txtTitleLargeStyle)

        # active product
        self.active = ft.Switch(label="Ativo", value=True, label_position=ft.LabelPosition.LEFT, on_change=self.on_change_switch_active)

        # description
        self.description = ft.TextField(label="Descrição", width=880, autofocus=True, **txtFldBorderColorStyle)

        # quantity
        self.qtty = ft.TextField(label='Quantidade', width=120, input_filter=ft.NumbersOnlyInputFilter(), **txtFldBorderColorStyle)

        # unit
        unitOption=[
                ft.dropdown.Option("UNI"),
                ft.dropdown.Option("CXA"),
                ft.dropdown.Option("FDO")]
        self.unit = ft.Dropdown(label="Unidade", width=120, border_color=ft.colors.BLUE_800)
        self.unit.options = unitOption

        # price
        self.price = ft.TextField(label="Preço",
                                  width=160,
                                  prefix_text="R$ ",
                                  input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9,]", replacement_string=""),
                                  **txtFldBorderColorStyle)

        # description category
        self.txtFldCategoryDescription = ft.TextField(label='Categoria',
                                                      width=300,
                                                      on_change=self.on_change_text_field_category_description,
                                                      **txtFldBorderColorStyle)
        
        self.colShowCategoryDescription = ft.Column(height=100, width=300, scroll=ft.ScrollMode.ALWAYS)
        self.cntColShowCategoryDescription = ft.Container(self.colShowCategoryDescription, visible=False, **cntStyle)
        self.colShowCategDescrip = ft.Column([self.txtFldCategoryDescription, self.cntColShowCategoryDescription], spacing=0)

        # button add category
        self.buttonSearch = ft.IconButton(icon=ft.icons.SEARCH, tooltip='Localizar Categoria', on_click=self.on_click_button_search_category)

        # condition
        conditionOption=[
                ft.dropdown.Option("Novo"),
                ft.dropdown.Option("Usado")]
        self.condition = ft.Dropdown(label="Condição", width=150, border_color=ft.colors.BLUE_800)
        self.condition.options = conditionOption

        # observation
        self.observation = ft.TextField(label="Observação", width=790, **txtFldBorderColorStyle)

        # Features product
        self.featuresProduct = ft.TextField(label='Características', width=1320, height=420, border='None', multiline=True, max_lines=30)

        # buttons form product
        self.btnSave = ft.ElevatedButton(text="Salvar", on_click=self.on_click_button_save_product)
        self.btnCloseFormProduct = ft.ElevatedButton(text="Fechar", on_click=self.on_click_button_close_form_product)

        # form product required fields
        self.requiredFieldsFormProduct={}
        self.requiredFieldsFormProduct['Campo Descrição deve ser informado!'] = self.description
        self.requiredFieldsFormProduct['Campo Quantidade deve ser informado!'] = self.qtty
        self.requiredFieldsFormProduct['Campo Unidade deve ser informado!'] = self.unit
        self.requiredFieldsFormProduct['Campo Preço deve ser informado!'] = self.price
        self.requiredFieldsFormProduct['Campo Categoria deve ser informado!'] = self.txtFldCategoryDescription
        self.requiredFieldsFormProduct['Campo Condição deve ser informado!'] = self.condition
        self.requiredFieldsFormProduct['Campo Características deve ser informado!'] = self.featuresProduct

        # select icon image_add
        imageAdd = self.select_image_add_from_app()

        # image 0 (default)
        self.imageAdd = ft.Image(src_base64=imageAdd, tooltip='Inserir Foto')
        self.cntImageAdd = ft.Container(self.imageAdd, on_click=self.on_click_container_image)
        self.txtFldCounter = ft.Text('Foto: 0/6', **txtLabelSmallStyle)
        self.txtFldPath = ft.TextField(label='Diretório',
                                       width=500,
                                       prefix_icon=ft.icons.DRIVE_FOLDER_UPLOAD_SHARP,
                                       hint_text='Informe o diretório das fotos',
                                       **txtFldBorderColorStyle)

        # rows form product
        row0 = ft.Row([self.formTitle, ft.Container(width=1040), self.active])
        row1 = ft.Row([self.description, self.qtty, self.unit, self.price])
        row2 = ft.Row([self.colShowCategDescrip, self.buttonSearch, self.condition, self.observation])
        self.cntImagePath = ft.Container(ft.Column([self.cntImageAdd, self.txtFldCounter, self.txtFldPath], horizontal_alignment=ft.CrossAxisAlignment.CENTER), padding=10)
        self.rowImage = ft.Row([self.cntImagePath])
        row4 = ft.Row([self.featuresProduct])
        row5 = ft.Row([self.btnSave, self.btnCloseFormProduct])

        # container image
        cntImage = ft.Container(self.rowImage, width=1310, **cntStyle)

        # col
        colFormProduct = ft.Column([row0, row1, row2, cntImage, row4, row5])

        # container input card
        self.cntFormProduct = ft.Container(colFormProduct, padding=ft.padding.only(left=10, bottom=10), **cntStyle)       


    # clear form product
    def clear_form_product(self):
        self.id = None
        self.idCategory = None
        self.description.value = ''
        self.qtty.value = ''
        self.unit.value = ''
        self.price.value =  ''
        self.txtFldCategoryDescription.value = ''
        self.condition.value = ''
        self.observation.value = ''
        self.featuresProduct.value = ''
        self.txtFldCounter.value = 'Foto: 0/6'
        self.txtFldPath.value = ''
        self.rowImage.controls.clear()
        self.rowImage.controls.append(self.cntImagePath)


    # on change switch active
    def on_change_switch_active(self, e):

        #
        if e.control.value == True:
            e.control.label = 'Ativo'
            e.control.label_position = ft.LabelPosition.LEFT
        else:
            e.control.label = 'Pausado'
            e.control.label_position = ft.LabelPosition.RIGHT
        e.control.update()


    # on_change_text_field_category
    def on_change_text_field_category_description(self, e):

        if not self.txtFldCategoryDescription.value:
            self.colShowCategoryDescription.controls.clear()
            self.cntColShowCategoryDescription.visible=False
            self.page.update()
            return None

        allDescription = self.select_all_from_category_like_description(self.txtFldCategoryDescription.value.lower())
        if allDescription:

            # show description category
            self.set_description_category_in_row(allDescription)

    
    # set description category in row
    def set_description_category_in_row(self, allDescription):

        # clear column description category
        self.colShowCategoryDescription.controls.clear()

        # iter 
        for cat in allDescription:
            self.colShowCategoryDescription.controls.append(ft.TextButton(cat['descricao'],
                                                                          data=cat['id'],
                                                                          on_click=self.on_click_text_button_category_description))

        #
        self.cntColShowCategoryDescription.visible=True
        self.page.update()


    # on_click_text_button_category_description
    def on_click_text_button_category_description(self, e):

        # set value in text field category
        self.idCategory = e.control.data
        self.txtFldCategoryDescription.value = e.control.text
        self.colShowCategoryDescription.controls.clear()
        self.cntColShowCategoryDescription.visible=False
        self.page.update()


    # on click button search product
    def on_click_button_search_product(self, e):
        self.set_values_data_table_product(self.searchProduct.value)


    # on click button refresh data table product
    def on_click_button_refresh_data_table_product(self, e):
        
        # clear data in dataTable Produto
        self.dtProduct.rows.clear()
        self.set_values_data_table_product()


    # on click button insert product
    def on_click_button_insert_product(self, e):
        self.flagDataset= 'Insert'
        self.formTitle.value = 'Incluir Produto'
        self.row_body.controls.clear()
        self.row_body.controls.append(self.cntFormProduct)
        self.page.update()


    # on click icon edit product
    def on_click_icon_edit_product(self, e):
        self.flagDataset = 'Edit'
        self.formTitle.value = 'Alterar Produto'

        #
        self.idProduct = e.control.data['id']
        self.idCategory = e.control.data['id_categoria']
        product= e.control.data

        # switch active
        if product['situacao'] == 'Ativo':
            self.active.value = True
            self.active.label = 'Ativo'
            self.active.label_position = ft.LabelPosition.LEFT

        elif product['situacao'] == 'Pausado':
            self.active.value = False
            self.active.label = 'Pausado'
            self.active.label_position = ft.LabelPosition.RIGHT

        #
        self.description.value = product['descricao']
        self.qtty.value = product['qtde']
        self.unit.value = product['unidade']
        self.price.value =  str(product['preco']).replace('.', ',')
        self.txtFldCategoryDescription.value = product['descricao_categoria']
        self.condition.value = product['condicao']
        self.observation.value = product['observacao']
        cntImage = self.set_container_image('default_image', product['imagem'])
        self.rowImage.controls.append(cntImage)        

        # set images
        images = ['imagem_0', 'imagem_1', 'imagem_2', 'imagem_3', 'imagem_4']
        for img in images:
            cntImage = self.set_container_image(img, product[img])
            if not cntImage:
                continue
            self.rowImage.controls.append(cntImage)

        # description product
        self.featuresProduct.value = product['produto_descricao']

        # qtty images
        self.qttyImage = len(self.rowImage.controls)-1
        self.txtFldCounter.value = f'Foto: {self.qttyImage}/6'
        
        #
        self.row_body.controls.clear()
        self.row_body.controls.append(self.cntFormProduct)
        self.page.update()

    
    # on click button delete product
    def on_click_button_delete_product(self, e):
        idProduct = e.control.data['id']
        description = e.control.data['descricao']

        # message confirmatio delete product
        message = MessageConfirm(self.page, 'Excluir Produto', f'Deseja excluir produto: {description}?')

        while message.dialogResponse == None:
            if message.dialogResponse == False:
                return False

        self.update_situation_product_from_product(idProduct)
        self.main.home.refresh()
        self.main.cart.refresh()
        self.main.favorite.refresh()
        self.refresh()

    
    # on click button add category
    def on_click_button_search_category(self, e):
        getCategory = GetCategory(self)


    # on click container image
    def on_click_container_image(self, e):
        
        # if not directory
        if not self.txtFldPath.value:
            show_snack_bar_warning(self.page, 'Diretório onde as fotos estão deve ser informado!')
            return

        # container image selected
        self.containerImageSelected = e.control.data

        # select image
        self.pickerImageName = ft.FilePicker(on_result=self.dialog_picker)
        self.page.overlay.append(self.pickerImageName)
        self.page.update()
        self.pickerImageName.pick_files(file_type=ft.FilePickerFileType.IMAGE, allow_multiple=True, initial_directory=self.txtFldPath.value)


    # dialog picker
    def dialog_picker(self, e: ft.FilePickerResultEvent):
        
        # not choice
        if not e.files:
            return None

        # verify qtty image selected
        if len(e.files) >= 7:
            show_snack_bar_warning(self.page, 'Permitido somente 6 fotos!')
            return None

        # iter files selected
        for file in e.files:

            # test directory exist
            try:

                # load image
                imageBase64 = convert_image_base64(self.txtFldPath.value + '\\' + file.name)

            except:
                show_snack_bar_warning(self.page, 'Diretório ou Arquivo inválido!')
                return None

            # container image
            cntImage = self.set_container_image(file.name, imageBase64)
            if not cntImage:
                return None

            # set image and total
            self.rowImage.controls.append(cntImage)
            self.qttyImage = len(self.rowImage.controls)-1
            self.txtFldCounter.value = f'Foto: {self.qttyImage}/6'
            self.page.update()

            # test qtty image
            if len(self.rowImage.controls) >= 7:
                self.cntImageAdd.disabled=True
                self.page.update()
                return None


    # set container image
    def set_container_image(self, fileName, imageBase64):

        # for edit product
        if not imageBase64:
            return None

        # if image exist
        for cntImg in self.rowImage.controls:
            if fileName == cntImg.data:
                show_snack_bar_warning(self.page, 'Foto já foi selecionada!')
                return None

        # set image in page
        txtBtnRemoveImage = ft.TextButton('Remover', data=fileName, icon=ft.icons.DELETE_FOREVER, icon_color=ft.colors.RED_800, on_click=self.on_click_button_remove_image)
        image = ft.Image(src_base64=imageBase64, width=100, height=130, tooltip=fileName)
        colImage = ft.Column([image, txtBtnRemoveImage], spacing=0)
        cntImage = ft.Container(colImage,
                                data=fileName,
                                margin=ft.margin.only(top=10, bottom=10),
                                padding=0,
                                **cntStyle)

        # 
        return cntImage


    # verify required fields
    def verify_required_fields(self):
        
        # verify required fields
        for input in self.requiredFieldsFormProduct:
            if not self.requiredFieldsFormProduct[input].value:
                show_snack_bar_warning(self.page, input)
                self.requiredFieldsFormProduct[input].focus()
                return None


        # verify category typed
        idCategory = self.select_description_from_category(self.txtFldCategoryDescription.value.lower())
        if not idCategory:
            show_snack_bar_warning(self.page, 'Categoria não cadastrada!')
            self.txtFldCategoryDescription.focus()
            return None

        
        # verify insert image
        if len(self.rowImage.controls) < 2:
                show_snack_bar_warning(self.page, 'Selecione uma (1) imagem pelo menos!')
                self.txtFldPath.focus()
                return None

        # if all controls True
        return True


    # save insert product
    def save_insert_product(self):

        # 
        if not self.verify_required_fields():
            return None

        # switch active
        situation='Ativo'
        if not self.active.value:
            situation='Pausado'

        # insert values in table product
        idProduct = self.insert_product_into_product(
                                         self.main.env.idClient,
                                         self.description.value,
                                         self.qtty.value,
                                         self.unit.value,
                                         self.price.value.replace(',', '.'),
                                         self.rowImage.controls[1].content.controls[0].src_base64,
                                         self.idCategory,
                                         situation,
                                         self.condition.value,
                                         self.observation.value
                                         )

        # number images
        seq=0
        images=[None, None, None, None, None]
        for img in range(2, len(self.rowImage.controls)):
            images[seq] = (self.rowImage.controls[img].content.controls[0].src_base64)
            seq+=1
        
        # insert into product_description
        self.insert_product_into_product_description(idProduct, self.featuresProduct.value, images[0], images[1], images[2], images[3], images[4])

        # clear form product
        self.clear_form_product()
        
        # set container data table product
        self.row_body.controls.clear()
        self.main.home.refresh()
        self.refresh()
        self.page.update()


    # save edit product
    def save_edit_product(self):

        # 
        if not self.verify_required_fields():
            return None

        # switch active
        if self.active.value:
            situation='Ativo'
        else:
            situation='Pausado'

        # change currency price
        price = self.price.value.replace(',', '.')

        # insert values in table product
        self.update_product(
                        self.idProduct,
                        self.description.value,
                        self.qtty.value,
                        self.unit.value,
                        price,
                        self.rowImage.controls[1].content.controls[0].src_base64,
                        self.idCategory,
                        self.condition.value,
                        situation,
                        self.observation.value
        )

        # number images
        seq=0
        images=[None, None, None, None, None]
        for img in range(2, len(self.rowImage.controls)):
            images[seq] = (self.rowImage.controls[img].content.controls[0].src_base64)
            seq+=1
        
        # verify se product exist in table product description
        productDescription = self.select_product_description(self.idProduct)

        #
        if not productDescription:
            self.insert_product_into_product_description(self.idProduct, self.featuresProduct.value, images[0], images[1], images[2], images[3], images[4])
        else:
            # update product_description
            self.update_description_product(self.idProduct, self.featuresProduct.value, images[0], images[1], images[2], images[3], images[4])

        # clear form product
        self.clear_form_product()
        
        # refresh pages
        self.row_body.controls.clear()
        self.main.favorite.refresh()
        self.main.cart.refresh()
        self.main.home.refresh()
        self.refresh()
        self.page.update()


    # on click button revome image
    def on_click_button_remove_image(self, e):
        
        # index da image
        imageName = e.control.data

        # iter cntImage in rowImage
        for cnt in self.rowImage.controls:
            if cnt.data == imageName:
                self.rowImage.controls.remove(cnt)
                self.page.update()
  
        # set text field qtty image
        self.qttyImage = len(self.rowImage.controls)-1
        self.txtFldCounter.value = f'Foto: {self.qttyImage}/6'
        self.cntImageAdd.disabled=False

        #
        self.page.update()


    # on click button save product
    def on_click_button_save_product(self, e):
        
        # if insert product
        if self.flagDataset == 'Insert':
            self.save_insert_product()
        
        # if edit product
        elif self.flagDataset == 'Edit':
            self.save_edit_product()


    # on click button close form product
    def on_click_button_close_form_product(self, e):
        self.clear_form_product()
        self.row_body.controls.clear()
        self.row_body.controls.append(self.cntDataTableProduct)
        self.page.update()