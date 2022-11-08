import pickle 

with open('pickle3.pk', 'rb') as f:
    orders = pickle.load(f)

for group in orders:
    for item in group:
        print (item)


