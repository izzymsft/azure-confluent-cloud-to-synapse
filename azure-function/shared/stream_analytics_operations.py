from enum import StrEnum


class StreamAnalyticsOperation(StrEnum):
    """The different operation types supported by Azure Stream Analytics (ASA)"""
    UPSERT = "upsert"  # inserts new records IF NOT EXIST and updates if the key exists
    INSERT = "insert"  # inserts all records as new
    ACCUMULATE = "accumulation"  # increments the product count by the total number of records received
