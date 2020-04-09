from models.BooksData import BooksData
from surprise import KNNBasic
import numpy as np
import heapq
from collections import defaultdict
from operator import itemgetter

testSubject = '276680'
k = 10

# Load our data set and compute the user similarity matrix
bk = BooksData()
data = bk.loadBooksData()

trainSet = data.build_full_trainset()

sim_options = {'name': 'cosine',
               'user_based': True
               }

model = KNNBasic(sim_options=sim_options)
model.fit(trainSet)
simsMatrix = model.compute_similarities()
simsMatrix = np.nan_to_num(simsMatrix)

# print(simsMatrix)
# print(type(simsMatrix))

# Get top N similar users to our test subject
testUserInnerID = trainSet.to_inner_uid(testSubject)

if sim_options['user_based']:
    similarityRow = simsMatrix[testUserInnerID]

    similarUsers = []
    for innerID, score in enumerate(similarityRow):
        if innerID != testUserInnerID:
            similarUsers.append((innerID, score))

    kNeighbors = heapq.nlargest(k, similarUsers, key=lambda t: t[1])

    candidates = defaultdict(float)
    for similarUser in kNeighbors:
        innerID = similarUser[0]
        userSimilarityScore = similarUser[1]
        theirRatings = trainSet.ur[innerID]
        for rating in theirRatings:
            candidates[rating[0]] += (rating[1] / 10.0) * userSimilarityScore

else:
    testUserRatings = trainSet.ur[testUserInnerID]
    kNeighbors = heapq.nlargest(k, testUserRatings, key=lambda t: t[1])

    candidates = defaultdict(float)
    for itemID, rating in kNeighbors:
        similarityRow = simsMatrix[itemID]
        for innerID, score in enumerate(similarityRow):
            candidates[innerID] += score * (rating / 10.0)
# Get the stuff they rated, and add up ratings for each item, weighted by user similarity

# Build a dictionary of stuff the user has already read
read = {}
print('\n\nBooks user already read.')
print("============================")
for itemID, rating in trainSet.ur[testUserInnerID]:
    bookID = trainSet.to_raw_iid(itemID)
    print(bk.getBookName(bookID))
    read[itemID] = 1

# Get top-rated items from similar users:
print('\n\nBooks recommended.')
print("=======================")
pos = 0
for itemID, ratingSum in sorted(candidates.items(), key=itemgetter(1), reverse=True):
    if not itemID in read:
        bookID = trainSet.to_raw_iid(itemID)
        print(bk.getBookName(bookID))
        pos += 1
        if (pos > 10):
            break



