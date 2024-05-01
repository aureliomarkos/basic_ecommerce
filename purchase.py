import flet as ft
from datetime import datetime

# app
from utils import cntStyle, txtColorStyle, txtTitleMediumStyle, txtTitleSmallStyle
from header_app import HeaderApp
from sql_utils import db


class CrudPurchase:
    

    # select all items in view purchase items
    def select_all_from_view_purchase_item(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT * FROM view_compra_item WHERE id_cliente=? ORDER BY id DESC", (idClient, ))
        items = cursor.fetchall()
        conn. close()
        return items


    # select qtty product from product
    def select_qtty_situation_from_product(self, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT qtde, situacao FROM produto WHERE id=?", (idProduct, ))
        result = cursor.fetchall()
        conn.close()
        return result



class Purchase(HeaderApp, CrudPurchase):

    def __init__(self, main):
        HeaderApp.__init__(self, main)
        self.page = main.page
        self.main = main
        
        # columns
        self.row_header = ft.Row([self.cntHeaderMaster])
        self.row_body = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
        self.row_footer = ft.Row()

        # column master
        self.colMaster = ft.Column([self.row_header, self.row_body, self.row_footer])


    # clear page
    def clear(self):
        self.row_body.controls.clear()


    # get control master
    def get(self):
        return self.colMaster

    # show page
    def show(self):
        self.refresh()

    
    # refresh data page body purchase
    def refresh(self):
        self.set_page_body_purchase()

    
    # set page body purchase
    def set_page_body_purchase(self):
        
        # clear row body
        self.row_body.controls.clear()

        # get all purchase products
        allItemsPurchase = self.select_all_from_view_purchase_item(self.main.env.idClient)

        # column purchase products
        colAllPurchase = ft.Column()
        colProduct = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=850)
        rowPurchase = ft.Row()

        # First Purchase ID
        idPurchase=0

        # iter items
        for purchaseProd in allItemsPurchase:

            result = self.select_qtty_situation_from_product(purchaseProd['id_produto'])[0]
            qtty, situation = result['qtde'], result['situacao']

            # id purchase
            txtIdPurchase = ft.Text(f'ID: {purchaseProd['id']}', **txtTitleMediumStyle)

            # date purchase
            purchaseDate = datetime.strptime(purchaseProd['data'], "%Y-%m-%d %H:%M:%S")
            txtDatePurchase = ft.Text(f'Data: {purchaseDate.strftime("%d/%m/%Y %H:%M:%S")}', **txtTitleMediumStyle)

            # payment method
            txtPaymentMethod = ft.Text(f'Pgto: {purchaseProd['forma_pgto']}', **txtTitleMediumStyle)

            # Purchase price
            txtPurchasePrice = ft.Text(f'Valor: R$ {purchaseProd['valor']:>8.2f}'.replace('.', ','), **txtTitleMediumStyle)

            # address
            txtAddress = ft.Text(f'Endereço: {purchaseProd['rua']}, {purchaseProd['nro']} - {purchaseProd['bairro']} - {purchaseProd['cidade']}', **txtColorStyle)

            # row purchase
            rowPurchase = ft.Row([txtIdPurchase, txtDatePurchase, txtPaymentMethod, txtPurchasePrice])
            rowAddress = ft.Row([txtAddress])

            # Seller's name
            txtSellerName = ft.Text(f'Vendedor: {purchaseProd['vendedor_nome']}', **txtColorStyle)

            # image purchase
            imageProduct = ft.Image(src_base64=purchaseProd['imagem'], width=60, height=60)
            cntImageProduct = ft.Container(imageProduct, data=purchaseProd, on_click=self.on_click_image_product)
            
            #
            if qtty == 0:
                cntImageProduct.tooltip = 'Produto finalizado(qtde=0).'
                cntImageProduct.disabled=True

            #
            elif situation != 'Ativo':
                cntImageProduct.tooltip = f'Produto esta {situation}.'
                cntImageProduct.disabled=True


            # description product
            txtDescriptionProduct = ft.Text(purchaseProd['descricao'], width=560, max_lines=3, **txtTitleSmallStyle)

            # qtde product
            txtQtdeProduct = ft.Text(f'Qtde: {purchaseProd['qtde']}', **txtColorStyle)

            # price product
            txtPrice = ft.Text(f'R$ {purchaseProd['preco']:>8.2f}'.replace('.', ','), **txtTitleMediumStyle)

            # row qtdePduct, priceProduct
            rowQtdePrice = ft.Column([txtQtdeProduct, txtPrice], spacing=0)

            # column left and right description product
            colLeft = ft.Column([cntImageProduct])
            colRight = ft.Column([txtDescriptionProduct, txtSellerName, rowQtdePrice], spacing=0)

            # row left row right description product
            rowDescriptionProduct = ft.Row([colLeft, colRight])

            # if change id, new column
            if purchaseProd['id'] != idPurchase:

                # new colAllPurchase
                colAllPurchase = ft.Column()
                colAllPurchase.controls.append(rowPurchase)
                colAllPurchase.controls.append(rowAddress)
                colAllPurchase.controls.append(rowDescriptionProduct)

                # container product
                cntProduct = ft.Container(colAllPurchase, padding=10, margin=ft.margin.only(right=10), **cntStyle)

                # append product in colProduct
                colProduct.controls.append(cntProduct)

            #
            else:

                # set row description product
                colAllPurchase.controls.append(rowDescriptionProduct)

            # idPurchase
            idPurchase = purchaseProd['id']

        # append all product in row body
        self.row_body.controls.append(colProduct)

        #
        self.page.update()
    

    # on click image product
    def on_click_image_product(self, e):
        idProduct = e.control.data['id_produto']
        self.main.prod_desc.set_product(idProduct)
        self.page.go('/product_description')