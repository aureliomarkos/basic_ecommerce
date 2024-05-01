import flet as ft

# app
from sql_utils import db
from utils import cntStyle, txtFldBorderColorStyle



class CrudHeaderApp:

    # select imagem app
    def select_image_from_app(self):
        conn, cursor = db()
        cursor.execute("SELECT imagem FROM app WHERE nome='home_128.png'")
        imagem = cursor.fetchone()[0]
        conn.close()
        return imagem



class HeaderApp(CrudHeaderApp):

    def __init__(self, main):
        self.main = main
        self.page = main.page

        # image app
        imageApp = ft.Image(src_base64=self.select_image_from_app())
        cntImageApp = ft.Container(content=imageApp, width=70, height=70, on_click=self.on_click_container_image_app)

        # search bar
        self.searchProductDescription = ft.TextField(height=40, on_submit=self.on_submit_search_product, **txtFldBorderColorStyle)
        cntSearchProduto = ft.Container(content=self.searchProductDescription, width=500, padding=ft.padding.only(top=10))

        # icon button search
        iconBtnSearch = ft.IconButton(icon=ft.icons.SEARCH, icon_size=40, style=ft.ButtonStyle(color=ft.colors.BLUE_600), on_click=self.on_submit_search_product)
        cntIconBtnSearch = ft.Container(content=iconBtnSearch, margin=0, padding=0)

        # link favorite
        txtBtnFavorite = ft.TextButton('Favoritos', style=ft.ButtonStyle(color=ft.colors.BLUE_600, bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_50}), on_click=self.on_click_favorite)
        if self.__class__.__name__ == 'Favorite':
            txtBtnFavorite.style = ft.ButtonStyle(color=ft.colors.RED, bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_50})
            txtBtnFavorite.disabled=True

        # link purchase
        txtBtnPurchase = ft.TextButton('Compras', style=ft.ButtonStyle(color=ft.colors.BLUE_600, bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_50}), on_click=self.on_click_button_purchase)
        if self.__class__.__name__ == 'Purchase':
            txtBtnPurchase.style = ft.ButtonStyle(color=ft.colors.RED, bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_50})
            txtBtnPurchase.disabled=True

        # link sales
        txtBtnSell = ft.TextButton('Vender', style=ft.ButtonStyle(color=ft.colors.BLUE_600, bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_50}), on_click=self.on_click_button_sell)
        if self.__class__.__name__ == 'Sell':
            txtBtnSell.style = ft.ButtonStyle(color=ft.colors.RED, bgcolor={ft.MaterialState.HOVERED: ft.colors.BLUE_50})
            txtBtnSell.disabled=True

        # icon button account
        iconBtnAccount = ft.IconButton(icon=ft.icons.MANAGE_ACCOUNTS_ROUNDED, tooltip='Login', icon_size=40, style=ft.ButtonStyle(color=ft.colors.BLUE_600), on_click=self.on_click_icon_button_account)
        self.badgeAccount = ft.Badge(iconBtnAccount, alignment=ft.alignment.top_left)

        # disable icon
        if self.__class__.__name__ == 'Account':
            iconBtnAccount.style = ft.ButtonStyle(color=ft.colors.RED)
            iconBtnAccount.disabled=True

        # icon button cart
        iconBtnCart = ft.IconButton(icon=ft.icons.SHOPPING_CART, icon_size=40, style=ft.ButtonStyle(color=ft.colors.BLUE_600), on_click=self.on_click_icon_cart)
        self.badgeCart = ft.Badge(iconBtnCart)

        # disable icon
        if self.__class__.__name__ == 'Cart':
            iconBtnCart.style = ft.ButtonStyle(color=ft.colors.RED)
            iconBtnCart.disabled=True

        #
        row0 = ft.Row([cntImageApp, cntSearchProduto, cntIconBtnSearch], alignment=ft.MainAxisAlignment.CENTER)
        row1 = ft.Row([
                        txtBtnFavorite,
                        txtBtnPurchase,
                        txtBtnSell,
                        self.badgeAccount,
                        self.badgeCart],
                        spacing=80,
                        alignment=ft.MainAxisAlignment.CENTER)
        
        # row header
        rowHeader = ft.Column([row0, row1], spacing=0)
        self.cntHeaderMaster = ft.Container(rowHeader, expand=True, **cntStyle)

    
    # on click button sell
    def on_click_button_sell(self, e):
        self.page.go('/sell')


    # on click button purchase
    def on_click_button_purchase(self, e):
        self.page.go('/purchase')


    # on click favorite
    def on_click_favorite(self, e):
        self.page.go('/favorite')        


    # on click icon button account
    def on_click_icon_button_account(self, e):
        self.page.go('/account')


    # on click icon cart
    def on_click_icon_cart(self, e):
        self.page.go('/cart')
        

    # on click container image
    def on_click_container_image_app(self, e):
     
        # if click for in page home
        if self.__class__.__name__ == 'Home':
            self.searchProductDescription.value=''
            self.ddOrderBy.value=-1
            self.refresh()

        # go Home
        self.page.go('/home')
        self.page.update()


    # on submit text field searchProduct
    def on_submit_search_product(self, e):

        # if not values in searchProduct
        if not self.searchProductDescription.value:
            return None

        # if route initial
        if self.page.route == '/home' or self.page.route == '/':
            self.make_exec_sql_command()

        # others route
        else:
            self.main.home.searchProductDescription.value = self.searchProductDescription.value
            self.main.home.make_exec_sql_command()
            self.page.go('/home')
