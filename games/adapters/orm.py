from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Text, Float, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Publisher, Genre, User, Review, Wishlist

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

publishers_table = Table(
    'publishers', metadata,
    # We only want to maintain those attributes that are in our domain model
    # For publisher, we only have name.
    Column('name', String(255), primary_key=True)  # nullable=False, unique=True)
)

games_table = Table(
    'games', metadata,
    Column('game_id', Integer, primary_key=True),
    Column('game_title', Text, nullable=False),
    Column('game_price', Float, nullable=False),
    Column('release_date', String(50), nullable=False),
    Column('game_description', String(255), nullable=True),
    Column('game_image_url', String(255), nullable=True),
    Column('game_website_url', String(255), nullable=True),
    Column('publisher_name', ForeignKey('publishers.name'))
)

genres_table = Table(
    'genres', metadata,
    Column('genre_name',String(64),  primary_key=True, nullable=False)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_id', ForeignKey('genres.genre_name'))
)

reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),  # do i need this review_ID?
    Column('review_comment', String(255), nullable=False),
    Column('review_rating', Integer, nullable=False),
    Column('review_by_user', ForeignKey('users.username')),
    Column('game_reviewed', ForeignKey('games.game_id'))
)

users_table = Table(
    'users', metadata,
    Column('username', String(64), primary_key=True),
    Column('password', String(255), nullable=False),
)

favourites_table = Table(
    'favourites', metadata,
    Column('username', ForeignKey('users.username'), primary_key=True),
    Column('game_id', ForeignKey('games.game_id'), primary_key=True)
)

def map_model_to_tables():
    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.name,
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.game_price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.game_description,
        '_Game__image_url': games_table.c.game_image_url,
        '_Game__website_url': games_table.c.game_website_url,
        '_Game__publisher': relationship(Publisher),
        '_Game__genres': relationship(Genre, secondary=game_genres_table,
                                      back_populates='_Genre__genre_to_game'),
    })

    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,
        '_Genre__genre_to_game': relationship(Game, secondary=game_genres_table,
                                              back_populates='_Game__genres')
    })

    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
        '_User__favourite_games': relationship(Game, secondary=favourites_table)
    })

    mapper(Review, reviews_table, properties={
        '_Review__comment': reviews_table.c.review_comment,
        '_Review__rating': reviews_table.c.review_rating,
        #'_Review__user': relationship(User, back_populates='_User__reviews'),
        #'_Review__game': relationship(Game, back_populates='_Game__reviews'),
    })


