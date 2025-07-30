CREATE TABLE IF NOT EXISTS users
(
    id       INTEGER PRIMARY KEY AUTO_INCREMENT,
    login    TEXT,
    password TEXT,
    role     TEXT
);

INSERT INTO users(login, password, role)
VALUES ('a', 'a', 'user');

CREATE TABLE IF NOT EXISTS products
(
    id             INTEGER PRIMARY KEY AUTO_INCREMENT,
    name           VARCHAR(100)   NOT NULL,
    description    TEXT,
    price          DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER        NOT NULL DEFAULT 0,
    created_at     TIMESTAMP               DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP               DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO products (name, description, price, stock_quantity)
VALUES ('Смартфон X', 'Новейший смартфон с камерой 48 МП', 599.99, 100),
       ('Ноутбук Pro', 'Мощный ноутбук для работы и игр', 1299.99, 50),
       ('Наушники Wireless', 'Беспроводные наушники с шумоподавлением', 199.99, 200),
       ('Умные часы', 'Фитнес-трекер с мониторингом здоровья', 149.99, 75),
       ('Планшет Mini', 'Компактный планшет с экраном 8 дюймов', 349.99, 60),
       ('Внешний жесткий диск', '1 ТБ памяти, USB 3.0', 89.99, 120),
       ('Беспроводная клавиатура', 'Эргономичная клавиатура с подсветкой', 59.99, 90),
       ('Компьютерная мышь', 'Игровая мышь с 6 программируемыми кнопками', 49.99, 150);

CREATE TABLE cart
(
    id         INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id    INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity   INTEGER NOT NULL DEFAULT 1,
    added_at   TIMESTAMP        DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);