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
                      


    def select_entry_feature(self, column_choice):
        match column_choice:
            case 1:
                return "price"
            case 2:
                return "quantity"
            case _:
                  return None
    
    def modify_product(self):
        try: 
            id = int(input("Enter the product ID you want modify: "))
            column_choice = int(input("Select change:\n 1.Change Price\n 2.Change Quantity\nYour Choice: "))
            new_value= int(input('Enter new value: '))
            
            column = self.select_entry_feature(column_choice)
            if column is None:
                print("Invalid selection")
                return

            query= f'UPDATE product SET {column} = %s WHERE id = %s'
            self.cursor.execute(query,(new_value,id))
            self.connection.commit()
            print(f'Product {id} updated successfully')
        except Exception as e:
            self.connection.rollback()
            print(f'An error occurred: {e}')

config = {
    "user" : "root",
    "password" : "cN06+#P34",
    "host" : "localhost",
    "database" : "store",
    "port" : 3306
}

store = Stock(config)

store.stock_product_display()

store.modify_product()

store.stock_product_display()