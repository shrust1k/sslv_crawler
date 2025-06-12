import requests, os
UPLOAD_FOLDER = './tmp'

os.mkdir('./tmp')

categories= ['homes-summer-residences', 'flats', 'farms-estates']
places = ['riga/all', 'jurmala', 'riga-region', 'aizkraukle-and-reg',
         'aluksne-and-reg', 'balvi-and-reg', 'bauska-and-reg', 'cesis-and-reg', 'daugavpils-and-reg',
         'dobele-and-reg', 'gulbene-and-reg', 'jekabpils-and-reg', 'jelgava-and-reg', 'kraslava-and-reg',
         'kuldiga-and-reg', 'liepaja/all', 'limbadzi-and-reg', 'ludza-and-reg',
         'madona-and-reg', 'ogre-and-reg', 'preili-and-reg', 'rezekne-and-reg', 
         'saldus-and-reg', 'talsi-and-reg', 'tukums-and-reg', 'valka-and-reg',
         'valmiera-and-reg', 'ventspils-and-reg']


counter = 0
for c in categories:
    page_num = 10
    for p in places:
        try:
            if p == 'riga/all' or p == 'jurmala':
                page_num = 30
            for i in range(1, page_num):
                url = f"https://www.ss.lv/lv/real-estate/{c}/{p}/page{i}.html"
                # print(url)
                file = requests.get(url=url).text
                with open(f"{UPLOAD_FOLDER}/page{counter}.html", "w", encoding='utf-8') as f:
                    f.write(file)
                
                if counter % 5 == 0 and counter != 0:
                    print(f"{counter} pages loaded")
                counter += 1
        except:
            print(f"{p} failed.")

