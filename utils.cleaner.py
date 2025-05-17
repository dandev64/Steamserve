# original columns:
# AppID,Name,Release date,Estimated owners,Peak CCU,Required age,Price,DLC count,About the game,Supported languages,Full audio languages,Reviews,Header image,Website,Support url,Support email,Windows,Mac,Linux,Metacritic score,Metacritic url,User score,Positive,Negative,Score rank,Achievements,Recommendations,Notes,Average playtime forever,Average playtime two weeks,Median playtime forever,Median playtime two weeks,Developers,Publishers,Categories,Genres,Tags,Screenshots,Movies

# retained columns:
# AppID,Name,Release date,Price,DLC count,Header image,Positive,Negative,Achievements,Developers,Publishers,Categories,Genres

# script to extract needed columns and create new csv file (for use in utils.import.py)
import pandas as pd
orig = pd.read_csv("games.csv", dtype=str)
keptCols = ["AppID","Name","Release date","Price","DLC count","Header image","Positive","Negative","Achievements","Developers","Publishers","Genres"]

new = orig[keptCols]
new.to_csv("steam.csv", index=False)