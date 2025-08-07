import csv
import random

def generate_csv(filename, num_items=10000):
    categories = ['Electronics', 'Books', 'Clothing', 'Home', 'Sports']
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Category', 'Price'])
        
        for i in range(1, num_items + 1):
            name = f"Item{i}"
            category = random.choice(categories)
            price = round(random.uniform(10.0, 500.0), 2)
            writer.writerow([i, name, category, price])

if __name__ == "__main__":
    generate_csv("generated_items_data.csv")
    print("CSV-файл згенеровано успішно.")
