from sql_utils import db



class CrudEnviroment:

    # select qtty items in cart
    def select_qtty_items_cart(self, idClient):
        conn, cursor = db()
        cursor.execute("SELECT COUNT(id) FROM carrinho WHERE id_cliente=?", (idClient, ))
        cartQtty = cursor.fetchone()
        conn.close()
        return cartQtty



class Enviroment(CrudEnviroment):

    def __init__(self, main):
        self.main = main
        self.page = main.page


    # start all pages app
    def start_pages(self):

        # set default client
        self.idClient = 1
        self.clientName = 'Visitante App'

        # qtty in cart
        self.cartQtty=0
        cartQtty = self.select_qtty_items_cart(self.idClient)[0]
        if cartQtty:
            self.cartQtty=cartQtty

        # start default pages
        self.main.home.show()
        self.main.account.show()
        self.main.cart.show()
        self.main.favorite.show()
        self.main.purchase.show()
        self.main.sell.show()
        
        # icon button logout
        self.main.account.iconBtnLogout.disabled=True

        # set badge
        self.set_badge_account(self.clientName[:self.clientName.find(' ')])
        self.set_badge_cart(self.cartQtty)

        # go home page
        self.page.go('/home')


    # change client
    def change_client(self, idClient=1, clientName='Visitante App'):

        # set default client
        self.idClient = idClient
        self.clientName = clientName

        # clear pages
        self.main.home.clear()
        self.main.cart.clear()
        self.main.favorite.clear()
        self.main.sell.clear()
        self.main.purchase.clear()
        self.main.account.clear()

        # start pages
        self.main.home.refresh()
        self.main.account.refresh()
        self.main.cart.refresh()
        self.main.favorite.refresh()
        self.main.purchase.refresh()
        self.main.sell.refresh()

        if idClient==1:
            self.main.account.iconBtnLogout.disabled=True
        else:
            self.main.account.iconBtnLogout.disabled=False

        # qtty in cart
        self.cartQtty=0
        cartQtty = self.select_qtty_items_cart(self.idClient)[0]
        if cartQtty:
            self.cartQtty=cartQtty

        # set badge
        self.set_badge_account(self.clientName[:self.clientName.find(' ')])
        self.set_badge_cart(self.cartQtty)

        # go home page
        self.page.go('/home')


    # refresh qtty cart
    def refresh_badge_cart(self):
        self.cartQtty = self.select_qtty_items_cart(self.idClient)[0]
        self.set_badge_cart(self.cartQtty)


    # refresh badge account
    def set_badge_account(self, clientName='Visitante'):
        self.main.favorite.badgeAccount.text = clientName
        self.main.cart.badgeAccount.text = clientName
        self.main.prod_desc.badgeAccount.text = clientName
        self.main.checkout.badgeAccount.text = clientName
        self.main.home.badgeAccount.text = clientName
        self.main.account.badgeAccount.text = clientName
        self.main.purchase.badgeAccount.text = clientName
        self.main.sell.badgeAccount.text = clientName
        self.page.update()


    # refresh badge cart
    def set_badge_cart(self, cartQtty=0):
        self.main.favorite.badgeCart.text = cartQtty
        self.main.cart.badgeCart.text = cartQtty
        self.main.prod_desc.badgeCart.text = cartQtty
        self.main.checkout.badgeCart.text = cartQtty
        self.main.home.badgeCart.text = cartQtty
        self.main.account.badgeCart.text = cartQtty
        self.main.purchase.badgeCart.text = cartQtty
        self.main.sell.badgeCart.text = cartQtty
        self.page.update()