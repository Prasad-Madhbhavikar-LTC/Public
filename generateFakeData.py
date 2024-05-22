import csv
import random
import string
import concurrent.futures

from faker import Faker

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def generate_customer_data(num_rows):
    fake = Faker()
    data = []
    for _ in range(num_rows):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        gender = fake.random_element(["Male", "Female"])
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%d-%m-%Y")
        phone = fake.phone_number()
        account_number = generate_random_string(8)
        balance = round(random.uniform(1000, 1000000), 2)
        data.append((first_name, last_name, email, gender, dob, phone, account_number, balance))
    return data

def write_csv(filename, data):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["first_name", "last_name", "email", "gender", "dob", "phone", "account_number", "balance"])
        writer.writerows(data)

def generate_and_write_data(num_rows, filename):
    customer_data = generate_customer_data(num_rows)
    write_csv(filename, customer_data)

def main():
    num_rows = int(input("Enter the number of rows: "))
    num_threads = 4  # You can adjust the number of threads as needed
    filenames = [f"customer_data_{i}.csv" for i in range(num_threads)]

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            executor.submit(generate_and_write_data, num_rows // num_threads, filenames[i])

    # Merge all files into a single CSV
    merged_data = []
    for filename in filenames:
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            merged_data.extend(list(reader))

    merged_filename = "merged_customer_data.csv"
    write_csv(merged_filename, merged_data)
    print(f"Generated {num_rows} rows of customer data in {num_threads} files. Merged into {merged_filename}.")

if __name__ == "__main__":
    main()