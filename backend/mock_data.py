"""Fallback movie catalog used when TMDB_API_KEY is missing.
Curated across moods with a bias toward hidden gems / cult classics.
Poster URLs use TMDB CDN paths directly (no auth needed for images)."""

MOCK_MOVIES = [
    # NOSTALGIC / COMING-OF-AGE
    {"id": 508, "title": "Stand by Me", "year": 1986, "runtime": 89, "rating": 8.1, "vote_count": 8400,
     "genres": ["Drama", "Adventure"], "moods": ["nostalgic", "melancholy"], "poster": "/kAdNK7QSMLmuU2GbwtccbK4jj9m.jpg",
     "backdrop": "/dLKzS4t3F9c1TgQ2VYU2Rj27nDe.jpg", "overview": "Four boys walk the tracks to find a body and a summer they will never forget.",
     "gem": False, "popularity": 42},
    {"id": 105, "title": "Back to the Future", "year": 1985, "runtime": 116, "rating": 8.5, "vote_count": 19500,
     "genres": ["Adventure", "Comedy", "Sci-Fi"], "moods": ["nostalgic", "euphoric"], "poster": "/fNOH9f1aA7XRTzl1sAOx9iF553Q.jpg",
     "backdrop": "/fq3wyOs1RHyz2yfzsb4sck7aWRG.jpg", "overview": "A teen is hurled into 1955 by his mad-scientist friend's DeLorean.",
     "gem": False, "popularity": 88},
    {"id": 12405, "title": "Slumdog Millionaire", "year": 2008, "runtime": 120, "rating": 7.9, "vote_count": 10200,
     "genres": ["Drama", "Romance"], "moods": ["euphoric", "romantic"], "poster": "/9tG5MRDf7ykuxWjMOhpNPBUw5jc.jpg",
     "backdrop": "/6yV1nDBGwUUZlBhCM0FiXvvZI1r.jpg", "overview": "A Mumbai teen from the slums competes on Who Wants to Be a Millionaire.",
     "gem": False, "popularity": 40},

    # COZY / RAINY DAY
    {"id": 12762, "title": "Whisper of the Heart", "year": 1995, "runtime": 111, "rating": 7.9, "vote_count": 1650,
     "genres": ["Animation", "Romance", "Drama"], "moods": ["cozy", "nostalgic", "romantic"], "poster": "/2vLGJGyBGltvbY0DzXqrxCUgm8m.jpg",
     "backdrop": "/whFEyAll3EWZKgYlGxi9DZKELtM.jpg", "overview": "A Tokyo teen discovers a mysterious cat, an antique shop, and her own voice as a writer.",
     "gem": True, "popularity": 22},
    {"id": 449, "title": "Kiki's Delivery Service", "year": 1989, "runtime": 103, "rating": 7.8, "vote_count": 3400,
     "genres": ["Animation", "Fantasy"], "moods": ["cozy", "euphoric"], "poster": "/7nO5DUMnGUuXrA4r2h5v0huTGwT.jpg",
     "backdrop": "/htLPZphxx3fUEinRHKB1EHdCJVh.jpg", "overview": "A young witch starts a broomstick delivery service in a seaside town.",
     "gem": False, "popularity": 34},
    {"id": 490132, "title": "Paterson", "year": 2016, "runtime": 118, "rating": 7.3, "vote_count": 1900,
     "genres": ["Drama", "Comedy"], "moods": ["cozy", "melancholy"], "poster": "/nJQTL5wKtVJx8VfCyGpxvNpCTUW.jpg",
     "backdrop": "/mHzoP2fBBjWfKgQ7hR8CxLR6b8j.jpg", "overview": "A bus driver in New Jersey writes poems in the margins of his quiet life.",
     "gem": True, "popularity": 15},

    # CHAOTIC / ANGRY
    {"id": 680, "title": "Pulp Fiction", "year": 1994, "runtime": 154, "rating": 8.5, "vote_count": 27500,
     "genres": ["Thriller", "Crime"], "moods": ["chaotic", "weird", "angry"], "poster": "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
     "backdrop": "/suaEOtk1N1sgg2MTM7oZd2cfVp3.jpg", "overview": "The lives of two mob hitmen, a boxer, and a diner couple intertwine.",
     "gem": False, "popularity": 92},
    {"id": 550, "title": "Fight Club", "year": 1999, "runtime": 139, "rating": 8.4, "vote_count": 28000,
     "genres": ["Drama", "Thriller"], "moods": ["angry", "chaotic", "weird"], "poster": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
     "backdrop": "/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg", "overview": "An insomniac and a soap salesman start an underground club that spirals out of control.",
     "gem": False, "popularity": 85},
    {"id": 66021, "title": "Good Time", "year": 2017, "runtime": 101, "rating": 7.2, "vote_count": 2600,
     "genres": ["Crime", "Thriller"], "moods": ["chaotic", "angry"], "poster": "/tQMYzTqXlpZzRxWfnP7RysBWg.jpg",
     "backdrop": "/g0Rk4dTTCF6HTsRfBK5S3tR3fCJ.jpg", "overview": "A bank robber sprints through neon New York to save his brother.",
     "gem": True, "popularity": 18},

    # MELANCHOLY
    {"id": 843, "title": "Lost in Translation", "year": 2003, "runtime": 102, "rating": 7.7, "vote_count": 7800,
     "genres": ["Drama", "Romance"], "moods": ["melancholy", "romantic"], "poster": "/kOJDs6EqiWzMWSXCU2skqQCtL7z.jpg",
     "backdrop": "/hzGKtYbaYsIkbG8LGjOtSjMYo0S.jpg", "overview": "Two lonely Americans drift through Tokyo nights together.",
     "gem": False, "popularity": 30},
    {"id": 76341, "title": "In the Mood for Love", "year": 2000, "runtime": 98, "rating": 8.1, "vote_count": 3200,
     "genres": ["Drama", "Romance"], "moods": ["melancholy", "romantic"], "poster": "/iYypPT4bhqXfq1b6EnmxvRt6b2Y.jpg",
     "backdrop": "/2r4uEjRV2nMg6d40nhKG4gU29Ah.jpg", "overview": "Two Hong Kong neighbors discover their spouses are having an affair — and slowly become entangled themselves.",
     "gem": True, "popularity": 20},
    {"id": 490, "title": "Perfect Blue", "year": 1997, "runtime": 81, "rating": 8.0, "vote_count": 2500,
     "genres": ["Animation", "Thriller"], "moods": ["melancholy", "weird"], "poster": "/79ldj39xNbYy4CVFyM2Q7ie3PYY.jpg",
     "backdrop": "/9Y7pDf1P36GA6NqjBQd5j5uJc0v.jpg", "overview": "A pop idol quits music for acting and reality begins to unravel.",
     "gem": True, "popularity": 24},

    # EUPHORIC
    {"id": 194, "title": "Amélie", "year": 2001, "runtime": 122, "rating": 7.9, "vote_count": 9500,
     "genres": ["Comedy", "Romance"], "moods": ["euphoric", "cozy", "romantic"], "poster": "/f0uorE7K6a8SPFji8W6vY2ryV3S.jpg",
     "backdrop": "/j2Zc0Pf76mZk3jjXwFEahAkfPPi.jpg", "overview": "A shy Paris waitress secretly transforms strangers' lives.",
     "gem": False, "popularity": 55},
    {"id": 4348, "title": "Sing Street", "year": 2016, "runtime": 106, "rating": 7.9, "vote_count": 2100,
     "genres": ["Comedy", "Drama", "Music"], "moods": ["euphoric", "nostalgic"], "poster": "/dJcRxG7z5oKgLxWmyaEOJc3JgcW.jpg",
     "backdrop": "/aH6dP8fJp0hJ1M2gCkCqR8fH2X8.jpg", "overview": "A Dublin teen starts a band in the 80s to impress a girl.",
     "gem": True, "popularity": 26},

    # WEIRD / CULT
    {"id": 62, "title": "2001: A Space Odyssey", "year": 1968, "runtime": 149, "rating": 8.1, "vote_count": 10800,
     "genres": ["Sci-Fi", "Adventure"], "moods": ["weird", "melancholy"], "poster": "/ve72VxNqjGM69Uky4WTo2bK6rfq.jpg",
     "backdrop": "/pOO7QeuLbLvSc1uQ4hZfCiXbmY.jpg", "overview": "A mysterious monolith propels humanity from apes to the stars.",
     "gem": False, "popularity": 45},
    {"id": 1417, "title": "Eraserhead", "year": 1977, "runtime": 89, "rating": 7.4, "vote_count": 1500,
     "genres": ["Horror", "Drama"], "moods": ["weird", "chaotic"], "poster": "/8oT3RCEuQ8h6Tgs7X0hCgZmqSXn.jpg",
     "backdrop": "/2K8B4Ll1u7QGqDcqYgS4nHqYd8x.jpg", "overview": "David Lynch's black-and-white industrial nightmare.",
     "gem": True, "popularity": 10},
    {"id": 315837, "title": "The Lighthouse", "year": 2019, "runtime": 109, "rating": 7.5, "vote_count": 4700,
     "genres": ["Horror", "Drama"], "moods": ["weird", "melancholy", "angry"], "poster": "/3nk9UoepYmv1G9oP18q6JJnpZQ.jpg",
     "backdrop": "/wvzHu2ZFhTB2ZFp88M1PLPFe3Wn.jpg", "overview": "Two lighthouse keepers lose their minds on a remote New England island.",
     "gem": True, "popularity": 28},

    # ROMANTIC
    {"id": 38, "title": "Eternal Sunshine of the Spotless Mind", "year": 2004, "runtime": 108, "rating": 8.1, "vote_count": 13100,
     "genres": ["Sci-Fi", "Romance", "Drama"], "moods": ["romantic", "melancholy"], "poster": "/5MwkWH9tYHv3mV9OdYTMR5qreIz.jpg",
     "backdrop": "/9wDEZgKUYX3z3Ny53whWtb6XkVW.jpg", "overview": "A couple erases each other from their memories, then finds each other again.",
     "gem": False, "popularity": 60},
    {"id": 24238, "title": "Before Sunrise", "year": 1995, "runtime": 101, "rating": 8.0, "vote_count": 3800,
     "genres": ["Drama", "Romance"], "moods": ["romantic", "nostalgic"], "poster": "/qYQqfvKp8h4dbLmvEQZ2QpTQ2rY.jpg",
     "backdrop": "/6MKr3KgOL0eYU7zw90R5vP1a7YU.jpg", "overview": "An American and a Frenchwoman spend one Vienna night together.",
     "gem": True, "popularity": 32},
    {"id": 27205, "title": "Portrait of a Lady on Fire", "year": 2019, "runtime": 122, "rating": 8.1, "vote_count": 3600,
     "genres": ["Drama", "Romance"], "moods": ["romantic", "melancholy"], "poster": "/2Mdw5nUC0fmw3TxIw5oNRSK1Njm.jpg",
     "backdrop": "/aRQ9E2X5jgnPUq2vY2KUdA0Ecvk.jpg", "overview": "A painter falls for the reluctant bride she was hired to secretly portray.",
     "gem": True, "popularity": 25},

    # ANGRY / VISCERAL
    {"id": 807, "title": "Se7en", "year": 1995, "runtime": 127, "rating": 8.3, "vote_count": 20500,
     "genres": ["Crime", "Thriller"], "moods": ["angry", "melancholy"], "poster": "/6yoghtyTpznpBik8EngEmJskVUO.jpg",
     "backdrop": "/ba4CpvnaxvAgff2jHiaqJrVpZJ5.jpg", "overview": "Two detectives hunt a killer using the seven deadly sins.",
     "gem": False, "popularity": 65},
    {"id": 27578, "title": "Enemy", "year": 2013, "runtime": 91, "rating": 6.9, "vote_count": 3400,
     "genres": ["Thriller", "Mystery"], "moods": ["weird", "angry"], "poster": "/gzZbBQeXWfEyBXSbYbi9d5B1lZE.jpg",
     "backdrop": "/2M0lZ2u7VP1YY0hVQOAqoTQGmc.jpg", "overview": "A history professor sees his double in a movie and everything unravels.",
     "gem": True, "popularity": 14},
]


def all_moods():
    return ["nostalgic", "cozy", "chaotic", "melancholy", "euphoric", "weird", "romantic", "angry"]
