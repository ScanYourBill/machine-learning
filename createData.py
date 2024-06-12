import random
import csv


daftar_barang_dan_harga = [
    {"nama": "Sprite", "harga": 10000, "kategori": "Food"},
    {"nama": "Susu", "harga": 15000, "kategori": "Food"},
    {"nama": "Chitos", "harga": 12000, "kategori": "Food"},
    {"nama": "Telur", "harga": 20000, "kategori": "Food"},
    {"nama": "Roti", "harga": 25000, "kategori": "Food"},
    {"nama": "Oatmeal Instan", "harga": 30000, "kategori": "Food"},
    {"nama": "Kit Kat", "harga": 5000, "kategori": "Food"},
    {"nama": "prochiz", "harga": 25000, "kategori": "Food"},
    {"nama": "Minyak Kayu Putih", "harga": 15000, "kategori": "Medical and Health Care"},
    {"nama": "Air Mineral", "harga": 3000, "kategori": "Food"},
    {"nama": "Rokok", "harga": 20000, "kategori": "Others"},
    {"nama": "Silver Queen", "harga": 10000, "kategori": "Food"},
    {"nama": "Taro", "harga": 15000, "kategori": "Food"},
    {"nama": "Ultra Milk", "harga": 10000, "kategori": "Food"},
    {"nama": "Pepperoni", "harga": 25000, "kategori": "Food"},
    {"nama": "Anggur", "harga": 30000, "kategori": "Food"},
    {"nama": "Cupcakes", "harga": 5000, "kategori": "Food"},
    {"nama": "Muffin", "harga": 25000, "kategori": "Food"},
    {"nama": "Lemon", "harga": 30000, "kategori": "Food"},
    {"nama": "Tomat", "harga": 25000, "kategori": "Food"},
    {"nama": "Yogurt", "harga": 10000, "kategori": "Food"},
    {"nama": "Ayam Goreng", "harga": 50000, "kategori": "Food"},
    {"nama": "Sepatu", "harga": 150000, "kategori": "Clothing"},
    {"nama": "Kopi", "harga": 20000, "kategori": "Food"},
    {"nama": "Baju Anak", "harga": 50000, "kategori": "Clothing"},
    {"nama": "Jus Buah", "harga": 15000, "kategori": "Food"},
    {"nama": "Daging Sapi Segar", "harga": 75000, "kategori": "Food"},
    {"nama": "Vitamin D", "harga": 20000, "kategori": "Medical and Health Care"},
    {"nama": "Paracetamol", "harga": 30000, "kategori": "Medical and Health Care"},
    {"nama": "Sapu", "harga": 30000, "kategori": "Others"},
    {"nama": "Popok Bayi Sekali Pakai", "harga": 50000, "kategori": "Others"},
    {"nama": "Mayonnaise", "harga": 20000, "kategori": "Food"},
    {"nama": "Celana Jeans", "harga": 25000, "kategori": "Clothing"},
    {"nama": "Pensil", "harga": 3000, "kategori": "Stationery"},
    {"nama": "Spidol", "harga": 10000, "kategori": "Stationery"},
    {"nama": "Penghapus", "harga": 5000, "kategori": "Stationery"},
    {"nama": "Bulpen", "harga": 10000, "kategori": "Stationery"},
    {"nama": "Lifebuoy Body Wash", "harga": 30000, "kategori": "Toiletries"},
    {"nama": "Sikat Gigi", "harga": 20000, "kategori": "Toiletries"},
    {"nama": "Pasta Gigi", "harga": 15000, "kategori": "Toiletries"},
    {"nama": "Vitamin C", "harga": 50000, "kategori": "Medical and Health Care"},
    {"nama": "Head & Shoulders", "harga": 60000, "kategori": "Toiletries"},
    {"nama": "Sabun Cuci Muka", "harga": 25000, "kategori": "Toiletries"},
    {"nama": "Gunting", "harga": 30000, "kategori": "Stationery"},
    {"nama": "Kipas Angin", "harga": 100000, "kategori": "Others"},
    {"nama": "Gayung", "harga": 20000, "kategori": "Toiletries"},
    {"nama": "Seafood Beku", "harga": 75000, "kategori": "Food"},
    {"nama": "Ember", "harga": 30000, "kategori": "Toiletries"},
    {"nama": "Decolgen", "harga": 30000, "kategori": "Medical and Health Care"},
    {"nama": "Earphone", "harga": 50000, "kategori": "Others"},
    {"nama": "Penggaris", "harga": 15000, "kategori": "Stationery"},
    {"nama": "Teh", "harga": 10000, "kategori": "Food"},
    {"nama": "Voucher Goggle Play", "harga": 50000, "kategori": "Entertainment"},
    {"nama": "Voucher Garena", "harga": 100000, "kategori": "Entertainment"},
    {"nama": "Voucher Steam", "harga": 10000, "kategori": "Entertainment"},
    {"nama": "Promag", "harga": 10000, "kategori": "Medical and Health Care"},
    {"nama": "Panadol", "harga": 5000, "kategori": "Medical and Health Care"},
]

def generate_random_receipts(list_items, num_receipts):
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
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Receipt ID', 'Item', 'Quantity', 'Price', 'Item Total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for receipt in receipts:
            for item in receipt:
                writer.writerow(item)
            writer.writerow({})  # Add an empty row to separate receipts


def save_to_csv(data, filename):
    # Specify the field names
    fieldnames = ["nama", "harga", "kategori"]

    # Write the data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the data
        for item in data:
            writer.writerow(item)

    print(f"Data has been written to {filename}")

# # Parameters
# num_receipts = 10  # Number of receipts to generate
#
# # Generate random receipts
# random_receipts = generate_random_receipts(daftar_barang_dan_harga, num_receipts)
#
# # Save the receipts to a CSV file
# csv_filename = 'receipts10.csv'
# save_receipts_to_csv(random_receipts, csv_filename)
#
# print(f"Random receipts saved to {csv_filename}")

# Save teh data to CSV file
save_to_csv(daftar_barang_dan_harga, 'data/items_list.csv')