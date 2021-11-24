CREATE TABLE chatbot_question
(
    id serial primary key,
    topic varchar(50),
    sub_topic varchar(50),
    video_title varchar(50),
    question varchar(250),
    answer varchar(2000),
    sequence_tree varchar(1000),
    topic_terms varchar(250)
);

CREATE TABLE chatbot_video
(
    id serial primary key,
    title varchar(100),
    url varchar(300),
    added timestamp
);