INSERT INTO person (person_id, name, email, join_date) VALUES
(1, 'Alice', 'alice@email.com', '2023-01-15'),
(2, 'Bob', 'bob@email.com', '2023-02-10'),
(3, 'Charlie', 'charlie@email.com', '2023-03-05');

INSERT INTO game (game_id, title, price) VALUES
(1, 'Space Invaders', 19.99),
(2, 'Mystic Quest', 29.99),
(3, 'Battle Arena', 49.99);

INSERT INTO purchase (purchase_id, game_id, person_id, purchase_date) VALUES
(1, 1, 1, '2023-04-01'),
(2, 2, 1, '2023-04-10'),
(3, 2, 2, '2023-04-12'),
(4, 3, 3, '2023-05-01');

INSERT INTO review (review_id, person_id, game_id, comment, rating, timestamp) VALUES
(1, 1, 1, 'Really fun classic!', 4, '2023-04-02 14:30:00'),
(5, 1, 2, "Not Great", 3, '2023-04-02 14:30:00'),
(6, 1, 3, "Terrible!", 1, '2023-04-02 14:30:00'),
(2, 1, 2, 'Pretty good, but short.', 4, '2023-04-11 16:45:00'),
(3, 2, 2, 'Not my style.', 2, '2023-04-13 10:15:00'),
(4, 3, 3, 'Amazing graphics!', 5, '2023-05-02 09:00:00');

INSERT INTO tag (tag_id, name) VALUES
(1, 'Action'),
(2, 'RPG'),
(3, 'Multiplayer'),
(4, 'Retro');

INSERT INTO game_tag (game_id, tag_id) VALUES
(1, 4), -- Space Invaders -> Retro
(1, 1), -- Space Invaders -> Action
(2, 2), -- Mystic Quest -> RPG
(3, 1), -- Battle Arena -> Action
(3, 3); -- Battle Arena -> Multiplayer
