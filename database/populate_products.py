import sqlite3

DATABASE = 'database/app.db'

def populate_products():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Optional: Clean old products
    c.execute('DELETE FROM products')

    sample_products = [
        # Produtos para consumidores
        ("Pacote de Bolachas Maria", 2, "2025-12-31", 1.19, 0.36, "bolacha.jpg", "Continente Marcas", "Continente Telheiras", "consumer"),
        ("Garrafa de Leite Meio-Gordo", 3, "2025-06-15", 0.89, 0.27, "leite.jpg", "Agros", "Continente Amadora", "consumer"),
        ("Detergente Limpeza Ativa", 2, "2026-01-20", 7.49, 2.25, "detergente.jpg", "Continente Saúde", "Continente Loures", "consumer"),
        ("Iogurte Natural Pack 6", 3, "2025-05-10", 2.29, 0.69, "iogurte.jpg", "Danone", "Continente Colombo", "consumer"),
        ("Pacote de Arroz Carolino", 4, "2026-08-30", 0.79, 0.24, "arroz.jpg", "Milaneza", "Continente Oeiras", "consumer"),
        ("Maçãs Golden", 6, "2025-05-20", 2.99, 0.90, "macas.jpg", "Frutas Continente", "Continente Cascais", "consumer"),

        # Produtos para organizações
        ("Saco de Batatas 20kg", 10, "2025-10-15", 16.50, 4.95, "sacobatatas.jpg", "Agrícola Nacional", "Continente Sintra", "organization"),
        ("Caixa de Águas 24x0.5L", 8, "2025-07-01", 4.49, 1.35, "agua.jpg", "Águas Luso", "Continente Alfragide", "organization"),
        ("Palete de Arroz Agulha 30kg", 5, "2026-01-01", 190.00, 57.00, "arroz.jpg", "Orivárzea", "Continente Odivelas", "organization"),
        ("Detergente Limpeza Ativa", 12, "2027-03-12", 39.90, 11.97, "detergente.jpg", "Continente Limpeza", "Continente Seixal", "organization"),
        ("Palete de Papel Higiénico", 6, "2027-06-01", 220.00, 66.00, "papel.jpg", "Renova", "Continente Almada", "organization"),
        ("Saco de Cebolas 25kg", 7, "2025-09-15", 14.90, 4.47, "cebolas.jpg", "Hortícolas do Oeste", "Continente Torres Vedras", "organization"),
    ]
    c.executemany('''
        INSERT INTO products (name, quantity, expiration_date, price, discounted_price, image, supplier, location, target_user_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_products)

    conn.commit()
    conn.close()
    print("Produtos populados com sucesso!")

if __name__ == "__main__":
    populate_products()
