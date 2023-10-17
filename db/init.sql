CREATE TABLE types (
  id              SERIAL PRIMARY KEY,
  name            VARCHAR(100) NOT NULL,
  max_speed       INTEGER NOT NULL
);

CREATE TABLE resources (
  id              SERIAL PRIMARY KEY,
  name            VARCHAR(100) NOT NULL,
  type_id         INTEGER NOT NULL,
  speed           INTEGER NOT NULL,
  CONSTRAINT fk_type FOREIGN KEY(type_id) REFERENCES types(id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO types (name, max_speed) VALUES ('car', 100);
INSERT INTO types (name, max_speed) VALUES ('motorcycle', 200);

INSERT INTO resources (name, type_id, speed) VALUES ('car1', 1, 90);
INSERT INTO resources (name, type_id, speed) VALUES ('car2', 1, 110);
INSERT INTO resources (name, type_id, speed) VALUES ('motorcycle1', 2, 100);
INSERT INTO resources (name, type_id, speed) VALUES ('motorcycle2', 2, 250);
