import azure.functions as func

from controllers.product_deletes import delete_controller
from controllers.product_accumulation import accumulate_controller
from controllers.product_upserts import upsert_controller

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

app.register_functions(upsert_controller)
app.register_functions(delete_controller)
app.register_functions(accumulate_controller)
