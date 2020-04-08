import csv
with open('ratings.csv', newline='\n', encoding='utf-8') as csvfile, open('ratings2.csv','w',newline='\n') as userfile:
    rdr = csv.reader(csvfile, delimiter=',')
    wrt = csv.writer(userfile, delimiter=',')
    for row in rdr:
        try:
            x = float(row[2])
            wrt.writerow([row[x] for x in range(1,4)])
        except:
            pass