import logging
import os

import azure.functions as func
from azure.functions import AuthLevel

from models.product import Product
from shared.function_utils import APISuccessOK
from shared.product_operations import ProductOperations, handle_empty_request, handle_request_too_large

upsert_controller = func.Blueprint()


@upsert_controller.function_name("products_upsert")
@upsert_controller.route(route="products/upsert", methods=["POST"],
                          auth_level=AuthLevel.ANONYMOUS)
def product_upsert(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    headers = req.headers
    request_body: list[Product] = req.get_json()
    request_contents: bytes = req.get_body()
    conversation_id = headers.get("x-conversation-id", "")
    logging.info("Conversation Id: " + conversation_id)

    maximum_request_size = int(os.environ.get("MAXIMUM_REQUEST_SIZE", "262144"))
    maximum_batch_count = int(os.environ.get("MAXIMUM_BATCH_INBOUND_RECORDS", "100"))

    content_length = len(request_contents)
    batch_size = len(request_body)

    # handles empty requests (used for testing connectivity with ASA)
    if content_length == 0 or batch_size == 0:
        return handle_empty_request()

    # handles large request exceeding batch size from ASA
    if content_length > maximum_request_size or batch_size > maximum_batch_count:
        return handle_request_too_large(content_length, batch_size)

    operations = ProductOperations()
    result = operations.handle_upsert(request_body)
    return APISuccessOK(result).build_response()
