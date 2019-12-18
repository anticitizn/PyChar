import json

filename = input("File name: ")
with open (filename) as json_file:
    st = json.load(json_file)
    for data in st:
        print(data + " " + st.get(data))
    
input()
