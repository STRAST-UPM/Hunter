# Data dictionary

## SQL structure

### Table: `` 

| Column | Type | Description |
|--------|------|-------------|
|        |      |             |

```sql

```

### Table: `ip_addresses`

| Column  | Type         | Description |
|---------|--------------|-------------|
| address | VARCHAR (PK) |             |

```sql

```

### Table: `pings`

| Column | Type | Description |
|--------|------|-------------|
|        |      |             |

```sql

```

### Table: `traceroutes`

| Columna    | Tipo         | Descripción                  |
|------------|--------------|------------------------------|
| id         | INTEGER (PK) | Unique ID  of the traceroute |
| timestamp  | DATETIME     | Date an time of execution    |
| origen_ip  | VARCHAR      | Origen IP                    |
| destino_ip | VARCHAR      | Destiny IP                   |

```sql
CREATE TABLE traceroutes (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    origen_ip VARCHAR NOT NULL,
    destino_ip VARCHAR NOT NULL
);
```

### Table: `traceroute_hops`

| Columna       | Tipo         | Descripción                    |
|---------------|--------------|--------------------------------|
| id            | INTEGER (PK) | Unique hop ID                  |
| traceroute_id | INTEGER (FK) | Forming key of the traceroute  |
| hop_position  | INTEGER      | Hop position in the traceroute |

```sql
CREATE TABLE traceroutes_hops (
    id SERIAL PRIMARY KEY,
    traceroute_id INTEGER NOT NULL REFERENCES traceroutes(id) ON DELETE CASCADE,
    hop_position INTEGER NOT NULL
);
```

### Table: `hops_reponses`

| Columna     | Tipo          | Descripción                            |
|-------------|---------------|----------------------------------------|
| id          | INTEGER (PK)  | Unique hop response ID                 |
| hop_id      | INTEGER (FK)  | Foreing reference to hop               |
| ip_address  | VARCHAR       | IP address from the host which respond |
| hostname    | VARCHAR       | Hostname (opcional)                    |
| rtt_ms      | FLOAT         | Round Trip Time in ms                  |

```sql
CREATE TABLE hops_responses (
    id SERIAL PRIMARY KEY,
    hop_id INTEGER NOT NULL REFERENCES traceroutes_hops(id) ON DELETE CASCADE,
    ip_address VARCHAR NOT NULL,
    hostname VARCHAR,
    rtt_ms FLOAT
);
```
