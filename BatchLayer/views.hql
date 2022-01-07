##########################################################################################################################

CREATE MATERIALIZED VIEW IF NOT EXISTS pos_neg_view
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '/tweetsdata/pos_neg_view/' AS
SELECT users.sentiment, COUNT(*) sent_count FROM tweets JOIN users ON (tweets.tweetID = users.tweetID)
GROUP BY users.sentiment;

##########################################################################################################################

CREATE VIEW month_view AS
SELECT MONTH(FROM_UNIXTIME(UNIX_TIMESTAMP(tweets.public_date, 'EEE MMM dd HH:mm:ss z yyyy'))) month_pub, users.sentiment
FROM tweets JOIN users ON (tweets.tweetID = users.tweetID);

CREATE MATERIALIZED VIEW IF NOT EXISTS time_view
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '/tweetsdata/time_view/' AS
select *, COUNT(1) from month_view GROUP BY month_pub, sentiment;

##########################################################################################################################

CREATE VIEW day_view AS
SELECT MONTH(FROM_UNIXTIME(UNIX_TIMESTAMP(tweets.public_date, 'EEE MMM dd HH:mm:ss z yyyy'))) month_pub, 
DAY(FROM_UNIXTIME(UNIX_TIMESTAMP(tweets.public_date, 'EEE MMM dd HH:mm:ss z yyyy'))) day_pub
FROM tweets JOIN users ON (tweets.tweetID = users.tweetID);

CREATE MATERIALIZED VIEW IF NOT EXISTS concurrency_view
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE LOCATION '/tweetsdata/concurrency_view/' AS
select *, COUNT(1) from day_view GROUP BY month_pub, day_pub;

##########################################################################################################################
