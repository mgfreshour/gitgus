from .sobjects.product_tag import ProductTag


class Products:
    def get_product_tag(self, product_tag_name):
        return list(ProductTag.soql_query(f"WHERE Name LIKE '%{product_tag_name}%'"))
