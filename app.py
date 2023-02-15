import sys, requests, json
from difflib import SequenceMatcher
from urllib.parse import urlsplit

s = SequenceMatcher()
url = sys.argv[1]
max_trust = 0.9422

# gets the full url in case of bit.ly
if url[:6] == 'bit.ly':
    url = requests.head("http://"+url).headers["location"]

# gets the black list from memory
black_list = []
with open('black list.txt', encoding='utf-8') as my_file:
    for line in my_file:
        black_list.append(line.strip())

# checks if the url is in the black list
if url in black_list:
    print(json.dumps([1])) # 1 = defenatly a phishing using the black list
    sys.exit()

# change url to root
url = "https://" + url.split("/")[2]

# if the url isn't in the black list its gonna be making a few security checks:

#checks for https
if url[4] != "s":
    print(json.dumps([2, "this website does not use https!"])) # 2 = url doesn't use https
    sys.exit()

# loads white list of trusted websites from memory
white_list = []
with open('white list.txt', encoding='utf-8') as my_file:
    for line in my_file:
        white_list.append(line.strip())

# checks if url is in the white list
if url in white_list:
    print(json.dumps([0])) # 1 = defenatly a phishing using the black list
    sys.exit()

# checks for similar urls in the white list
for i in range(len(white_list)):
    to_compare = [url, white_list[i]]
    for j in range(len(to_compare)):
        x = to_compare[j]
        s.set_seq1(x)
        for k in range(j+1, len(to_compare)):
            y = to_compare[k]
            s.set_seq2(y)
            end_val = s.ratio()
            if end_val > max_trust:
                real_website = urlsplit(white_list[i]).netloc
                print(json.dumps([2, f"this website might be trying to look like: {real_website}!"]))
                sys.exit()
    
    # checks for home and about page
    try:
        response = requests.get(url + "about")
        response = requests.get(url)
    except:
        print(json.dumps([2, f"this website does not have home/about page like most of the websits!"]))
        sys.exit()

print(json.dumps("0")) # 0 = probably a safe site