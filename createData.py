"""
Generate random receipts and save them to a CSV file.

This script generates random sales receipts containing random items and quantities,
calculates the total price for each receipt, and saves the receipts to a CSV file.

Parameters:
- list_items: A list of dictionaries containing items and their prices.
- num_receipts: The number of receipts to generate.

Returns:
- receipts: A list of dictionaries representing the generated receipts.
- filename: The filename of the CSV file where the receipts are saved.
"""

import random
import csv

daftar_barang_dan_harga = [
    {"nama": "Sprite", "harga": 10000},
    {"nama": "Susu", "harga": 15000},
    {"nama": "Chitos", "harga": 12000},
    {"nama": "Telur", "harga": 20000},
    {"nama": "Roti", "harga": 25000},
    {"nama": "Oatmeal Instan", "harga": 30000},
    {"nama": "Kit Kat", "harga": 5000},
    {"nama": "prochiz", "harga": 25000},
    {"nama": "Minyak Kayu Putih", "harga": 15000},
    {"nama": "Air Mineral", "harga": 3000},
    {"nama": "Rokok", "harga": 20000},
    {"nama": "Silver Queen", "harga": 10000},
    {"nama": "Taro", "harga": 15000},
    {"nama": "Ultra Milk", "harga": 10000},
    {"nama": "Pepperoni", "harga": 25000},
    {"nama": "Anggur", "harga": 30000},
    {"nama": "Cupcakes", "harga": 5000},
    {"nama": "Muffin", "harga": 25000},
    {"nama": "Lemon", "harga": 30000},
    {"nama": "Tomat", "harga": 25000},
    {"nama": "Yogurt", "harga": 10000},
    {"nama": "Ayam Goreng", "harga": 50000},
    {"nama": "Sepatu", "harga": 150000},
    {"nama": "Kopi", "harga": 20000},
    {"nama": "Baju Anak", "harga": 50000},
    {"nama": "Jus Buah", "harga": 15000},
    {"nama": "Daging Sapi Segar", "harga": 75000},
    {"nama": "Vitamin D", "harga": 20000},
    {"nama": "Paracetamol", "harga": 30000},
    {"nama": "Sapu", "harga": 30000},
    {"nama": "Popok Bayi Sekali Pakai", "harga": 50000},
    {"nama": "Mayonnaise", "harga": 20000},
    {"nama": "Celana Jeans", "harga": 25000},
    {"nama": "Pensil", "harga": 3000},
    {"nama": "Spidol", "harga": 10000},
    {"nama": "Penghapus", "harga": 5000},
    {"nama": "Bulpen", "harga": 10000},
    {"nama": "Lifebuoy Body Wash", "harga": 30000},
    {"nama": "Sikat Gigi", "harga": 20000},
    {"nama": "Pasta Gigi", "harga": 15000},
    {"nama": "Vitamin C", "harga": 50000},
    {"nama": "Head & Shoulders", "harga": 60000},
    {"nama": "Sabun Cuci Muka", "harga": 25000},
    {"nama": "Gunting", "harga": 30000},
    {"nama": "Kipas Angin", "harga": 100000},
    {"nama": "Gayung", "harga": 20000},
    {"nama": "Seafood Beku", "harga": 75000},
    {"nama": "Ember", "harga": 30000},
    {"nama": "Decolgen", "harga": 30000},
    {"nama": "Earphone", "harga": 50000},
    {"nama": "Penggaris", "harga": 15000},
    {"nama": "Teh", "harga": 10000},
    {"nama": "Voucher Goggle Play", "harga": 50000},
    {"nama": "Voucher Garena", "harga": 100000},
    {"nama": "Voucher Steam", "harga": 10000},
    {"nama": "Promag", "harga": 10000},
    {"nama": "Panadol", "harga": 5000},
]

def generate_random_receipts(list_items, num_receipts):
    """
    Generate random sales receipts.

    Parameters:
    - list_items: A list of dictionaries containing items and their prices.
    - num_receipts: The number of receipts to generate.

    Returns:
    - receipts: A list of dictionaries representing the generated receipts.
    """
    
    receipts = []

    for receipt_id in range(91, num_receipts + 91):
        receipt = []
        num_items = 10 # Random number of items per receipt
        chosen_items = random.sample(list_items, num_items)  # Randomly choose items
        total_price = 0

        for item in chosen_items:
            quantity = random.randint(1, 10)  # Random quantity between 1 and 10
            item_total = quantity * item['harga']
            total_price += item_total
            receipt.append({'Receipt ID': receipt_id, 'Item': item['nama'], 'Quantity': quantity, 'Price': item['harga'], 'Item Total': item_total})

        receipt.append(
            {'Receipt ID': receipt_id, 'Item': 'TOTAL', 'Quantity': '', 'Price': '', 'Item Total': total_price})
        receipts.append(receipt)

    return receipts


def save_receipts_to_csv(receipts, filename):
    """
    Save the generated receipts to a CSV file.

    Parameters:
    - receipts: A list of dictionaries representing the generated receipts.
    - filename: The filename of the CSV file to save the receipts.
    """
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Receipt ID', 'Item', 'Quantity', 'Price', 'Item Total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for receipt in receipts:
            for item in receipt:
                writer.writerow(item)
            writer.writerow({})  # Add an empty row to separate receipts


# Parameters
num_receipts = 10  # Number of receipts to generate

# Generate random receipts
random_receipts = generate_random_receipts(daftar_barang_dan_harga, num_receipts)

# Save the receipts to a CSV file
csv_filename = 'receipts10.csv'
save_receipts_to_csv(random_receipts, csv_filename)

print(f"Random receipts saved to {csv_filename}")
