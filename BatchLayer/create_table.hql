CREATE EXTERNAL TABLE tweets(
tweetID BIGINT,
public_date STRING,
text STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '/tweetsdata/tweets/';

SHOW TABLES;

SELECT * FROM tweets LIMIT 10;

CREATE EXTERNAL TABLE users(
tweetID BIGINT,
sentiment INT,
user_name STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '/tweetsdata/users/';

SHOW TABLES;

SELECT * FROM users LIMIT 10;
