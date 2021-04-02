import requests, bs4, openpyxl
from fake_useragent import UserAgent
  
ua = UserAgent()
header = {
    "User-Agent": ua.random
     }
# Replace "YEAR" by the year you
#  want to get data from. Eg. "2018"
url = 'https://summerofcode.withgoogle.com/archive/2020/organizations/'
  
# Creating a response object 
# from the given url
res = requests.get(url)
  
# We'll be using the Archive page
# of GSoC's website as our source.
# Checking the url's status
res.raise_for_status()
# Specify the language you
#  want to search for
language = 'python'
  
# BS4 object to store the 
# html text We use res.text 
# to get the html code in text format
soup = bs4.BeautifulSoup(res.text, 'html.parser')
  
# Selecting the specific tag 
# with class name
orgElem = soup.select('h4[class ="organization-card__name font-black-54"]')
  
  
# Similarly finding the links 
# for each org's gsoc page
orgLink = soup.find_all("a", class_="organization-card__link")
languageCheck = ['no'] * len(orgElem)
orgURL = ['none'] * len(orgElem)
item = 0
# Loop to go through each organisation
for link in orgLink:
  
    # Gets the anchor tag's hyperlink
    presentLink = link.get('href') 
  
    url2 = 'https://summerofcode.withgoogle.com' + presentLink 
    print(item)
    print(url2)
    orgURL[item] = url2
    res2 = requests.get(url2)
    res2.raise_for_status()
  
    soup2 = bs4.BeautifulSoup(res2.text, 'html.parser')
    tech = soup2.find_all("li",
                      class_="organization__tag organization__tag--technology")
  
    # Finding if the org uses 
    # the specified language
    for name in tech:
  
        if language in name.getText():
            languageCheck[item] = 'yes'
  
    item = item + 1
wb = openpyxl.Workbook()
sheet = wb['Sheet']
  
for i in range(0, len(orgElem)):
    sheet.cell(row = i + 1, column = 1).value = orgElem[i].getText()
    sheet.cell(row = i + 1, column = 2).value = languageCheck[i]
    sheet.cell(row = i + 1, column = 3).value = orgURL[i]
  
wb.save('gsocOrgsList.xlsx')