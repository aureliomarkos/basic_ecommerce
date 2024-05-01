import flet as ft

# app
from utils import cntStyle, txtColorStyle, txtTitleMediumStyle, txtTitleLargeStyle
from sql_utils  import db
from header_app import HeaderApp



class CrudProductDescription:

    # insert product
    def insert_product_into_cart(self, idClient, idProduct):
        conn, cursor = db()
        
        # exist product in cart?
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

        # if not exist in cart, insert product
        else:
            cursor.execute("INSERT INTO carrinho (id_cliente, id_produto, qtde, prod_selec) VALUES (?,?,?,?)", (idClient, idProduct, 1, 'True'))

        # commit e close db
        conn.commit()
        conn.close()


    # insert favorite product
    def insert_product_into_favorite(self, idClient, idProduct):
        conn, cursor = db()
        cursor.execute("INSERT INTO favorito (id_cliente, id_produto) VALUES (?,?)", (idClient, idProduct))
        conn.commit()
        conn.close()

    
    # delete favorite product
    def delete_product_from_favorite(self, idClient, idProduct):
        conn, cursor = db()
        cursor.execute("DELETE FROM favorito WHERE id_cliente=? AND id_produto=?", (idClient, idProduct))
        conn. commit()
        conn.close()


    # select descricao do produto
    def select_description_from_product_description(self, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT descricao FROM produto_descricao WHERE id_produto=?", (idProduct,))
        product_description = cursor.fetchone()[0]
        conn.close()
        return product_description


    # select all image products
    def select_all_image_from_product_description(self, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT imagem_0, imagem_1, imagem_2, imagem_3, imagem_4 FROM produto_descricao WHERE id_produto=?", (idProduct,))
        all_imagem = cursor.fetchone()
        conn.close()
        return all_imagem


    # select favorite product
    def select_product_from_favorite(self, idClient, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT id_cliente, id_produto FROM favorito WHERE id_cliente=? AND id_produto=?", (idClient, idProduct))
        favorite = cursor.fetchone()
        conn.close()
        return favorite


    # select product
    def select_product_from_product(self, idProduct):
        conn, cursor = db()
        cursor.execute("SELECT id, descricao, imagem, preco, condicao FROM produto WHERE id=?", (idProduct, ))
        product = cursor.fetchone()
        conn.close()
        return product



class ProductDescription(HeaderApp, CrudProductDescription):

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


    # set product
    def set_product(self, product):
        self.set_page_body_product_description(product)


    # set all image for product
    def set_all_image_product(self, colLeft, product):

        # insert image master
        imgMaster = ft.Image(src_base64=product['imagem'], width=60, height=60) 
        colLeft.controls.append(ft.Container(imgMaster,
                                             margin=ft.margin.only(top=10, left=10),
                                             on_hover=self.on_hover_small_image,
                                             **cntStyle))
        
        # get all image product
        allImage = self.select_all_image_from_product_description(product['id'])

        #
        for image in allImage:
            if image:
                imgProduct = ft.Image(src_base64=image, width=60, height=60) 
                cntImage = ft.Container(imgProduct,
                                             margin=ft.margin.only(top=10, left=10),
                                             on_hover=self.on_hover_small_image,
                                             **cntStyle)
                colLeft.controls.append(cntImage)


    # refresh description products
    def set_page_body_product_description(self, idProduct):

        # select favorite product
        selectFavProd = self.select_product_from_favorite(idClient=self.main.env.idClient, idProduct=idProduct)

        # if product is favorite
        if not selectFavProd: favProd=False
        else: favProd=True

        # select product
        product = self.select_product_from_product(idProduct)

        # icon favorite
        iconFavorite = ft.IconButton(icon=ft.icons.FAVORITE_OUTLINE_ROUNDED, data=product, selected=favProd, selected_icon=ft.icons.FAVORITE, icon_color=ft.colors.BLUE_800, on_click=self.on_click_icon_favorite)
        self.bdgIconFavorite = ft.Badge(content=iconFavorite)

        # description do product
        txtDescription = ft.Text(product['descricao'], width=395, max_lines=3, **txtTitleMediumStyle)

        # image Large   , 
        self.imgLarge = ft.Image(src_base64=product['imagem'], width=300, height=300)
        cntImageLarge = ft.Container(self.imgLarge, margin=ft.margin.only(top=10, bottom=10), **cntStyle)

        # preco vendas
        txtPrice = ft.Text(f"R$ {product['preco']:>8.2f}".replace('.', ','), **txtTitleLargeStyle)

        # button add cart       
        txtBtnAddCart = ft.TextButton(text="Adicionar ao Carrinho", data=product, on_click=self.on_click_button_add_produto, style=ft.ButtonStyle(color=ft.colors.BLUE_800), icon=ft.icons.ADD_SHOPPING_CART)

        # row favorite
        rowFavorite = ft.Row([ft.Text(product['condicao'], **txtColorStyle), ft.Container(width=10), ft.Text('+1000', **txtColorStyle), ft.Container(width=270), iconFavorite], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # columns page product description
        colLeft = ft.Column(spacing=0, scroll=ft.ScrollMode.ALWAYS, height=300, width=90)
        colCenter = ft.Column([cntImageLarge], height=320)
        colRight = ft.Column([rowFavorite, txtDescription, txtPrice, txtBtnAddCart])
        
        # 
        cntColRight = ft.Container(colRight, padding=10, margin=ft.margin.only(top=10, right=10), **cntStyle)

        # set all image product
        self.set_all_image_product(colLeft, product)

        # column
        rowProduto = ft.Row([colLeft, colCenter, cntColRight], vertical_alignment=ft.CrossAxisAlignment.START)
        contProduto = ft.Container(rowProduto, **cntStyle)

        # row product description
        productDescription = self.select_description_from_product_description(product['id'])
        txtProductDescription = ft.Text(productDescription, width=820, **txtColorStyle)
        
        colProduct = ft.Column([contProduto])
        colDescription = ft.Container(ft.Column([txtProductDescription], height=500, scroll=ft.ScrollMode.ALWAYS), padding=10, **cntStyle)

        # set in row body
        self.row_body.controls = [ft.Column([colProduct, colDescription])]
        self.page.update()


    # on click icon favorite
    def on_click_icon_favorite(self, e):
        product = e.control.data
        # insert and delete product favorite
        if e.control.selected==False:
            self.insert_product_into_favorite(idClient=self.main.env.idClient, idProduct=product['id'])
        else:
            self.delete_product_from_favorite(idClient=self.main.env.idClient, idProduct=product['id'])

        # refresh icon favorite
        e.control.selected = not e.control.selected

        # refresh page favorite product
        self.main.favorite.refresh()

        # refresh page
        self.page.update()


    # button add produto clicked
    def on_click_button_add_produto(self, e):

        #
        product = e.control.data

        # insert product in cart
        self.insert_product_into_cart(idClient=self.main.env.idClient, idProduct=product['id'])
        self.main.env.refresh_badge_cart()
        self.main.cart.refresh()
        

    # on hover in small image
    def on_hover_small_image(self, e):
        
        # set imageSmall  in imageLarge
        self.imgLarge.src_base64 = e.control.content.src_base64
        self.page.update()