from database.DB_connect import DBConnect
from model.category import Category
from model.product import Product


class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last



    @staticmethod
    def get_category():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                   from category """

        cursor.execute(query)

        for row in cursor:
            result.append(Category(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def get_product(cat):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                   from product p 
                   where p.category_id =%s
                     """

        cursor.execute(query,(cat.id,))

        for row in cursor:
            result.append(Product(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_product_vendite(cat_id, data1, data2):

        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT p.id, count(*) as vendite
            FROM product p, order_item oi, `order` o
            WHERE p.category_id = %s 
              AND p.id = oi.product_id 
              AND oi.order_id = o.id 
              AND o.order_date BETWEEN %s AND %s
            GROUP BY p.id
        """

        cursor.execute(query, (cat_id.id, data1, data2))

        for row in cursor:
            result[row['id']] = row['vendite']

        cursor.close()
        conn.close()
        return result