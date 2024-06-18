import azure.functions as func

from controllers.products import products_controller

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_functions(products_controller)
