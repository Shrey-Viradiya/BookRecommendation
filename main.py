from models.BooksData import BooksData

Data = BooksData()

Data.loadBooksData()
# Data.getUserRatings(35433)
x = Data.getPopularityRanks()

for isbn in list(x.keys())[:15]:
    try:
        print(Data.ISBN_to_title[isbn])
    except KeyError:
        print(f"No Book data found for {isbn}")
