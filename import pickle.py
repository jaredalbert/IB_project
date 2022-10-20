import pickle 
count = 1000
with open('pickle.pk', 'wb') as file:
    pickle.dump(count, file)

with open('pickle.pk', 'rb') as file:
    count = pickle.load(file)

with open('pickle2.pk', 'rb') as file:
    count = pickle.load(file)
print (count)

#count +=1

with open('pickle.pk', 'wb') as file:
    pickle.dump(count, file)

with open('pickle.pk', 'rb') as file:
    count = pickle.load(file)
print (count)