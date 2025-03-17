import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from gestion_stock import *

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.stock = Stock(config)
        
        # Frame principal
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titre
        self.title_label = tk.Label(self.main_frame, text="Gestion de Stock", font=("Arial", 18, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=10)
        
        # Frame pour les onglets
        self.tabs = ttk.Notebook(self.main_frame)
        self.tabs.pack(fill=tk.BOTH, expand=True)
        
        # Onglet Affichage
        self.display_tab = tk.Frame(self.tabs, bg="#f5f5f5")
        self.tabs.add(self.display_tab, text="Affichage")
        self.setup_display_tab()
        
        # Onglet Création
        self.create_tab = tk.Frame(self.tabs, bg="#f5f5f5")
        self.tabs.add(self.create_tab, text="Créer Produit")
        self.setup_create_tab()
        
        # Onglet Modification
        self.modify_tab = tk.Frame(self.tabs, bg="#f5f5f5")
        self.tabs.add(self.modify_tab, text="Modifier Produit")
        self.setup_modify_tab()
        
        # Onglet Suppression
        self.delete_tab = tk.Frame(self.tabs, bg="#f5f5f5")
        self.tabs.add(self.delete_tab, text="Supprimer Produit")
        self.setup_delete_tab()
        
        # Actualisation initiale
        self.refresh_product_table()
        
    def setup_display_tab(self):
        # Frame pour le tableau
        table_frame = tk.Frame(self.display_tab, bg="#f5f5f5")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Création du tableau (Treeview)
        columns = ("ID", "Nom", "Description", "Prix", "Quantité", "Catégorie")
        self.product_table = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Configuration des en-têtes
        for col in columns:
            self.product_table.heading(col, text=col)
            self.product_table.column(col, width=100)
        
        # Ajout d'une barre de défilement
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.product_table.yview)
        self.product_table.configure(yscroll=scrollbar.set)
        
        # Placement du tableau et de la barre de défilement
        self.product_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bouton d'actualisation
        refresh_button = tk.Button(
            self.display_tab, 
            text="Actualiser", 
            command=self.refresh_product_table,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        refresh_button.pack(pady=10)
    
    def setup_create_tab(self):
        create_frame = tk.Frame(self.create_tab, bg="#f5f5f5")
        create_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        tk.Label(create_frame, text="Ajouter un nouveau produit", font=("Arial", 14, "bold"), bg="#f5f5f5").grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        # Champs de saisie
        fields = [
            ("Nom:", "name_entry"),
            ("Description:", "desc_entry"),
            ("Prix:", "price_entry"),
            ("Quantité:", "quantity_entry"),
            ("ID Catégorie:", "category_entry")
        ]
        
        for i, (label_text, attr_name) in enumerate(fields):
            tk.Label(create_frame, text=label_text, bg="#f5f5f5", font=("Arial", 10)).grid(row=i+1, column=0, pady=5, sticky="w")
            entry = tk.Entry(create_frame, width=40)
            entry.grid(row=i+1, column=1, pady=5, padx=10, sticky="w")
            setattr(self, attr_name, entry)
        
        # Bouton de création
        create_button = tk.Button(
            create_frame, 
            text="Créer Produit",
            command=self.create_product,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        create_button.grid(row=len(fields)+1, column=0, columnspan=2, pady=15)
    
    def setup_modify_tab(self):
        modify_frame = tk.Frame(self.modify_tab, bg="#f5f5f5")
        modify_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        tk.Label(modify_frame, text="Modifier un produit", font=("Arial", 14, "bold"), bg="#f5f5f5").grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        # ID du produit
        tk.Label(modify_frame, text="ID du produit:", bg="#f5f5f5", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="w")
        self.modify_id_entry = tk.Entry(modify_frame, width=10)
        self.modify_id_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        
        # Type de modification
        tk.Label(modify_frame, text="Choisir:", bg="#f5f5f5", font=("Arial", 10)).grid(row=2, column=0, pady=5, sticky="w")
        self.modify_type = tk.StringVar()
        modify_options = ttk.Combobox(modify_frame, textvariable=self.modify_type, width=15)
        modify_options['values'] = ('Prix', 'Quantité')
        modify_options.current(0)
        modify_options.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        
        # Nouvelle valeur
        tk.Label(modify_frame, text="Nouvelle valeur:", bg="#f5f5f5", font=("Arial", 10)).grid(row=3, column=0, pady=5, sticky="w")
        self.new_value_entry = tk.Entry(modify_frame, width=20)
        self.new_value_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        
        # Bouton de modification
        modify_button = tk.Button(
            modify_frame, 
            text="Modifier Produit",
            command=self.modify_product,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        modify_button.grid(row=4, column=0, columnspan=2, pady=15)
    
    def setup_delete_tab(self):
        delete_frame = tk.Frame(self.delete_tab, bg="#f5f5f5")
        delete_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titre
        tk.Label(delete_frame, text="Supprimer un produit", font=("Arial", 14, "bold"), bg="#f5f5f5").grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        # ID du produit
        tk.Label(delete_frame, text="ID du produit:", bg="#f5f5f5", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="w")
        self.delete_id_entry = tk.Entry(delete_frame, width=10)
        self.delete_id_entry.grid(row=1, column=1, pady=5, padx=10, sticky="w")
        
        # Bouton de suppression
        delete_button = tk.Button(
            delete_frame, 
            text="Supprimer Produit",
            command=self.delete_product,
            bg="#F44336",
            fg="white",
            font=("Arial", 10),
            padx=10
        )
        delete_button.grid(row=2, column=0, columnspan=2, pady=15)
    
    def refresh_product_table(self):
        # Effacer les données existantes
        for item in self.product_table.get_children():
            self.product_table.delete(item)
        
        try:
            # Récupérer les données
            self.stock.cursor.execute("SELECT * FROM product")
            products = self.stock.cursor.fetchall()
            
            # Ajouter les données au tableau
            for product in products:
                self.product_table.insert("", tk.END, values=product)
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des produits: {e}")
    
    def create_product(self):
        try:
            name = self.name_entry.get()
            description = self.desc_entry.get()
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())
            category_id = int(self.category_entry.get())
            
            if not name:
                messagebox.showwarning("Attention", "Le nom du produit est obligatoire")
                return
                
            self.stock.create_product(name, description, price, quantity, category_id)
            messagebox.showinfo("Succès", "Produit créé avec succès")
            
            # Vider les champs
            for entry in [self.name_entry, self.desc_entry, self.price_entry, self.quantity_entry, self.category_entry]:
                entry.delete(0, tk.END)
                
            # Actualiser l'affichage
            self.refresh_product_table()
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir des valeurs numériques valides pour le prix, la quantité et l'ID de catégorie")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création du produit: {e}")
    
    def modify_product(self):
        try:
            product_id = int(self.modify_id_entry.get())
            new_value = self.new_value_entry.get()
            
            if not product_id or not new_value:
                messagebox.showwarning("Attention", "Veuillez remplir tous les champs")
                return
                
            # Convertir en valeur numérique
            new_value = float(new_value) if self.modify_type.get() == 'Prix' else int(new_value)
            
            # Déterminer la colonne à modifier
            column = "price" if self.modify_type.get() == 'Prix' else "quantity"
            
            # Exécuter la requête de modification
            query = f"UPDATE product SET {column} = %s WHERE id = %s"
            self.stock.cursor.execute(query, (new_value, product_id))
            self.stock.connection.commit()
            
            messagebox.showinfo("Succès", f"Produit #{product_id} modifié avec succès")
            
            # Vider les champs
            self.modify_id_entry.delete(0, tk.END)
            self.new_value_entry.delete(0, tk.END)
            
            # Actualiser l'affichage
            self.refresh_product_table()
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir des valeurs numériques valides")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification du produit: {e}")
    
    def delete_product(self):
        try:
            product_id = int(self.delete_id_entry.get())
            
            if not product_id:
                messagebox.showwarning("Attention", "Veuillez saisir l'ID du produit")
                return
                
            # Vérifier si le produit existe
            self.stock.cursor.execute("SELECT name FROM product WHERE id = %s", (product_id,))
            product = self.stock.cursor.fetchone()
            
            if not product:
                messagebox.showerror("Erreur", f"Aucun produit trouvé avec l'ID {product_id}")
                return
                
            # Confirmer la suppression
            confirm = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer le produit {product[0]} ?")
            
            if confirm:
                # Exécuter la suppression
                self.stock.cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
                self.stock.connection.commit()
                
                messagebox.showinfo("Succès", f"Produit {product[0]} supprimé avec succès")
                
                # Vider le champ
                self.delete_id_entry.delete(0, tk.END)
                
                # Actualiser l'affichage
                self.refresh_product_table()
            
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez saisir un ID valide")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
