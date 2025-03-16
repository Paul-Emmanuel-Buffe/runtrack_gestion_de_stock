import mysql.connector

class Stock:
    def __init__(self, config):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def create_product(self, name, description, price, quantity, id_category): 
        query = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s,%s,%s,%s,%s)"
        try: 
           self.cursor.execute(query, (name, description, price, quantity, id_category))
           self.connection.commit()
           print("Product recorded")
        except Exception as e: 
            self.connection.rollback()
            print(f"An error occured: {e}")

    def stock_product_display(self):
        
        query = "SELECT * FROM product"
        
        try:
            self.cursor.execute(query)
            for row in self.cursor.fetchall():
                print(row)
        except Exception as e:
            self.connection.rollback()
            print(f"An error occured: {e}")

    def delete_product(self):

        try:
            id = int(input("Enter the ID product you want to delete: "))
            select_query = 'SELECT name FROM product WHERE id = %s'
            self.cursor.execute(select_query,(id,))     
            product_name = self.cursor.fetchone()  

            if product_name:
                product_name = product_name[0]
                query = 'DELETE FROM product WHERE id = %s'
                self.cursor.execute(query,(id,))
                self.connection.commit()
                print(f'{product_name} deleted')
            
            else:
                print(f'No product found with the id {id}.')

        except Exception as e:
            self.connection.rollback()
            print(f"An error occured: {e}")            
                      



    
    #def modify_product(self):

config = {
    "user" : "root",
    "password" : "cN06+#P34",
    "host" : "localhost",
    "database" : "store",
    "port" : 3306
}

store = Stock(config)

store.delete_product()

store.stock_product_display()