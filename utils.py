import flet as ft
import pathlib
import base64
import re


# style for Container
cntStyle = {
    'bgcolor':"#e8eff7",
    'border_radius':10,
    'border':ft.border.all(1, color=ft.colors.BLUE_900)
}


# style for text
txtColorStyle = {
    'color':ft.colors.BLUE_800
}


# style for Text Label Small
txtLabelSmallStyle = {
    'color':ft.colors.BLUE_800,
    'theme_style':ft.TextThemeStyle.LABEL_SMALL
}


# style for Text Title Small
txtTitleSmallStyle = {
    'color':ft.colors.BLUE_800,
    'theme_style':ft.TextThemeStyle.TITLE_SMALL
}


# style for Text Title Medium
txtTitleMediumStyle = {
    'color':ft.colors.BLUE_800,
    'theme_style':ft.TextThemeStyle.TITLE_MEDIUM
}


# style for Text Title Large
txtTitleLargeStyle = {
    'color':ft.colors.BLUE_800,
    'theme_style':ft.TextThemeStyle.TITLE_LARGE
}


# style for TextField
txtFldBorderColorStyle = {
    'border_color':ft.colors.BLUE_800
}


# show message warning
def show_snack_bar_warning(page, message):
    page.snack_bar = ft.SnackBar(ft.Text(message, color=ft.colors.WHITE), bgcolor=ft.colors.RED_800)
    page.snack_bar.open = True
    page.update()


# show message information
def show_snack_bar_info(page, message):
    page.snack_bar = ft.SnackBar(ft.Text(message, color=ft.colors.WHITE), bgcolor=ft.colors.BLUE_900)
    page.snack_bar.open = True
    page.update()


# directoru working
directoryWorking=str(pathlib.Path(__file__).parent.absolute()) + '\\'


# convert image to base64
def convert_image_base64(image_local):
    with open(image_local, "rb") as image_file:
          convertImgToString = base64.b64encode(image_file.read()).decode()
    return convertImgToString



# validate cep
def validate_cep(cep):

    # Verifica a formatação do CPF
    if not re.match(r'\d{5}-\d{3}', cep):
        return False
    else:
        return True


# validate email
def validate_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, email):
        return True
    else:
        return False


# validate cpf
def validate_cpf(cpf: str) -> bool:

    # Verifica a formatação do CPF
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False
    
    # Obtém apenas os números do CPF, ignorando pontuações
    numbers = [int(digit) for digit in cpf if digit.isdigit()]
    
    # Verifica se o CPF possui 11 números ou se todos são iguais
    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False
    
    # Validação do primeiro dígito verificador
    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False
    
    # Validação do segundo dígito verificador
    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False
    
    return True




# show message information
class Message:
    
    # show message
    def __init__(self, page, message):
        
        # show message information
        msg = ft.AlertDialog(title=ft.Text(message))
        page.dialog = msg
        msg.open = True
        page.update()



# show message information with confirm option
class MessageConfirm:

    def __init__(self, page, title, message):
        self.page = page

        # flag for message confirm yes or no, 
        self.dialogResponse = None

        # alert dialog with confirm options
        self.msgConfirm = ft.AlertDialog(
                            modal=True,
                            title=ft.Text(title),
                            content=ft.Text(message),
                            actions=[
                                    ft.TextButton("Sim", on_click=self.answer_yes),
                                    ft.TextButton("Não", on_click=self.answer_no),
                            ],
                            actions_alignment=ft.MainAxisAlignment.END
                            )        
        
        # config show message dialog
        self.page.dialog = self.msgConfirm
        self.msgConfirm.open = True
        self.page.update()


    # answer yes
    def answer_yes(self, e):
        self.dialogResponse = True
        self.msgConfirm.open = False
        self.page.update()


    # answer no
    def answer_no(self, e):
        self.dialogResponse = False
        self.msgConfirm.open = False
        self.page.update()