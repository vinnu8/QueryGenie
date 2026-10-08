import kagglehub

# Download latest version
path = kagglehub.dataset_download("muhammadaammartufail/global-e-commerce-sales-and-customer-data")

print("Path to dataset files:", path)