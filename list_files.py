import os

dataset_directory = r"C:\Users\user\.cache\kagglehub\datasets\patrickfleith\nasa-battery-dataset\versions\2\cleaned_dataset\data"

def list_files():
    print("Available files in the dataset folder:")
    for root, dirs, files in os.walk(dataset_directory):
        print(f"Folder: {root}")
        for file in files:
            print(f"  - {file}")

if __name__ == "__main__":
    list_files()




