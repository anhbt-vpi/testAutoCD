username = 'anhbt@vpi.pvn.vn'
password = ''
driver = '{ODBC Driver 18 for SQL Server}'

lookup_table = {
    "server": "xznozrobo3funm76yoyaoh75wm-tkjpmh452t6utd6ixztthtmnoa.datamart.pbidedicated.windows.net",
    "database": "ProductInfo",
    "tableName": "Table"
}

error_message = {
    "missing_product": "Missing product. Please check your product again",
    "product_not_found": "Product not found. Please check your product again",
    "table_not_found": "Table not found. Please check your table name again"
}

endpoints = {
    "datamart": "/products/{product}/international/price/daily"
}
