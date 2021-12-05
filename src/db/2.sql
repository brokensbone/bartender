--User table
CREATE TABLE User (
	UserName TEXT,
	Token TEXT,
	Salt TEXT,
	Approved BIT
);

CREATE UNIQUE INDEX UserId ON User ( UserName ASC );