import json
import logging
import os

import azure.functions as func
from azure.functions import AuthLevel

from models.product import Product
from shared.function_utils import APIContentTooLarge, APISuccessNoContent
from shared.stream_analytics_operations import StreamAnalyticsOperation

products_controller = func.Blueprint()


@products_controller.function_name("products_controller")
@products_controller.route(route="products/{operation?}", methods=["POST"],
                           auth_level=AuthLevel.ANONYMOUS)
def ask_elizabeth(req: func.HttpRequest) -> func.HttpResponse:
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

    operation_name: StreamAnalyticsOperation = req.route_params.get('operation', None)

    if operation_name == StreamAnalyticsOperation.UPSERT:
        return handle_product_upsert(request_body)
    elif operation_name == StreamAnalyticsOperation.INSERT:
        return handle_product_insert(request_body)
    elif operation_name == StreamAnalyticsOperation.ACCUMULATE:
        return handle_products_accumulation_count(request_body)
    else:
        return handle_undefined_operation(request_body)


def handle_request_too_large(row_count: int, content_length: int) -> func.HttpResponse:
    response = {"message": "Request size too large", "row_count": row_count, "content_length": content_length}
    json_string = json.dumps(response)
    return APIContentTooLarge(json_string).build_response()


def handle_empty_request() -> func.HttpResponse:
    return APISuccessNoContent().build_response()


def handle_undefined_operation(request_body: list[Product]) -> func.HttpResponse:
    return None


def handle_product_upsert(request_body: list[Product]) -> func.HttpResponse:
    return None


def handle_product_insert(request_body: list[Product]) -> func.HttpResponse:
    return None


def handle_products_accumulation_count(request_body: list[Product]) -> func.HttpResponse:
    return None
