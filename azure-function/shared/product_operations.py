import json
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text

import azure.functions as func

from models.product import Product
from shared.function_utils import APIContentTooLarge, APISuccessNoContent


class ProductOperations:

    def __init__(self):
        connection_string = os.environ.get("AZURE_SQL_CONNECTION_STRING")
        self.product_table_name = "product_data"  # this will store all the INSERT and UPDATES
        self.product_count_table = "product_tracking"  # this will keep track of all the products we have seen so far
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        self.engine = create_engine(connection_url)

    def __prepare_product_rows(self, products: list[Product]) -> str:
        records: list[str] = []
        for product in products:
            records.append(self.__prepare_product_row(product))

        return ", ".join(records)

    @staticmethod
    def __prepare_row_accumulations(products: list[Product]) -> str:
        records: list[str] = []
        for product in products:
            product_id = product['product_id']
            record_count = 1
            row = f"({product_id}, {record_count})"
            records.append(row)

        return ", ".join(records)

    def __prepare_product_row(self, record: Product):
        identifier: int = record['product_id']
        name: str = self.sanitize_string(record['product_name'])
        price: float = record['product_price']
        coupon_code: str = self.sanitize_string(record['coupon_code'])
        description: str = self.sanitize_string(record['product_description'])
        active: int = int(record['active_product'])

        return f"({identifier}, '{name}', {price}, '{coupon_code}', '{description}', {active})"

    def handle_upsert(self, products: list[Product]):
        connection = self.engine.connect()
        table_name = self.product_table_name
        upsert_values = self.__prepare_product_rows(products)

        sql_string = """
        MERGE INTO [{}] t
        USING ( VALUES {} ) AS v (product_id, product_name, product_price, coupon_code, product_description, active_product)
        ON t.product_id = v.product_id
        -- Replace when the key exists
        WHEN MATCHED THEN
            UPDATE SET
                t.product_name = v.product_name,
                t.product_price = v.product_price,
                t.coupon_code = v.coupon_code,
                t.product_description = v.product_description,
                t.active_product = v.active_product
        -- Insert new keys
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (product_id, product_name, product_price, coupon_code, product_description, active_product)
            VALUES (v.product_id, v.product_name, v.product_price, 
            v.coupon_code, v.product_description, v.active_product);
        """.format(table_name, upsert_values)

        statement = text(sql_string)
        result = connection.execute(statement)

        print(sql_string)

        connection.commit()
        connection.close()

        return sql_string

    def handle_accumulate(self, products: list[Product]):
        connection = self.engine.connect()
        table_name = self.product_count_table
        row_values = self.__prepare_row_accumulations(products)

        sql_string = """
        MERGE INTO [{}] t
        USING ( VALUES {} ) AS v (product_id, transaction_count)
        ON t.product_id = v.product_id
        -- Replace when the key exists
        WHEN MATCHED THEN
            UPDATE SET
                t.transaction_count += v.transaction_count
        -- Insert new keys
        WHEN NOT MATCHED BY TARGET THEN
            INSERT (product_id, transaction_count)
            VALUES (v.product_id, v.transaction_count);
        """.format(table_name, row_values)

        result = connection.execute(text(sql_string))

        connection.commit()
        connection.close()

        print(sql_string)

        return sql_string

    def handle_delete(self, products: list[Product]):
        connection = self.engine.connect()
        table_name = self.product_table_name
        upsert_values = self.__prepare_product_rows(products)

        sql_string = """
        MERGE INTO [{}] t
        USING ( VALUES {} ) AS v (product_id)
        ON t.product_id = v.product_id
        -- Replace when the key exists
        WHEN MATCHED THEN
           DELETE;
        """.format(table_name, upsert_values)

        statement = text(sql_string)
        result = connection.execute(statement)

        print(sql_string)

        connection.commit()
        connection.close()

        return sql_string

    @staticmethod
    def sanitize_string(input_string: str) -> str:
        """
        Sanitizes a string for insertion into SQL database by escaping potentially dangerous characters.

        Args:
        input_string (str): The string to be sanitized.

        Returns:
        str: The sanitized string.
        """
        if input_string is None:
            return None

        if not isinstance(input_string, str):
            raise ValueError("Input must be a string")

        # Replace single quotes with two single quotes to escape them
        sanitized_string = input_string.replace("'", "''")

        # Add more replacements if necessary, e.g., for backslashes
        sanitized_string = sanitized_string.replace("\\", "\\\\")

        # Optionally remove any other unwanted characters
        sanitized_string = re.sub(r'[^\w\s]', '', sanitized_string)

        return sanitized_string


def handle_request_too_large(row_count: int, content_length: int) -> func.HttpResponse:
    response = {"message": "Request size too large", "row_count": row_count, "content_length": content_length}
    json_string = json.dumps(response)
    return APIContentTooLarge(json_string).build_response()


def handle_empty_request() -> func.HttpResponse:
    return APISuccessNoContent().build_response()