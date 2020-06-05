# this project is for movie recommendation. input user ratings and find 3 most similar critics in 100 critics.
# recommend top average rated movies in each genre.
# Please put 'data' and 'data-tiny' files under cwd.
# sample interaction should be 'data IMDB.csv ratings.csv p8.csv'.
# p2 - p10 stands for each different user rating data.
import os,os.path
import pandas as pd


def secondElm(tuple):
    return tuple[1]

# using euclidean distance between user rating and critics ratings to find three critics similar with user's taste
def findCloseCritics(personal,critic):
    # make index columns 'Title'
    personal.index = personal['Title']
    critic.index = critic['Title']
    # find same movie,inner join
    join = pd.merge(personal, critic)
    dicOfScore = {}
    # find movie names in the join dataframe
    a=join['Title'].values
    # make column name a list
    b = list(join.columns)
    # find personal name
    name = b[2:]
    # find how many rows in the dataframe
    length = len(a)
    # make a dictionary that can associate name with euclidean distance
    for name in name:
        score = 0
        for i in range(1, length+1):
            score = score + (join[join.columns[1]].loc[i-1]-join[name].loc[i-1])**2
        dicOfScore[name] = score**0.5
    # sort by score and select first 3 of them
    lstOfScore = sorted(dicOfScore.items(), key=secondElm)
    lstOfCritics = lstOfScore[:3]
    lst1 = []
    # put them in a list
    for i in lstOfCritics:
        lst1.append(list(i)[0])
    return lst1

#  using the list of three similar critics to find the unwatched movies in each genre by descending order
def recommandMovie(critic, personal, threeCritic, movie):
    # find same movies
    other = pd.merge(critic, personal, how='inner')
    titleRatedMovie = list(other['Title'].values)
    # drop same movie data
    for movieName in titleRatedMovie:
        critic.drop(index=movieName, inplace=True)
    # select 3 critics' names
    a = list(critic.columns)
    if len(a)>4:
        for name in a:
            if name in threeCritic:
                a.remove(name)
        for name in a:
            critic.drop(columns=name, inplace=True)
    else:
        critic.drop(columns='Title', inplace=True)
    # average score
    critic['average'] = (critic[threeCritic[0]]+critic[threeCritic[1]]+critic[threeCritic[2]])/3
    # sort movie dataframe by column and then join
    totalList = pd.merge(critic, movie.reindex_axis(sorted(movie.columns), axis=1), how='left', left_index=True, right_index=True)
    b = []
    # group by Genre
    for g in totalList.groupby(by='Genre1'):
        a = []
        a = [g[0], g[1].sort_values('average')['average']]
        max = a[1][-1]
        cate = a[0]
        # find movie name equal to max rating
        recomandName = g[1][g[1]['average'] == max]
        b.append([cate, recomandName])
    return b


#  print out recommended movies and names of three critics
def printRecommendations(b,personName):
    # sorted by category name
    b = sorted(b)
    print('Recommendations for ', personName, ':')
    for i in b:
        for n in i[1].values:
            if pd.isnull(n[-3]):
                print('"', n[-2], '"', '('.rjust(40-len(n[-2])), i[0], ')', ', ', 'rating: ', round(n[3],2), ', ', n[-1])
            else:
                print('"', n[-2],'"', '('.rjust(40-len(n[-2])), i[0], ')', ', ', 'rating: ', round(n[3],2), ', ', n[-1], ', runs ', n[-3])

def main():
    folder, nameOfMovieFile, nameOfCriticsFiles, nameOfPersonalRatingFiles = input(
        'Please enter the name of folder with files, the name of movies files, the name of critics files, the name of personal ratings files, separated by spaces:').split()
    direc = os.path.join(os.getcwd(), folder)
    personalPath = os.path.join(direc, nameOfPersonalRatingFiles)
    personal = pd.read_csv(personalPath)
    personName = list(personal.columns)[1]
    criticsPath = os.path.join(direc, nameOfCriticsFiles)
    critic = pd.read_csv(criticsPath)
    threeCritic = findCloseCritics(personal,critic)
    print(threeCritic)
    moviePath = os.path.join(direc, nameOfMovieFile)
    # choose only columns we need
    movie = pd.read_csv(moviePath , usecols= ['Title','Year', 'Rating','Genre1','Runtime'])
    movie.index = movie['Title']
    b = recommandMovie(critic,personal,threeCritic,movie)
    printRecommendations(b,personName)

main()
