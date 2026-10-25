PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Listings (
    id INTEGER PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES Users(id),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL CHECK (price >= 0),
    status TEXT NOT NULL DEFAULT 'available'
        CHECK (status IN ('available', 'reserved', 'sold')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Images (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER NOT NULL UNIQUE REFERENCES Listings(id)
        ON DELETE CASCADE,
    image BLOB NOT NULL
);

CREATE TABLE IF NOT EXISTS Categories (
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    value TEXT NOT NULL,
    UNIQUE (type, value)
);

CREATE TABLE IF NOT EXISTS ListingCategories (
    listing_id INTEGER NOT NULL REFERENCES Listings(id)
        ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES Categories(id),
    PRIMARY KEY (listing_id, category_id)
);

CREATE TABLE IF NOT EXISTS Favorites (
    user_id INTEGER NOT NULL REFERENCES Users(id)
        ON DELETE CASCADE,
    listing_id INTEGER NOT NULL REFERENCES Listings(id)
        ON DELETE CASCADE,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, listing_id)
    UNIQUE(user_id, listing_id)
);

CREATE TABLE IF NOT EXISTS Dialogues (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES Listings(id),
    buyer_id INTEGER NOT NULL REFERENCES Users(id),
    seller_id INTEGER NOT NULL REFERENCES Users(id),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (listing_id, buyer_id)
);

CREATE TABLE IF NOT EXISTS Messages (
    id INTEGER PRIMARY KEY,
    dialogue_id INTEGER NOT NULL REFERENCES Dialogues(id)
        ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES Users(id),
    message TEXT NOT NULL,
    sent_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER NOT NULL UNIQUE
        REFERENCES Listings(id),
    seller_id INTEGER NOT NULL REFERENCES Users(id),
    buyer_id INTEGER NOT NULL REFERENCES Users(id),
    final_price REAL NOT NULL CHECK (final_price >= 0),
    status TEXT NOT NULL DEFAULT 'reserved'
        CHECK (status IN ('reserved', 'completed', 'cancelled')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS Reviews (
    id INTEGER PRIMARY KEY,
    transaction_id INTEGER NOT NULL REFERENCES Transactions(id),
    from_user_id INTEGER NOT NULL REFERENCES Users(id),
    to_user_id INTEGER NOT NULL REFERENCES Users(id),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (transaction_id, from_user_id)
);
