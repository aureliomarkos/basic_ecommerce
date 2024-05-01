import flet as ft

# app
from utils import cntStyle, txtColorStyle, txtLabelSmallStyle, txtTitleMediumStyle, txtFldBorderColorStyle
from sql_utils import db
from header_app import HeaderApp


class CrudHome:


    # get all produtos
    def select_all_from_product(self):
        conn, cursor = db()
        cursor.execute("SELECT * FROM produto WHERE situacao='Ativo' AND qtde > 0 ORDER BY LOWER(descricao) ASC LIMIT 500")
        all = cursor.fetchall()
        conn.close()
        return all
    

    # select all category
    def select_all_from_category(self):
        conn, cursor = db()
        cursor.execute("SELECT id, descricao FROM categoria WHERE ativo=1 ORDER BY descricao")
        allCategory = cursor.fetchall()
        conn.close()
        return allCategory


    # select description from product
    def select_from_product_order_by(self, sqlCommand):
        conn, cursor = db()
        cursor.execute(sqlCommand)
        all = cursor.fetchall()
        conn.close()
        return all


class NavigationPages:

    def __init__(self, main):
        self.page = main.page
        self.main = main
        self.row_footer = main.row_footer
        self.colCenter = main.colCenter
        
        # controls
        self.txtTotalPages = ft.Text(**txtColorStyle)
        self.txtBtnFirstPage = ft.TextButton('primeira', icon=ft.icons.FIRST_PAGE, on_click=self.first_page)
        self.txtBtnPreviousPage = ft.TextButton('anterior', icon=ft.icons.SKIP_PREVIOUS, on_click=self.previous_page)
        self.txtBtnNextPage = ft.TextButton('próxima', icon=ft.icons.SKIP_NEXT, on_click=self.next_page)
        self.txtBtnLastPage = ft.TextButton('última', icon=ft.icons.LAST_PAGE, on_click=self.last_page)
        rowPages = ft.Row([self.txtTotalPages, self.txtBtnFirstPage, self.txtBtnPreviousPage, self.txtBtnNextPage, self.txtBtnLastPage], width=580)
        cntRowPages = ft.Container(rowPages, padding=10, **cntStyle)

        # set controls in row_footer
        self.row_footer.controls = [cntRowPages]


    # set products
    def set_result(self, result):

        # if not products
        if not result:

            # disable buttons
            self.txtBtnFirstPage.disabled=True
            self.txtBtnPreviousPage.disabled=True
            self.txtBtnNextPage.disabled=True
            self.txtBtnLastPage.disabled=True
            self.totalPages=0
            self.pageNumber=0

            #
            self.colCenter.controls.clear()
            self.refresh_text_total_pages()
            return None
        #
        else:

            # enable buttons
            self.txtBtnFirstPage.disabled=False
            self.txtBtnPreviousPage.disabled=False
            self.txtBtnNextPage.disabled=False
            self.txtBtnLastPage.disabled=False

        # start control navigation        
        self.products = result
        self.totalProducts = len(result)
        self.totalPages = 0
        self.pageNumber = 1 
        self.initialIndex = 0
        self.qttyIndex = 9
        self.totalProductsForPage = 9
        self.totalProductsForLastPage = 9
        self.flagExactDivision = True

        # if total products < 9
        if self.totalProducts <= 9:
            self.totalPages=1
            self.qttyIndex=self.totalProducts
            self.refresh_products()
            self.refresh_text_total_pages()
            return None

        # if division not exact
        if self.totalProducts % self.totalProductsForPage:
            self.flagExactDivision=False
            self.totalPages = (self.totalProducts // self.totalProductsForPage) + 1
            self.totalProductsForLastPage = self.totalProducts - (self.totalProducts // self.totalProductsForPage) * self.totalProductsForPage
        else:
            self.totalPages = (self.totalProducts // self.totalProductsForPage)

        #
        self.refresh_products()
        self.refresh_text_total_pages()


    #
    def first_page(self, e):
        if self.pageNumber == 1:
            return None
        self.pageNumber=1
        self.initialIndex=0
        self.qttyIndex = self.totalProductsForPage
        self.refresh_products()

    #
    def previous_page(self, e):
        if self.pageNumber == 1:
            return None
        self.pageNumber-=1
        self.initialIndex -= self.totalProductsForPage
        self.qttyIndex = self.totalProductsForPage
        self.refresh_products()

    #
    def next_page(self, e):
        if self.pageNumber >= self.totalPages:
            return None
        
        # if division not exact
        if self.flagExactDivision == False:
            # verify if last page
            if self.pageNumber + 1 == self.totalPages:
                self.pageNumber+=1
                self.initialIndex += self.totalProductsForPage
                self.qttyIndex = self.totalProductsForLastPage
                self.refresh_products()
                return None

        #
        self.pageNumber+=1
        self.initialIndex += self.totalProductsForPage
        self.qttyIndex = self.totalProductsForPage
        self.refresh_products()

    #
    def last_page(self, e):
        if self.totalPages == 1 or self.pageNumber == self.totalPages:
            return None
        self.pageNumber = self.totalPages
        self.initialIndex = (self.totalPages-1) * self.totalProductsForPage
        self.qttyIndex = self.totalProductsForLastPage
        self.refresh_products()

    #
    def refresh_text_total_pages(self):
        self.txtTotalPages.value = f'Página:{self.pageNumber:5} / {self.totalPages}' 
        self.page.update()


    # refresh product na home
    def refresh_products(self):

        # clear colCenter
        self.colCenter.controls.clear()

        # counter column product
        numberColumn = 0

        # row product
        rowProduct = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # iter
        for idx in range(self.initialIndex, self.initialIndex + self.qttyIndex):

            # load image
            image = ft.Image(src_base64=self.products[idx]['imagem'], width=200, height=180)

            # description product
            description = ft.Text(self.products[idx]['descricao'], width=200, max_lines=3, **txtLabelSmallStyle)

            # 
            price = ft.Text(f"R$ {self.products[idx]['preco']:8.2f}".replace('.', ','), **txtColorStyle)

            # container for description product
            colProduct = ft.Column([image, description, price], spacing=0)
            cntProduct = ft.Container(
                                colProduct,
                                data=self.products[idx],
                                padding=10,
                                on_click=self.main.on_click_image_product,
                                **cntStyle
                                )

            # add col in rowProduct
            rowProduct.controls.append(cntProduct)
            numberColumn+=1

            # check number column in row
            if numberColumn == 3:
                self.colCenter.controls.append(rowProduct)
                numberColumn=0
                rowProduct = ft.Row(alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START)

        # 
        self.colCenter.controls.append(rowProduct)

        # refresh text total pages
        self.refresh_text_total_pages()



class Home(HeaderApp, CrudHome):
        
    
    def __init__(self, main):
        HeaderApp.__init__(self, main)
        self.page = main.page
        self.main = main

        # row 
        self.row_header = ft.Row([self.cntHeaderMaster])
        self.row_body = ft.Row(alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START)
        self.row_footer = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

        # column master
        self.colMaster = ft.Column([self.row_header, self.row_body, self.row_footer])

        # colLeft category
        rowTitleCategory = ft.Row([ft.Text('Categorias', **txtTitleMediumStyle)])
        self.colCategory = ft.Column(scroll=ft.ScrollMode.ALWAYS, width=340, height=690)
        self.colLeft = ft.Column([rowTitleCategory, self.colCategory])

        # container for colLeft
        self.cntColLeft = ft.Container(self.colLeft, padding=10, **cntStyle)

        # colCenter products
        self.colCenter = ft.Column(width=720, scroll=ft.ScrollMode.ALWAYS, height=760)

        # colRight orderBy
        orderByOption=[
                ft.dropdown.Option("Crescente"),
                ft.dropdown.Option("Decrescente"),
                ft.dropdown.Option("Menor preço"),
                ft.dropdown.Option("Maior preço")]
        self.ddOrderBy = ft.Dropdown(label="Ordena por:",  on_change=self.on_change_order_by, **txtColorStyle)
        self.ddOrderBy.options = orderByOption
        self.colRight = ft.Container(ft.Column([self.ddOrderBy]), bgcolor="#e8eff7")
        
        # set controls in row body
        self.row_body.controls = [self.cntColLeft, self.colCenter, self.colRight]
        
        # orderBy
        self.orderBy = 'LOWER(descricao) ASC'

        # selected category
        self.selectedIdCategory = None
        self.whereClauseCategory = None
        self.indexSelectedCategory = None

        # navigation pages
        self.nav = NavigationPages(self)


    # clear enviroment
    def clear(self):
        self.selectedIdCategory = None
        self.whereClauseCategory = None
        self.indexSelectedCategory = None


    # get colMaster
    def get(self):
        return self.colMaster


    # show page
    def show(self):
        self.refresh()


    # refresh
    def refresh(self):

        # select product
        product = self.select_all_from_product()

        # config navigation pages
        self.nav.set_result(product)

        # select category
        category = self.select_all_from_category()
        self.set_category(category)


    # container product clicked
    def on_click_image_product(self, e):
        idProduct = e.control.data['id']
        self.main.prod_desc.set_product(idProduct)
        self.page.go('/product_description')


    # set category
    def set_category(self, allCategory):
        
        #
        self.colCategory.controls.clear()

        #
        for idx, cat in enumerate(allCategory):
            txtDescription = ft.Text(cat['descricao'], width=300, text_align=ft.TextAlign.LEFT)
            txtBtnCategoryDescription = ft.TextButton(content=txtDescription, data={'id_categoria':cat['id'], 'index':idx}, on_click=self.on_click_text_button_category)
            self.colCategory.controls.append(txtBtnCategoryDescription)
        self.page.update()
    

    # on change order by
    def on_change_order_by(self, e):
        self.orderBy = e.control.value

        # orderBy description ASC
        if self.orderBy == 'Crescente':
            self.orderBy = 'LOWER(descricao) ASC'
        
        # orderBy description DESC
        elif self.orderBy == 'Decrescente':
            self.orderBy = 'LOWER(descricao) DESC'

        # orderBy  price ASC
        elif self.orderBy == 'Menor preço':
            self.orderBy = 'preco ASC'

        # orderBy price DESC
        elif self.orderBy == 'Maior preço':
            self.orderBy = 'preco DESC'
        
        # call execute sql command
        self.make_exec_sql_command()


    # on click category
    def on_click_text_button_category(self, e):
        
        # change last category selected
        if self.indexSelectedCategory != None:
            self.colCategory.controls[self.indexSelectedCategory].style = ft.ButtonStyle(bgcolor="#e8eff7")
            self.colCategory.controls[self.indexSelectedCategory].content.color = ft.colors.BLUE_800

        # change bgcolor e font color
        if self.selectedIdCategory == e.control.data['id_categoria']:
            e.control.style = ft.ButtonStyle(bgcolor="#e8eff7")
            e.control.content.color = ft.colors.BLUE_800
            self.selectedIdCategory = None
            self.whereClauseCategory = None
            self.indexSelectedCategory = None

        else:
            e.control.style = ft.ButtonStyle(bgcolor=ft.colors.BLUE_800)
            e.control.content.color = ft.colors.WHITE
            self.selectedIdCategory = e.control.data['id_categoria']
            self.indexSelectedCategory = e.control.data['index']
            self.whereClauseCategory = f"WHERE id_categoria = '{e.control.data['id_categoria']}'"
        
        # call execute sql command
        self.make_exec_sql_command()


    # make sql command
    def make_exec_sql_command(self):
        if self.whereClauseCategory:
            sqlCommand = f"SELECT * FROM produto WHERE LOWER(descricao) LIKE '{self.searchProductDescription.value.lower()+'%'}' AND id_categoria = '{self.selectedIdCategory}'  AND situacao = 'Ativo' AND qtde > 0 ORDER BY {self.orderBy} LIMIT 500"
        else:
            sqlCommand = f"SELECT * FROM produto WHERE LOWER(descricao) LIKE '{self.searchProductDescription.value.lower()+'%'}' AND situacao = 'Ativo' AND qtde > 0 ORDER BY {self.orderBy} LIMIT 500"

        # refresh products
        products = self.select_from_product_order_by(sqlCommand)
        self.nav.set_result(products)
        self.page.update()