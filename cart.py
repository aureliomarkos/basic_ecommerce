import flet as ft

# app
from utils import Message, MessageConfirm, cntStyle, txtColorStyle, txtTitleMediumStyle, txtTitleSmallStyle
from header_app import HeaderApp
from sql_utils import db



class CrudCart:
    
    # select all product
    def select_all_from_view_cart(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT * FROM view_carrinho WHERE id_cliente=?", (idClient, ))
        all = cursor.fetchall()
        conn.close()
        return all


    # select from view cart
    def select_from_view_cart_where_prod_selec(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT * FROM view_carrinho WHERE id_cliente=? AND prod_selec='True'", (idClient, ))
        all = cursor.fetchall()
        conn.close()
        return all


    # select qtty product from product
    def select_qtty_situation_from_product(self, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT qtde, situacao FROM produto WHERE id=?", (idProduct, ))
        result = cursor.fetchall()
        conn.close()
        return result


    # delete product cart
    def delete_product_from_cart(self, idProduct):
        conn, cursor = db()
        cursor.execute("DELETE FROM carrinho WHERE id=?", (idProduct,))
        conn.commit()
        conn.close()


    # delete all product cart
    def delete_all_from_cart(self):
        conn, cursor = db()
        cursor.execute("DELETE FROM carrinho")
        conn.commit()
        conn.close()


    # update all products cart
    def update_all_prod_selec_cart(self, boolValue):
        conn, cursor = db()
        cursor.execute("UPDATE carrinho SET prod_selec=?", (boolValue,))
        conn.commit()
        conn.close()


    # update field qtde in cart
    def update_qtty_cart(self, idCart, qtde):
        conn, cursor = db()
        cursor.execute("UPDATE carrinho SET qtde=? WHERE id=? ", (qtde, idCart))
        conn.commit()
        conn.close()

    
    # update field prod_select cart
    def update_prod_selec_cart(self, idCart, boolValue):
        conn, cursor = db()
        cursor.execute("UPDATE carrinho SET prod_selec=? WHERE id=?", (boolValue, idCart))
        conn.commit()
        conn.close()


    # select values for page footer
    def select_values_page_footer(self, idClient):

        # total items
        conn, cursor = db()
        cursor.execute("SELECT COUNT(*) AS total_items FROM carrinho WHERE id_cliente=?", (idClient,))
        total_items = cursor.fetchone()[0]
        conn.close()

        # total selected
        conn, cursor = db()
        cursor.execute("SELECT COUNT(*) AS total_selected FROM carrinho WHERE prod_selec='True' AND id_cliente=?", (idClient,))
        total_selected = cursor.fetchone()[0]
        conn.close()

        # qtty
        conn, cursor = db()
        cursor.execute("SELECT SUM(qtde) AS qtde FROM carrinho WHERE prod_selec='True' AND id_cliente=?", (idClient,))
        qtty = cursor.fetchone()[0]
        conn.close()

        # total price
        conn, cursor = db()
        cursor.execute("SELECT SUM(qtde * preco) AS total_price FROM view_carrinho WHERE prod_selec='True' AND id_cliente=?", (idClient,))
        total_price = cursor.fetchone()[0]
        conn.close()

        # values page footer cart
        values = {
            'total_items':total_items,
            'total_selected':total_selected,
            'qtty':qtty,
            'total_price':total_price
            }
        return values
    


class Cart(HeaderApp, CrudCart):

    def __init__(self, main):
        HeaderApp.__init__(self, main)
        self.page = main.page
        self.main = main

        # rows
        self.row_header = ft.Row([self.cntHeaderMaster])
        self.row_body = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.row_footer = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # set page header cart
        self.set_page_header_cart()

        # column master
        self.colMaster = ft.Column([self.row_header, self.row_body, self.row_footer])
    
    # get colMaster
    def get(self):
        return self.colMaster


    # show page
    def show(self):
        self.refresh()


    # clear items in page cart
    def clear(self):
        self.row_body.controls.clear()
        self.row_footer.controls.clear()
        self.page.update()


    # refresh cart
    def refresh(self):
        self.set_page_body_cart()
        self.set_page_footer_cart()


    #  page header cart
    def set_page_header_cart(self):
        
        
        # icon button select all products
        iconBtnAllProduct = ft.IconButton(icon=ft.icons.CHECK_BOX_OUTLINE_BLANK_ROUNDED, selected=False, selected_icon=ft.icons.CHECK_BOX_ROUNDED, on_click=self.on_click_icon_button_select_all_product)
        txtAllProduct = ft.Text('Selecionar Todos os produtos', **txtColorStyle)
        rowIconBtnAllProduct = ft.Row([iconBtnAllProduct, txtAllProduct], spacing=0)

        # icon button remove all products
        iconBtnRemoveAllProduct = ft.IconButton(icon=ft.icons.DELETE_FOREVER, on_click=self.on_click_icon_button_remove_all_product, icon_color=ft.colors.RED_800)
        txtRemoveAllProduct = ft.Text('Remover todos Produtos', **txtColorStyle)
        rowIconBtnRemoveAllProduct = ft.Row([iconBtnRemoveAllProduct, txtRemoveAllProduct], spacing=0)

        # icon button checkout
        self.iconBtnCheckout = ft.IconButton(icon=ft.icons.SHOPPING_CART_CHECKOUT, on_click=self.on_click_icon_button_checkout)
        txtCheckout = ft.Text("Checkout", **txtColorStyle)
        rowIconBtnCheckout = ft.Row([self.iconBtnCheckout, txtCheckout], spacing=0)

        # rows with icons
        rowHeader = ft.Row([rowIconBtnAllProduct, rowIconBtnRemoveAllProduct, rowIconBtnCheckout])
        self.cntRowHeader = ft.Container(content=rowHeader, padding=10, **cntStyle)

        # page update
        self.page.update()


    # set page body cart
    def set_page_body_cart(self):

        # column
        self.colProduto = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=720)

        # get all product for cart
        allCartProducts = self.select_all_from_view_cart(self.main.env.idClient)

        # if not exist product in cart
        if not allCartProducts:
            self.clear()
            return None

        # iter in products
        for cartProd in allCartProducts:

            # check box select product
            checkBoxSelectProduct = ft.Checkbox(tooltip="Selecionar Produto", data=cartProd, value=cartProd['prod_selec'], on_change=self.on_change_check_box_select_product)

            # icon button remove product
            iconRemoveProd = ft.IconButton(ft.icons.DELETE_FOREVER, data=cartProd, icon_color="red", tooltip="Excluir Produto", on_click=self.on_click_icon_remove_product)

            # image product
            imageProduct = ft.Image(width=60, height=60, src_base64=cartProd['imagem'])
            cntImageProduct = ft.Container(imageProduct, data=cartProd, on_click=self.on_click_image_product)

            # description product
            txtDescription = ft.Text(cartProd['descricao'], width=560, max_lines=3, **txtTitleMediumStyle)

            # qtde product
            txtQtty = ft.Text(cartProd['qtde'], **txtColorStyle)

            # increment
            iconBtnInc = ft.IconButton(ft.icons.ADD, icon_color=ft.colors.BLUE_800, data=[txtQtty, cartProd], on_click=self.on_click_icon_increment)

            # decrease
            iconBtnDec = ft.IconButton(ft.icons.REMOVE, icon_color=ft.colors.BLUE_800, data=[txtQtty, cartProd], on_click=self.on_click_icon_decrease)

            # container qtty
            rowIncDecQtty = ft.Row([iconBtnDec, txtQtty, iconBtnInc], spacing=0)

            # select qtty, situation from product
            result = self.select_qtty_situation_from_product(cartProd['id_produto'])[0]
            productQtty, productSituation = result['qtde'], result['situacao']

            # verify situation product
            if productSituation != 'Ativo':
                
                # change checkbox selected product
                checkBoxSelectProduct.value = False
                checkBoxSelectProduct.disabled=True
                self.update_prod_selec_cart(cartProd['id'], 'False')

                #
                txtMessage = ft.Text(f'Produto esta {cartProd['situacao']}.', color=ft.colors.RED_300, weight=ft.FontWeight.BOLD, width=200)
                cntIncDecQtty = ft.Container(txtMessage)

                # container Image product cart
                cntImageProduct.tooltip = f'Produto esta {cartProd['situacao']}.'
                cntImageProduct.disabled=True


            # if qtty == 0
            elif productQtty == 0:

                # change checkbox selected product
                checkBoxSelectProduct.value=False
                checkBoxSelectProduct.disabled=True
                self.update_prod_selec_cart(cartProd['id'], 'False')

                #
                txtMessage = ft.Text('Produto finalizado(qtde=0).', color=ft.colors.RED_300, weight=ft.FontWeight.BOLD, width=200)
                cntIncDecQtty = ft.Container(txtMessage)

                # container Image product Cart
                cntImageProduct.tooltip = 'Produto finalizado(qtde=0).'
                cntImageProduct.disabled=True

            # check qtty in stock
            elif productQtty < cartProd['qtde']:
                cntIncDecQtty = ft.Container(rowIncDecQtty, width=200)
                txtQtty.value = productQtty
                self.update_qtty_cart(cartProd['id'], productQtty)

            #
            else:
                cntIncDecQtty = ft.Container(rowIncDecQtty, width=200)

            # product price
            txtPrice = ft.Text(f'R$ {cartProd['preco']:>8.2f}'.replace('.', ','), width=100, **txtTitleMediumStyle)

            # column
            row = ft.Row([checkBoxSelectProduct, iconRemoveProd, cntImageProduct, txtDescription, cntIncDecQtty, txtPrice])
            cont = ft.Container(row, **cntStyle)

            # column
            self.colProduto.controls.append(cont)

        # set in row body
        self.row_body.controls = [ft.Column([self.cntRowHeader, self.colProduto], horizontal_alignment=ft.CrossAxisAlignment.CENTER)]

        # page update
        self.page.update()


    # page footer cart
    def set_page_footer_cart(self):

        # total items in cart
        txtTotItems = ft.Text('Total de Ítens:', **txtTitleSmallStyle)
        self.txtTotItems = ft.Text(**txtTitleSmallStyle)
        rowTotItems = ft.Row([txtTotItems, self.txtTotItems])

        # total items selected
        txtTotItemsSelected = ft.Text('Total Ítens Selecionados:', **txtTitleSmallStyle)
        self.txtTotItemsSelected = ft.Text(width=40, **txtTitleSmallStyle)
        rowTotItemsSelected = ft.Row([txtTotItemsSelected, self.txtTotItemsSelected])

        # total qtty
        txtQtty = ft.Text('Qtde:', **txtTitleSmallStyle)
        self.txtTotQtty = ft.Text(width=40, **txtTitleSmallStyle)
        rowTotQtty = ft.Row([txtQtty, self.txtTotQtty])

        # total price in cart
        txtTotPriceCart = ft.Text('Total:', **txtTitleSmallStyle)
        self.txtTotPriceCart = ft.Text(width=80, **txtTitleSmallStyle)
        rowTotPriceCart = ft.Row([txtTotPriceCart, self.txtTotPriceCart])

        # row Footer
        rowFooter = ft.Row([rowTotItems, rowTotItemsSelected, rowTotQtty, rowTotPriceCart], alignment=ft.MainAxisAlignment.CENTER, width=600)
        cntRowFooter = ft.Container(rowFooter, padding=10, **cntStyle)

        # set footer in page
        self.row_footer.controls = [cntRowFooter]

        # set values page footer
        self.set_values_page_footer()


    # set values page footer
    def set_values_page_footer(self):

        # select 
        values = self.select_values_page_footer(self.main.env.idClient)

        # if not items selected from cart
        if not values['total_selected']:
            self.iconBtnCheckout.disabled=True
        else:
            self.iconBtnCheckout.disabled=False

        # set values
        self.txtTotItems.value = values['total_items']
        self.txtTotItemsSelected.value = values['total_selected']

        # if qtde
        if values['qtty']:
            self.txtTotQtty.value = values['qtty']
        else:
            self.txtTotQtty.value = '0'
        
        # if price
        if values['total_price']:
            self.txtTotPriceCart.value = f"R$ {values['total_price']:>8.2f}".replace('.', ',')
        else:
            self.txtTotPriceCart.value = "R$ 0,00"
        self.page.update()


    # on click image product
    def on_click_image_product(self, e):
        idProduct = e.control.data['id_produto']
        self.main.prod_desc.set_product(idProduct)
        self.page.go('/product_description')


    # on click text button checkout
    def on_click_icon_button_checkout(self, e):

        # all product in cart
        allCartProdSelec = self.select_from_view_cart_where_prod_selec(self.main.env.idClient)
        
        #
        for cartProd in allCartProdSelec:
            
            # select qtty, situation of product
            result = self.select_qtty_situation_from_product(cartProd['id_produto'])[0]
            productQtty, productSituation = result['qtde'], result['situacao']
            
            # qtty = 0
            if not productQtty:
                Message(self.page, f'Produto: "{cartProd['descricao']}" finalizado, (qtde=0).')

                # refresh cart
                self.refresh()

                # refresh pages
                self.main.purchase.refresh()
                self.main.favorite.refresh()
                self.main.sell.refresh()
                self.main.home.refresh()
                return None

            # product paused or inactive
            elif productSituation != 'Ativo':
                Message(self.page, f'Produto: {cartProd['descricao']} "{productSituation}".')
                
                # refresh cart
                self.refresh()

                # refresh pages
                self.main.purchase.refresh()
                self.main.favorite.refresh()
                self.main.sell.refresh()
                self.main.home.refresh()
                return None

            # check product in stock
            elif productQtty < cartProd['qtde']:
                Message(self.page, f'Não tem essa qtde do produto: "{cartProd['descricao']}"')

                # refresh cart
                self.refresh()
                return None
   
        #
        self.main.checkout.refresh()
        self.page.update()
        self.page.go('/checkout')

    
    # on click button select all products
    def on_click_icon_button_select_all_product(self, e):

        #
        e.control.selected = not e.control.selected

        # 
        if e.control.selected == True:
            self.update_all_prod_selec_cart('True')
        else:
            self.update_all_prod_selec_cart('False')

        #
        self.refresh()
        self.set_values_page_footer()


    # on click button remove all product
    def on_click_icon_button_remove_all_product(self, e):

        # message remove all product
        message = MessageConfirm(self.page, "Excluir todos Produto", "Confirma Exclusão?")

        # wait response
        while message.dialogResponse == None:
            pass
        
        # if response False
        if message.dialogResponse == False:
            return None

        self.delete_all_from_cart()
        
        # clear page body
        self.row_body.controls = [ft.Row()]

        # clear values page footer
        self.set_values_page_footer()

        # refresh qtde items cart
        self.main.env.refresh_badge_cart()


    # on click Checkbox Select Product
    def on_change_check_box_select_product(self, e):
        idCart = e.control.data['id']

        # if selected
        if e.control.value == True:
            self.update_prod_selec_cart(idCart, 'True')
        else:
            self.update_prod_selec_cart(idCart, 'False')
        self.set_values_page_footer()


    # on click icon remove product
    def on_click_icon_remove_product(self, e):

        # message remove product
        message = MessageConfirm(self.page, "Excluir Produto", f"Confirma exclusão do produto: {e.control.data['descricao']}?")

        # wait response
        while message.dialogResponse == None:
            pass
        
        # if response yes
        if message.dialogResponse == False:
            return None

        # if message yes
        idCart = e.control.data['id']
        self.delete_product_from_cart(int(idCart))
        
        # refresh items in cart
        self.main.env.refresh_badge_cart()

        # refresh page
        self.refresh()


    # on click icon decrease
    def on_click_icon_decrease(self, e):

        #
        txtQtty = e.control.data[0]
        idCart = e.control.data[1]['id']
        idProduct = e.control.data[1]['id_produto']
        cartQtty = e.control.data[1]['qtde'] - 1
        
        # select qtty, situation of product
        result = self.select_qtty_situation_from_product(idProduct)[0]
        productQtty, productSituation = result['qtde'], result['situacao']

        # if not active
        if productSituation != 'Ativo':
            
            # refresh page
            self.refresh()

            # refresh pages
            self.main.purchase.refresh()
            self.main.favorite.refresh()
            self.main.sell.refresh()
            self.main.home.refresh()
            return None

        # if qtty == 0
        elif productQtty == 0:
            self.refresh()

            # refresh pages
            self.main.purchase.refresh()
            self.main.favorite.refresh()
            self.main.sell.refresh()
            self.main.home.refresh()
            return None
       
        #
        elif cartQtty == 0:
            message = MessageConfirm(self.page, "Excluir produto", f"Deseja Excluir Produto: {e.control.data[1]['descricao']}?")
            
            # wait response user
            while message.dialogResponse == None:
                pass

            # if message yes
            if message.dialogResponse == True:
                self.delete_product_from_cart(int(idCart))
                self.refresh()
                return None
            else:
                cartQtty = 1

        # set qtty cart
        txtQtty.value = str(cartQtty)

        # update qtde cart
        self.update_qtty_cart(idCart, cartQtty)

        # refresh page footer
        self.refresh()
        self.set_values_page_footer()


    # on click icon increment
    def on_click_icon_increment(self, e):

        #
        txtQtty = e.control.data[0]
        idCart = e.control.data[1]['id']
        idProduct = e.control.data[1]['id_produto']
        cartQtty = e.control.data[1]['qtde'] + 1    # after click increase

        # select qtty, situation product
        result = self.select_qtty_situation_from_product(idProduct)[0]
        productQtty, productSituation = result['qtde'], result['situacao']

        # if not active
        if productSituation != 'Ativo':
            
            # refresh page
            self.refresh()

            # refresh pages
            self.main.purchase.refresh()
            self.main.favorite.refresh()
            self.main.sell.refresh()
            self.main.home.refresh()
            self.page.update()
            return None

        # if qtty == 0
        elif productQtty == 0:
            
            # refresh
            self.refresh()
            
            # refresh pages
            self.main.purchase.refresh()
            self.main.favorite.refresh()
            self.main.sell.refresh()
            self.main.home.refresh()
            self.page.update()
            return None

        # check qtty in stock
        elif productQtty < cartQtty:
            self.refresh()
            Message(self.page, "Não há essa Qtde em Estoque!")
            return None

        txtQtty.value = str(cartQtty)
        self.update_qtty_cart(idCart, cartQtty)
        self.refresh()
        self.set_values_page_footer()
