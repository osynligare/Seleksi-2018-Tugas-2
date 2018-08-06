import json
import pandas as pd
import matplotlib.pyplot as plt


#---- Return list of actor with genres and amount of movies on each genre ----#
def actor_genre(data):
    # create list of actor with genres and amount of movies on each genre
    actor_genre = {}

    # iterate through the data
    for i in range(len(data)):
        actor = data[i]['actor']
        actor_genre[actor] = {}
        for movie in data[i]['movies']:
            for genre in movie['genre']:
                if genre in actor_genre[actor]:
                    actor_genre[actor][genre] += 1
                else:
                    actor_genre[actor][genre] = 1

    return actor_genre


#---- Return list of movies with year and average rating for each actor ----#
def actor_rating(data):    
    # create list of movies with year and average rating for every actor
    avg_rating_year = {}

    # iterate through the data to find average
    for i in range(len(data)):
        actor = data[i]['actor']
        avg_rating_year[actor] = {}
        for movie in data[i]['movies']:
            if movie['year'] in avg_rating_year[actor]:
                avg_rating_year[actor][movie['year']][0] += movie['rating']
                avg_rating_year[actor][movie['year']][1] += 1
            else:
                avg_rating_year[actor][movie['year']] = []
                avg_rating_year[actor][movie['year']].append(movie['rating'])
                avg_rating_year[actor][movie['year']].append(1) 
                
    # count the average
    for actor, years in avg_rating_year.items():
        for key, value in years.items():
            avg_rating_year[actor][key] = value[0]/value[1]

    return avg_rating_year


#---- Return list of actor with amount of movie each year ----#
def actor_amount(data):
    movie_yearly = {}

    # iterate through the data to find average
    for i in range(len(data)):
        actor = data[i]['actor']
        movie_yearly[actor] = {}
        for movie in data[i]['movies']:
            if movie['year'] in movie_yearly[actor]:
                movie_yearly[actor][movie['year']] += 1
            else:
                movie_yearly[actor][movie['year']] = 1

    return movie_yearly


#---- Return list of movies with year and average rating for every studio ----#
def studio_rating(data):    
    # create list of movies with year and average rating for every studio
    avg_rating_year = {}

    # iterate through the data to find average
    for i in range(len(data)):
        for movie in data[i]['movies']:
            studio = movie['studio']
            if studio not in avg_rating_year:
                avg_rating_year[studio] = {}
            if movie['year'] in avg_rating_year[studio]:
                avg_rating_year[studio][movie['year']][0] += movie['rating']
                avg_rating_year[studio][movie['year']][1] += 1
            else:
                avg_rating_year[studio][movie['year']] = []
                avg_rating_year[studio][movie['year']].append(movie['rating'])
                avg_rating_year[studio][movie['year']].append(1) 


    # count the average
    for movie, years in avg_rating_year.items():
        for key, value in years.items():
            avg_rating_year[movie][key] = value[0]/value[1]

    return avg_rating_year