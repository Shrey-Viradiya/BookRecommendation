import os
import csv
import sys
import re

from surprise import Dataset
from surprise import Reader

from collections import defaultdict
import pandas as pd
# import numpy as np

class BooksData:

    bookID_to_name = {}
    name_to_bookID = {}
    ratingsPath = 'data/ratings.csv'
    Books = 'data/books.csv'
    
    def loadBooksData(self):

        # Look for files relative to the directory we are running from
        os.chdir(os.path.dirname(sys.argv[0]))

        ratingsDataset = 0
        self.ISBN_to_title = {}
        self.title_to_ISBN = {}

        reader = Reader(line_format='user item rating', sep=',', skip_lines=1)

        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)

        with open(self.Books, newline='\n') as csvfile:
                bookReader = csv.reader(csvfile)
                next(bookReader)  #Skip header line
                for row in bookReader:
                    ISBN = row[0]
                    bookTitle = row[1]
                    self.ISBN_to_title[ISBN] = bookTitle
                    self.title_to_ISBN[bookTitle] = ISBN

        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        df = pd.read_csv(self.ratingsPath, delimiter=',')
        df = df[df['userID'] == user]
        for index, row in df.iterrows():
            userRatings.append((row['ISBN'], row['rating']))
        return userRatings

    def getPopularityRanks(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)
        with open(self.ratingsPath, newline='') as csvfile:
            ratingReader = csv.reader(csvfile)
            next(ratingReader)
            for row in ratingReader:
                ISBN = row[0]
                ratings[ISBN] += 1
        rank = 1
        for movieID, ratingCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[movieID] = rank
            rank += 1
        return rankings
    
    def getGenres(self):
        genres = defaultdict(list)
        genreIDs = {}
        maxGenreID = 0
        with open(self.Books, newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)  #Skip header line
            for row in movieReader:
                movieID = int(row[0])
                genreList = row[2].split('|')
                genreIDList = []
                for genre in genreList:
                    if genre in genreIDs:
                        genreID = genreIDs[genre]
                    else:
                        genreID = maxGenreID
                        genreIDs[genre] = genreID
                        maxGenreID += 1
                    genreIDList.append(genreID)
                genres[movieID] = genreIDList
        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for (movieID, genreIDList) in genres.items():
            bitfield = [0] * maxGenreID
            for genreID in genreIDList:
                bitfield[genreID] = 1
            genres[movieID] = bitfield            
        
        return genres
    
    def getYears(self):
        p = re.compile(r"(?:\((\d{4})\))?\s*$")
        years = defaultdict(int)
        with open(self.Books, newline='', encoding='ISO-8859-1') as csvfile:
            movieReader = csv.reader(csvfile)
            next(movieReader)
            for row in movieReader:
                movieID = int(row[0])
                title = row[1]
                m = p.search(title)
                year = m.group(1)
                if year:
                    years[movieID] = int(year)
        return years

    
    def getMovieName(self, movieID):
        if movieID in self.bookID_to_name:
            return self.bookID_to_name[movieID]
        else:
            return ""
        
    def getMovieID(self, movieName):
        if movieName in self.name_to_bookID:
            return self.name_to_bookID[movieName]
        else:
            return 0