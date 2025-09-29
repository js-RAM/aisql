create table person (
    person_id integer primary key,
    name varchar(20) not null,
    email varchar(20) not null,
    join_date date not null
);

create table game (
    game_id integer primary key,
    title varchar,
    price decimal(5,2)
);

create table purchase (
    purchase_id integer primary key,
    game_id integer not null,
    person_id not null,
    purchase_date date,
    foreign key (person_id) references person (person_id),
    foreign key (game_id) references game (game_id)
);

create table review (
    review_id integer primary key,
    person_id integer not null,
    game_id integer not null,
    comment text,
    rating smallint not null,
    timestamp datetime,
    foreign key (person_id) references person (person_id),
    foreign key (game_id) references game (game_id)
);

create table tag (
    tag_id integer primary key,
    name varchar
);

create table game_tag (
    game_id integer not null,
    tag_id integer not null,
    primary key (game_id, tag_id)
);