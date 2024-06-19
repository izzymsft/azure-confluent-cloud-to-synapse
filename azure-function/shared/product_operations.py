import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text
from models.product import Product


class ProductOperations:

    def __init__(self):
        connection_string = os.environ.get("AZURE_SQL_CONNECTION_STRING")
        self.product_table_name = "product_data"  # this will store all the INSERT and UPDATES
        self.product_count_table = "product_tracking"  # this will keep track of all the products we have seen so far
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        self.engine = create_engine(connection_url)

    def prepare_product_rows(self, products: list[Product]) -> str:
        records: list[str] = []
        for product in products:
            records.append(self.prepare_product_row(product))

        return ", ".join(records)

    def prepare_row_accumulations(self, products: list[Product]) -> str:
        records: list[str] = []
        for product in products:
            product_id = product['product_id']
            record_count = 1
            row = f"({product_id}, {record_count})"
            records.append(row)

        return ", ".join(records)

    def prepare_product_row(self, record: Product):
        identifier: int = record['product_id']
        name: str = record['product_name']
        price: float = record['product_price']
        coupon_code: str = record['coupon_code']
        description: str = record['product_description']
        active: int = int(record['active_product'])

        return f"({identifier}, '{name}', {price}, '{coupon_code}', '{description}', {active})"

    def handle_insert(self, products: list[Product]):
        connection = self.engine.connect()
        table_name = self.product_table_name

        insert_values = self.prepare_product_rows(products)
        sql_statement = text(
            f"INSERT INTO {table_name} (product_id, product_name, product_price, coupon_code, product_description, "
            f"active_product) VALUES {insert_values}")

        result = connection.execute(sql_statement)

        connection.commit()
        connection.close()

        return sql_statement

    def handle_upsert(self, products: list[Product]):
        connection = self.engine.connect()
        table_name = self.product_table_name
        upsert_values = self.prepare_product_rows(products)

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

        result = connection.execute(text(sql_string))

        connection.commit()
        connection.close()

        return sql_string

    def handle_accumulate(self, products: list[Product]):
        connection = self.engine.connect()
        table_name = self.product_table_name
        row_values = self.prepare_row_accumulations(products)

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

        return sql_string
