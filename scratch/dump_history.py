import database
hist = database.get_historial('MarcosDB12', 1000)
with open('scratch/history_dump.txt', 'w') as f:
    for h in hist:
        f.write(f"{h}\n")
print(f"Dumped {len(hist)} records")
