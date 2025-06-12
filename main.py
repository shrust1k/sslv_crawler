from bs4 import BeautifulSoup
import re, os, traceback
import sqlalchemy 

conn = sqlalchemy.create_engine('sqlite:///db.db')
db = conn.connect()

db.execute(sqlalchemy.text('''
create table if not EXISTS  ads (
id integer primary key AUTOINCREMENT,
description text,
district text,
address text,
square_inside int,
floor int,
square_ter int,
price int,
period text,
everything text UNIQUE NOT NULL,
link text)'''))
db.commit()

class Ad:
    def __init__(self, description, row, link):
        try:
            try:
                self.description = description
            except:
                self.description = None
            try:
                self.district = row[0].contents[0].text
            except:
                self.district = None
            try:
                self.address = row[0].contents[2].text
            except:
                self.address = None
            try:
                self.square_inside = int(row[1].text)
            except:
                self.square_inside = None
            try:
                self.floor = int(row[2].text)
            except:
                self.floor = None
            try:
                self.square_ter = int(row[3].text.split(" ")[0])
            except:
                self.square_ter = None
            try:
                self.price = int(row[4].text.split(" ")[0].replace(",", ""))
            except:
                self.price = None
            try:
                if row[4].text.split(" ")[2] == "€":
                    self.period = 'one-timer'
                elif row[4].text.split(" ")[2] == "€/mēn.":
                    self.period = 'month'
                elif row[4].text.split(" ")[2] == "€/dienā":
                    self.period = 'day'
                else:
                    self.period = None   
            except:
                self.period = None
            row = [cell.text for cell in row]
            self.everything = str(row)
            try:
                self.link = link
            except:
                self.link = None
        except:
            pass
       
    def __str__(self):
        return (
            "-------------------------------\n"
            f"Description: {self.description}\n"
            f"District: {self.district}\n"
            f"Address: {self.address}\n"
            f"Inside Area: {self.square_inside}\n"
            f"Floors: {self.floor}\n"
            f"Land Area: {self.square_ter}\n"
            f"Price: {self.price}\n"
            f"Period: {self.period}"
        )
        
    def load_to_db(self, database):
        try:
            database.execute(sqlalchemy.text(f'''
            INSERT INTO ads 
            (description, district, address,  square_inside, floor, square_ter, price, period, everything, link) 
            VALUES (:description, :district, :address, :square_inside, :floor, :square_ter, :price, :period, :everything, :link)'''),
            {"description":self.description,
             "district": self.district,
            "address":self.address,
            "square_inside":self.square_inside,
            "floor": self.floor,
            "square_ter": self.square_ter,
            "price": self.price,
            "period": self.period,
            "everything": self.everything,
            "link": self.link
            })
            database.commit()
        except sqlalchemy.exc.IntegrityError: # "already in db"
            # print(traceback.format_exc())
            pass

for page in os.listdir("./tmp"):
    try:
        with open(f"./tmp/{page}", 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            pattern = r'^tr_.*$'
            for tr in soup.find_all('tr'):
                if tr.get('id') and re.search(pattern, tr.get('id')) and tr.get('id').find('bnr') == -1: # inside ad row
                    description = tr.find(class_='msg2').string
                    row = tr.find_all(class_="msga2-o pp6")
                    link = tr.find(class_='msg2').find('div').find('a').get('href')
                    
                    if row and row[4] and row[4].text.strip() != 'pērku':
                        ad = Ad(description, row, link)
                        # print(ad)
                        ad.load_to_db(database=db)
    except Exception as e:
        print(traceback.format_exc())
                    
    print(f"{page} loaded")

