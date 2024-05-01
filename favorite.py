import flet as ft

# app
from header_app import HeaderApp
from sql_utils import db
from utils import MessageConfirm, Message, cntStyle, txtTitleMediumStyle


class CrudFavorite:
        
    # insert product
    def insert_product_into_cart(self, idClient, idProduct):
        conn, cursor = db()
        
        # exist product in cart
        cursor.execute("SELECT * FROM view_carrinho WHERE id_produto=? AND id_cliente=?", (idProduct, idClient))
        result = cursor.fetchall()
        

        # if exists product
        if result:

            # qtty product no stock, qtty product in cart
            qttyProduct = result[0]['qtde_produto']
            qttyCart = result[0]['qtde']

            # increment qtde
            if qttyProduct > qttyCart:
                cursor.execute("UPDATE carrinho SET qtde=qtde+1 WHERE id_produto=? AND id_cliente=?", (idProduct, idClient))

        # if not exist, insert product
        else:
            cursor.execute("INSERT INTO carrinho (id_cliente, id_produto, qtde, prod_selec) VALUES (?,?,?,?)", (idClient, idProduct, 1, 'True'))

        # commit e close db
        conn.commit()
        conn.close()


    # delete favorite product
    def delete_product_from_favorite(self, idFavorite):
        conn, cursor = db()
        cursor.execute("DELETE FROM favorito WHERE id=?", (idFavorite, ))
        conn.commit()
        conn.close()


    # select all favorite product
    def select_all_product_from_favorite(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT id, id_cliente, id_produto, descricao, qtde, preco, imagem, situacao  FROM view_favorito WHERE id_cliente=?", (idClient, ))
        allFavorito = cursor.fetchall()
        conn.close()
        return allFavorito


    # select situation from view favorite
    def select_situation_from_view_favorite(self, idProduto):
        conn, cursor = db()
        cursor.execute("SELECT situacao FROM view_favorito WHERE id_produto=?", (idProduto, ))
        situacao = cursor.fetchone()[0]
        conn.close()
        return situacao


    # select qtty product
    def select_qtty_from_product(self, idProduto):
        conn, cursor = db()
        cursor.execute("SELECT qtde FROM produto WHERE id=?", (idProduto,))
        productQtty = cursor.fetchone()[0]
        conn.close()
        return productQtty



class Favorite(HeaderApp, CrudFavorite):

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


    # get colMaster
    def get(self):
        return self.colMaster

    # show page
    def show(self):
        self.refresh()


    # refresh favorite product body
    def refresh(self):
        self.set_page_body_favorite_product()


    # clear
    def clear(self):
        self.row_body.controls.clear()
        self.page.update()


    # set page body favorite
    def set_page_body_favorite_product(self):
        
        # col favorite product
        self.colProduct = ft.Column()

        # get all favorite product
        allFavoriteProduct = self.select_all_product_from_favorite(idClient=self.main.env.idClient)

        # iter in products
        for idx, favoriteProd in enumerate(allFavoriteProduct):

            # icon remove favorite product
            iconRemoveFavProduct = ft.IconButton(ft.icons.DELETE_FOREVER, data=favoriteProd, icon_color="red", tooltip="Excluir Produto", on_click=self.on_click_icon_remove_product)

            # image product
            imageProduct = ft.Image(src_base64=favoriteProd['imagem'], width=60, height=60)
            cntImageProduct = ft.Container(imageProduct, data=favoriteProd, on_click=self.on_click_image_product)

            # description product
            txtDescription = ft.Text(favoriteProd['descricao'], width=560, max_lines=3, **txtTitleMediumStyle)

            # price product
            txtPrice = ft.Text(f'R$ {favoriteProd['preco']:>8.2f}'.replace('.', ','), width=100, **txtTitleMediumStyle)

            # if Active
            if favoriteProd['situacao'] != 'Ativo':
                cntImageProduct.tooltip = f'Este produto esta {favoriteProd['situacao']}.'
                cntImageProduct.disabled = True
                txtButtonAddCart = ft.Text(f'Este produto esta {favoriteProd['situacao']}.', color=ft.colors.RED_300, weight=ft.FontWeight.BOLD, width=200)

            # if qtty == 0
            elif favoriteProd['qtde'] == 0:
                cntImageProduct.tooltip = 'Produto finalizado(qtde=0).'
                cntImageProduct.disabled = True
                txtButtonAddCart = ft.Text('Produto finalizado(qtde=0).', color=ft.colors.RED_300, weight=ft.FontWeight.BOLD, width=200)
            #
            else:
                txtButtonAddCart = ft.TextButton(text="Adicionar ao Carrinho", on_click=self.on_click_button_add_produto, data=[idx, favoriteProd], style=ft.ButtonStyle(color=ft.colors.BLUE_800), icon=ft.icons.ADD_SHOPPING_CART)

            # row favorite
            self.rowFavorite = ft.Row([iconRemoveFavProduct, cntImageProduct, txtDescription, txtPrice, txtButtonAddCart])
            self.cntRowFavorite = ft.Container(self.rowFavorite, width=1000, **cntStyle)

            # add in colProduct
            self.colProduct.controls.append(self.cntRowFavorite)

        self.row_body.controls = [self.colProduct]
        self.page.update()


    # on click image product
    def on_click_image_product(self, e):
        idProduct = e.control.data['id_produto']
        self.main.prod_desc.set_product(idProduct)
        self.page.go('/product_description')


    # on click icon remove product
    def on_click_icon_remove_product(self, e):

        # message remove product
        message = MessageConfirm(self.page, "Remover Favorito", f"Remover o produto: {e.control.data['descricao']} de favoritos?")

        # wait response
        while message.dialogResponse == None:
            pass
        
        # if response yes
        if message.dialogResponse == False:
            return None

        # if message yes
        idFavorite = e.control.data['id']

        # delete favorite product
        self.delete_product_from_favorite(idFavorite)
        self.refresh()


    # button add produto clicked
    def on_click_button_add_produto(self, e):

        # idProduct
        index = e.control.data[0]
        idProduct = e.control.data[1]['id_produto']

        # verify situation product
        situacao = self.select_situation_from_view_favorite(idProduct)
        if situacao != 'Ativo':
            Message(self.page, f'Este produto esta {situacao}.')
            self.colProduct.controls[index].content.controls.pop(4)
            txtButtonAddCart = ft.Text(f'Este produto esta {situacao}.', color=ft.colors.RED_300, weight=ft.FontWeight.BOLD, width=200)
            self.colProduct.controls[index].content.controls.append(txtButtonAddCart)
            
            # container Image
            self.colProduct.controls[index].content.controls[1].tooltip = f'Este produto esta {situacao}.'
            self.colProduct.controls[index].content.controls[1].disabled=True

            # refresh Pages
            self.main.sell.refresh()
            self.main.cart.refresh()
            self.main.home.refresh()
            self.main.purchase.refresh()
            #
            self.page.update()
            return None

        # verify qtde product
        productQtty = self.select_qtty_from_product(idProduct)
        if productQtty == 0:
            Message(self.page, 'Produto sem estoque.')
            self.colProduct.controls[index].content.controls.pop(4)
            txtButtonAddCart = ft.Text('Produto finalizado(qtde=0).', color=ft.colors.RED_300, weight=ft.FontWeight.BOLD, width=200)
            self.colProduct.controls[index].content.controls.append(txtButtonAddCart)
            
            # container Image
            self.colProduct.controls[index].content.controls[1].tooltip = 'Produto finalizado(qtde=0).'
            self.colProduct.controls[index].content.controls[1].disabled=True

            # refresh Pages
            self.main.sell.refresh()
            self.main.cart.refresh()
            self.main.home.refresh()
            self.main.purchase.refresh()

            #
            self.page.update()
            return None

        # insert product in cart
        self.insert_product_into_cart(idClient=self.main.env.idClient, idProduct=idProduct)

        # refresh qtde items in cart
        self.main.env.refresh_badge_cart()
        self.main.cart.refresh()