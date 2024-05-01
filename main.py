import flet as ft

# app
from product_description import ProductDescription
from new_account import NewAccount
from enviroment import Enviroment
from checkout import Checkout
from favorite import Favorite
from purchase import Purchase
from login_app import Login
from account import Account
from sell import Sell
from cart import Cart
from home import Home



class MainApp:

    def __init__(self, page:ft.Page):
        self.page = page
        self.page.theme_mode = ft.ThemeMode.LIGHT


        # page home
        self.home = Home(self)
        self.viewHome = ft.View('/home', padding=2)
        self.viewHome.controls = [self.home.get()]


        # page account
        self.account = Account(self)
        self.viewAccount = ft.View('/account', padding=2)
        self.viewAccount.controls = [self.account.get()]


        # page login
        self.login = Login(self)
        self.viewLogin = ft.View('/login', padding=2)
        self.viewLogin.controls = [self.login.get()]


        # page new account
        self.newAccount = NewAccount(self)
        self.viewNewAccount = ft.View('/new_account', padding=2)
        self.viewNewAccount.controls = [self.newAccount.get()]


        # page favorite
        self.favorite = Favorite(self)
        self.viewFavorite = ft.View('/favorite', padding=2)
        self.viewFavorite.controls = [self.favorite.get()]


        # page cart
        self.cart = Cart(self)
        self.viewCart = ft.View('/cart', padding=2)
        self.viewCart.controls = [self.cart.get()]


        # page product description
        self.prod_desc = ProductDescription(self)
        self.viewProductDescription = ft.View('/product_description', padding=2)
        self.viewProductDescription.controls = [self.prod_desc.get()]


        # page checkout
        self.checkout = Checkout(self)
        self.viewCheckout = ft.View('/checkout', padding=2)
        self.viewCheckout.controls = [self.checkout.get()]


        # page purchase
        self.purchase = Purchase(self)
        self.viewPurchase = ft.View('/purchase', padding=2)
        self.viewPurchase.controls = [self.purchase.get()]


        # page sell
        self.sell = Sell(self)
        self.viewSell = ft.View('/sell', padding=2)
        self.viewSell.controls = [self.sell.get()]


        # page start and config enviroment
        self.env = Enviroment(self)
        self.env.start_pages()


        # router views
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    
    # route change
    def route_change(self, e):
        self.page.views.clear()

        # page (default)
        self.page.views.append(self.viewHome)


        # if page newAccount
        if self.page.route == '/new_account':
            self.page.views.append(self.viewNewAccount)


        # if page login
        elif self.page.route == "/login":
            self.page.views.append(self.viewLogin)


        # if page cart
        elif self.page.route == "/cart":
            self.page.views.append(self.viewCart)
        

        # if page product description
        elif self.page.route == "/product_description":
            self.page.views.append(self.viewProductDescription)


        # if page favorite product
        elif self.page.route == '/favorite':
            self.page.views.append(self.viewFavorite)


        # if page checkout
        elif self.page.route == '/checkout':
            self.page.views.append(self.viewCheckout)


        # if page Account
        elif self.page.route == '/account':
            self.page.views.append(self.viewAccount)


        # if page Purchase
        elif self.page.route == '/purchase':
            self.page.views.append(self.viewPurchase)


        # if page Sell
        elif self.page.route == '/sell':
            self.page.views.append(self.viewSell)

        # update page
        self.page.update()


    # view pop
    def view_pop(self, e):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)


# view=ft.AppView.WEB_BROWSER
ft.app(target=MainApp, view=ft.AppView.WEB_BROWSER)

