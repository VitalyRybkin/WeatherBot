PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS bot_user (
    user_id INTEGER,
    bot_user_id INTEGER NOT NULL,
    id INTEGER DEFAULT NULL,
    name VARCHAR(50) DEFAULT NULL,
    region VARCHAR(50) DEFAULT NULL,
    country VARCHAR(50) DEFAULT NULL,
    metric VARCHAR(8) CHECK (metric in ('metric', 'american')) DEFAULT 'metric',
    reply_menu INTEGER CHECK (reply_menu=0 OR reply_menu=1) DEFAULT 1,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS wishlist (
    wishlist_id INTEGER,
    wishlist_user_id INTEGER NOT NULL,
    id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    region VARCHAR(50) DEFAULT NULL,
    country VARCHAR(50) NOT NULL,
    PRIMARY KEY (wishlist_id )
    FOREIGN KEY (wishlist_user_id) REFERENCES bot_user(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS current_weather (
    current_weather_id INTEGER,
    current_weather_user_id INTEGER UNIQUE NOT NULL,
    wind_extended INTEGER CHECK (wind_extended=0 OR wind_extended=1) DEFAULT 0,
    pressure INTEGER CHECK (pressure=0 OR pressure=1) DEFAULT 0,
    visibility INTEGER CHECK (visibility=0 OR visibility=1) DEFAULT 0,
    humidity INTEGER CHECK (humidity=0 OR humidity=1) DEFAULT 0,
    PRIMARY KEY (current_weather_id)
    FOREIGN KEY (current_weather_user_id) REFERENCES bot_user(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS daily_weather (
    daily_weather_id INTEGER,
    daily_weather_user_id INTEGER UNIQUE NOT NULL,
    astro INTEGER CHECK (astro=0 OR astro=1) DEFAULT 0,
    visibility INTEGER CHECK (visibility=0 OR visibility=1) DEFAULT 0,
    humidity INTEGER CHECK (humidity=0 OR humidity=1) DEFAULT 0,
    PRIMARY KEY (daily_weather_id)
    FOREIGN KEY (daily_weather_user_id) REFERENCES bot_user(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS hourly_weather (
    hourly_weather_id INTEGER,
    hourly_weather_user_id INTEGER UNIQUE NOT NULL,
    wind_extended INTEGER CHECK (wind_extended=0 OR wind_extended=1) DEFAULT 0,
    pressure INTEGER CHECK (pressure=0 OR pressure=1) DEFAULT 0,
    visibility INTEGER CHECK (visibility=0 OR visibility=1) DEFAULT 0,
    humidity INTEGER CHECK (humidity=0 OR humidity=1) DEFAULT 0,
    PRIMARY KEY (hourly_weather_id)
    FOREIGN KEY (hourly_weather_user_id) REFERENCES bot_user(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS default_weather (
    default_weather_id INTEGER,
    default_user_id INTEGER NOT NULL UNIQUE,
    current_weather INTEGER CHECK (current_weather=0 OR current_weather=1) DEFAULT 1,
    daily_weather INTEGER CHECK (daily_weather IN (1, 2, 3) ) DEFAULT 3,
    hourly_weather INTEGER CHECK (hourly_weather BETWEEN 1 AND 12) DEFAULT 6,
    PRIMARY KEY (default_weather_id)
    FOREIGN KEY (default_user_id) REFERENCES bot_user(user_id)
);

CREATE INDEX IF NOT EXISTS wishlist_index ON wishlist(wishlist_id);
CREATE INDEX IF NOT EXISTS hourly_id_index ON hourly_weather(hourly_weather_id);
CREATE INDEX IF NOT EXISTS daily_id_index ON daily_weather(daily_weather_id);
CREATE INDEX IF NOT EXISTS current_id_index ON current_weather(current_weather_id);
CREATE INDEX IF NOT EXISTS bot_user_index ON bot_user(user_id);
CREATE INDEX IF NOT EXISTS default_user_id_index ON default_weather(default_weather_id);