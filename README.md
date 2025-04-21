# Movie Tracker

This is a simple app that connects to the MovieDatabase online at: https://developer.themoviedb.org/reference/ and exposes it in a friendlier way so that consumers of this app can interact and have fun with it!!


## Usage

The app is split into two sections: CLI, API.

### CLI

The cli will allow you to programatically access the MovieDB API once you set your API KEY following the practices from the `example.env` file. This will allow you to be able to search for your tv shows and or see the trending shows for either the week or the day so that you can hopefully find something you would like to watch.

```bash
> tracker tv trending daily # or weekly
# View the daily trending shows from MovieDB
Invincible (10/22/2025)
A show about a man who is invincible
Genres: Action, Adventure, Sci-fi
Networks: Prime Video
---
> tracker tv search invincible
# Search for specific shows
Invincible (10/22/2025)
A show about a man who is invincible
Genres: Action, Adventure, Sci-fi
Networks: Prime Video
---
> tracker movie trending daily # or weekly
# get list of daily trending movies
Mortal Kombat (10/22/2025)
A show about a man who is invincible
Genres: Action, Adventure, Sci-fi
Networks: Prime Video
---
> tracker movie search Up
# Search for specific movies
UP (10/22/2025)
A show about a man who is invincible
Genres: Action, Adventure, Sci-fi
Networks: Prime Video
```

### API 

This will be for our Movie Tracking System such that we will be able to track shows you would like to watch after connecting it to a spreadsheet of which you have delegated the app to have access to. We will support OAuth End to End authentication and also allow you to be able to connect to your own spreadsheets to save this data so that we don't need to manage an external DB. We will also have an In-Memory Mode to allow you to run locally for testing as well as a FileSystem Mode to allow you to run this locally with limited persistence.

### Metadata Endpoints

__Version Endpoint__

```http
GET /api/version HTTP 1.1

v1.10.0
```

__HealthZ Endpoint__

```http
GET /api/healthz HTTP 1.1

{"o": "k"}
```

### Query Endpoints

#### TV Shows

__Search__

```http
GET /api/tv/search/?query="some show" HTTP 1.1

{
    "results": [{
        "name": "Invincible",
        "airdate": "2025-01-22",
        "description": "A show about a man and his dog :3",
        "length": {
            "seasons": 3,
            "episodes": 8,
            "episodes_per_season": {
                "1": 8,
                "2": 8,
                "3": 8,
            }
        },
        "networks": ["HBO"]
    }],
    "meta": {
        "page": 1,
        "pages": 1,
        "size": 20,
        "next": null # or "https://api-host/api/tv/search?query=\"some show\"&page=2&size=20"
    }
}
```

__Trending__

Supports the timeframe for: "daily", "weekly"

```http
GET /api/tv/trending/?timeframe="daily" HTTP 1.1

{
    "results": [{
        "name": "Invincible",
        "airdate": "2025-01-22",
        "description": "A show about a man and his dog :3",
        "length": {
            "seasons": 3,
            "episodes": 8,
            "episodes_per_season": {
                "1": 8,
                "2": 8,
                "3": 8,
            }
        },
        "networks": ["HBO"]
    }],
    "meta": {}
}
```

#### Movies

__Search__

```http
GET /api/movies/search/?query="some show" HTTP 1.1

{
    "results": [{
        "name": "Invincible",
        "airdate": "2025-01-22",
        "description": "A show about a man and his dog :3",
        "length": {
            "seasons": 3,
            "episodes": 8,
            "episodes_per_season": {
                "1": 8,
                "2": 8,
                "3": 8,
            }
        },
        "networks": ["HBO"]
    }],
    "meta": {
        "page": 1,
        "pages": 1,
        "size": 20,
        "next": null # or "https://api-host/api/movies/search?query=\"some show\"&page=2&size=20"
    }
}
```

__Trending__

Supports the timeframe for: "daily", "weekly"

```http
GET /api/movies/trending/?timeframe="daily" HTTP 1.1

{
    "results": [{
        "name": "Invincible",
        "airdate": "2025-01-22",
        "description": "A show about a man and his dog :3",
        "length": {
            "seasons": 3,
            "episodes": 8,
            "episodes_per_season": {
                "1": 8,
                "2": 8,
                "3": 8,
            }
        },
        "networks": ["HBO"]
    }],
    "meta": {}
}
```


### Tracking Endpoints

TBD: Will work on these after we fully expose the query data for what we want to do. This will be the coolest part of the work that needs to be done and this will change the way we request the things we care about.