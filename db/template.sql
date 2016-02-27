CREATE TABLE feature_requests (
title TEXT,
description TEXT,
client TEXT,
priority INTEGER NOT NULL,
target_date DATE,
ticket_url TEXT,
product_area TEXT);

GRANT ALL ON feature_requests TO iws_user;

