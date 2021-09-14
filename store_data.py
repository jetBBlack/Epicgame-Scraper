import psycopg2
from psycopg2.extras import execute_batch
from epicgame_scrape import main

insert_game_table_query = "INSERT INTO game(id, title, description, image, price, discount, developer, publisher, release_date, platform, about, rating, min_requirement, max_requirement) VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
insert_category_table_query = """INSERT INTO category (title) VALUES ('Action'), ('Adventure'), ('Indie'), ('RPG'), ('Strategy'), ('Open World'), ('Shooter'), ('Puzzle'), ('First Person'), ('Narration'), ('Simulation'), ('Casual'), ('Turn-Based'), ('Exploration'), ('Horror'), ('Platformer'), ('Party'), ('Survival'), 
    ('Trivia'), ('City Builder'), ('Stealth'), ('Fighting'), ('Comedy'), ('Action-Adventure'), ('Racing'), ('Rogue-Lite'), ('Card Game'), ('Sports'), ('Dungeon Crawler'), ('Single Player'), ('Controller Support'), ('Multiplayer'), ('Co-op'), ('Competitive'), ('VR');"""

def insert_game_table():
    print('Initialize connection...')
    conn = psycopg2.connect("host=localhost dbname=gamedb user=postgres password = bloodyangel23")
    cursor = conn.cursor()
    print('Connected. Start write data into database...')
    games = main()
    for game in games:
        cursor.execute(insert_game_table_query, game )
        conn.commit()
    
    conn.close()
    print("Write succesful!")


if __name__ == "__main__":
    insert_game_table()


