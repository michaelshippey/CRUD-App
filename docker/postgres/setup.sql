CREATE TABLE user_data(
   id SERIAL PRIMARY KEY      NOT NULL,
   first_name        TEXT NOT NULL,
   last_name         TEXT      NOT NULL,
   username TEXT NOT NULL UNIQUE,
   email TEXT NOT NULL UNIQUE ,
   password TEXT NOT NULL ,
   created_at TEXT NOT NULL
);

CREATE table reviews(
   review_id SERIAL NOT NULL,
   user_id integer not null,
   score integer not null,
   comment text not null,
   update_date text not null,
   movie text not null,
   PRIMARY Key(review_id),
   constraint fk_review FOREIGN key(user_id) REFERENCES user_data(id)
)
