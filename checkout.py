import flet as ft
from datetime import datetime
import time

# app
from utils import cntStyle, txtColorStyle, txtTitleLargeStyle, show_snack_bar_info, show_snack_bar_warning, Message
from address import Address
from sql_utils import db
from header_app import HeaderApp

class CrudCheckout:
    

    # select qtty e total price for products in cart
    def select_qtty_and_total_price_from_cart(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT COUNT(*) AS qtde_items, SUM(qtde*preco) AS total_price FROM view_carrinho WHERE id_cliente=? AND prod_selec='True'", (idClient, ))
        qtdePriceTotal = cursor.fetchone()
        conn.close()
        return qtdePriceTotal
      
    
    # select all product from cart
    def select_all_product_from_cart(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT id, id_produto, descricao, qtde, preco FROM view_carrinho WHERE id_cliente=? AND prod_selec='True'", (idClient, ))
        allProduct = cursor.fetchall()
        conn.close()
        return allProduct


    # select qtty, product from product
    def select_qtty_situation_from_product(self, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT qtde, situacao FROM produto WHERE id=?", (idProduct, ))
        result = cursor.fetchall()
        conn.close()
        return result


    # update qtde product
    def update_qtty_product(self, idProduto, qtde):
        conn, cursor = db()
        cursor.execute("UPDATE produto SET qtde=qtde-? WHERE id=?", (qtde, idProduto))
        conn.commit()
        conn.close()


    # update field prod_select cart
    def update_prod_selec_cart(self, idCart, boolValue):
        conn, cursor = db()
        cursor.execute("UPDATE carrinho SET prod_selec=? WHERE id=?", (boolValue, idCart))
        conn.commit()
        conn.close()


    # update field qtde in cart
    def update_qtty_cart(self, idCart, qtde):
        conn, cursor = db()
        cursor.execute("UPDATE carrinho SET qtde=? WHERE id=? ", (qtde, idCart))
        conn.commit()
        conn.close()


    # insert new purchase
    def insert_into_purchase(self, idClient, idAddress, paymentMethod, datePurchase, total):
        conn, cursor = db()
        cursor.execute('INSERT INTO compra (id_cliente, id_endereco, forma_pgto, data, valor) VALUES (?,?,?,?,?)', (idClient, idAddress, paymentMethod, datePurchase, total))
        idPurchase = cursor.lastrowid
        conn.commit()
        conn.close()
        return idPurchase

    
    # insert purchase item
    def insert_into_purchase_item(self, idPurchase, idProduct, qtde, price):
        conn, cursor = db()
        cursor.execute('INSERT INTO compra_item (id_compra, id_produto, qtde, preco) VALUES (?,?,?,?)', (idPurchase, idProduct, qtde, price))
        conn.commit()
        conn.close()

    
    # delete products from cart
    def delete_products_from_cart(self, idClient):
        conn, cursor = db()
        cursor.execute("DELETE FROM carrinho WHERE id_cliente=? AND prod_selec='True'", (idClient, ))
        conn.commit()
        conn.close()


    

class Checkout(HeaderApp, CrudCheckout):

    def __init__(self, main):
        HeaderApp.__init__(self, main)
        self.page = main.page
        self.main = main

        # row 
        self.row_header = ft.Row([self.cntHeaderMaster])
        self.row_body = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.row_footer = ft.Row()

        # column master
        self.colMaster = ft.Column([self.row_header, self.row_body, self.row_footer])


    # get column master
    def get(self):
        return self.colMaster
    

    # refresh page checkout
    def refresh(self):

        # address
        self.address = Address(self)

        #
        self.set_page_body_checkout()


    def set_page_body_checkout(self):

        # set container
        self.set_container_payment_methods()
        self.set_container_purchase_summary()

        # columns master page checkout (left, center, right)
        colLeft = ft.Column([self.address.get_container_list_all_address()])
        colCenter = ft.Column([self.cntRadioPaymentMethod])
        colRight = ft.Column([self.cntPurchaseSumary])

        colBody = ft.Column([
                    ft.Row([colLeft, colCenter, colRight], vertical_alignment=ft.CrossAxisAlignment.START),
                    ft.Row([self.address.get_container_form_address(), ft.Container(width=570)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])

        # set page body row
        self.row_body.controls = [colBody]

        # page update
        self.page.update()


    # set container payment methods
    def set_container_payment_methods(self):

        # title Payment Method
        txtTitlePaymentMethod = ft.Text('Forma de Pagamento', **txtTitleLargeStyle)

        # radio 
        radioPix = ft.Radio(value='Pix', label='Pix')
        radioPaymentSlip = ft.Radio(value='Boleto', label='Boleto')
        radioCreditCard =  ft.Radio(value='Cartão de Crédito', label='Cartão de Crédito')

        # column
        colRadio = ft.Column([radioPix, radioPaymentSlip, radioCreditCard])

        # Payment Method
        self.radioGroupPaymentMethod = ft.RadioGroup(colRadio, value='Pix')

        #
        colPaymentMethod = ft.Column([txtTitlePaymentMethod, self.radioGroupPaymentMethod])
        self.cntRadioPaymentMethod = ft.Container(colPaymentMethod, padding=10, **cntStyle)

    
    # set container purchase summary
    def set_container_purchase_summary(self):

        # title
        txtTitle = ft.Text('Resumo da Compra', **txtTitleLargeStyle)

        # qtde de items in cart
        self.txtQtdeItems = ft.Text(**txtColorStyle)

        # total price
        self.txtTotalPrice = ft.Text(**txtColorStyle)

        # button confirm purchase
        btnConfirmPurchase = ft.ElevatedButton('Confirma compra', color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_800, style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=10)))
        btnConfirmPurchase.on_click=self.on_click_button_confirm_purchase

        # column
        colPurchaseSumary = ft.Column([txtTitle, self.txtQtdeItems, self.txtTotalPrice, btnConfirmPurchase])

        # container 
        self.cntPurchaseSumary = ft.Container(colPurchaseSumary, padding=10, **cntStyle)

        # set values
        self.set_values_purchase_summary()

    
    # set values container purchase summary
    def set_values_purchase_summary(self):

        # get dtde e total price from cart
        self.cartSummary = self.select_qtty_and_total_price_from_cart(idClient=self.main.env.idClient)

        # qtde de items in cart
        self.txtQtdeItems.value = f'Quantidade de Ítens: {self.cartSummary['qtde_items']}'

        # total price
        self.txtTotalPrice.value = f'Valor total R$ {self.cartSummary['total_price']:>8.2f}'

        # refresh
        self.page.update()


    # on click button confirm purchase    
    def on_click_button_confirm_purchase(self, e):

        # verify if address was selected
        if self.address.radioGroupAddress.value == None or self.address.radioGroupAddress.value=="":
            show_snack_bar_warning(self.page, 'Endereço deve ser selecionado!')
            return None

        # get all produc from cart
        allProductCart = self.select_all_product_from_cart(idClient=self.main.env.idClient)

        #
        for cartProd in allProductCart:

            # select qtty, situation from product
            result = self.select_qtty_situation_from_product(cartProd['id_produto'])[0]
            productQtty, productSituation = result['qtde'], result['situacao']

            # qtty = 0
            if not productQtty:
                Message(self.page, f'Produto: {cartProd['descricao']} finalizado, (qtde=0), verifique seu carrinho.')
                self.update_prod_selec_cart(cartProd['id'], 'False')
                
                # refresh purchase summary
                self.set_values_purchase_summary()

                # refresh pages
                self.main.purchase.refresh()
                self.main.favorite.refresh()
                self.main.cart.refresh()
                self.main.sell.refresh()
                self.main.home.refresh()
                return None

            # product paused
            elif productSituation != 'Ativo':
                Message(self.page, f'Produto: {cartProd['descricao']} "{productSituation}", verifique seu carrinho.')
                self.update_prod_selec_cart(cartProd['id'], 'False')
                
                # refresh purchase summary
                self.set_values_purchase_summary()

                # refresh pages
                self.main.purchase.refresh()
                self.main.favorite.refresh()
                self.main.cart.refresh()
                self.main.sell.refresh()
                self.main.home.refresh()
                return None

            # verify product in stock
            elif productQtty < cartProd['qtde']:
                Message(self.page, f"Não tem essa qtde do produto: {cartProd['descricao']}, verifique seu carrinho.")
                self.update_qtty_cart(cartProd['id'], productQtty)
                self.update_prod_selec_cart(cartProd['id'], 'False')

                # refresh purchase summary
                self.set_values_purchase_summary()

                # refresh page cart
                self.main.cart.refresh()
                return None

        # if not error call function make_new_purchase
        self.make_new_purchase(allProductCart)


    # new purchase
    def make_new_purchase(self, allProductCart):

        # New Purchase
        idPurchase = self.insert_into_purchase(
                    idClient=self.main.env.idClient,
                    idAddress=self.address.colRadio.controls[int(self.address.radioGroupAddress.value)].data,
                    paymentMethod=self.radioGroupPaymentMethod.value,
                    datePurchase=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    total=self.cartSummary['total_price'])

        # iter allProduct
        for cartProd in allProductCart:

            # update table product
            self.update_qtty_product(cartProd['id_produto'], cartProd['qtde'])

            # insert purchase item
            self.insert_into_purchase_item(idPurchase=idPurchase, idProduct=cartProd['id_produto'], qtde=cartProd['qtde'], price=cartProd['preco'])

        # show message purchase success
        self.delete_products_from_cart(self.main.env.idClient)
        show_snack_bar_info(self.page, f'Pedido Confirmado: {idPurchase}')
        time.sleep(4)
            
        # refresh pages
        self.main.env.refresh_badge_cart()
        self.main.purchase.refresh()
        self.main.favorite.refresh()
        self.main.home.refresh()
        self.main.cart.refresh()
        self.main.sell.refresh()
        self.page.go('/home')