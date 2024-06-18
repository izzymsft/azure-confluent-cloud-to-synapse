import json
import os

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, VARCHAR, NVARCHAR
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import event, DDL, text

from models.product import Product


class ProductOperations:

    def __init__(self):
        connection_string = os.environ.get("AZURE_SQL_CONNECTION_STRING")
        self.product_table_name = "products"  # this will store all the INSERT and UPDATES
        self.product_count_table = "product_counts"  # this will keep track of all the products we have seen so far
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        self.engine = create_engine(connection_url)

    def handle_inserts(self, products: list[Product]):
        connection = self.engine.connect()
        sql_statement = text("")
        parameters = {}

        result = connection.execute(sql_statement, parameters)
