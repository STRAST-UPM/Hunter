# Hunter Entity-Relationship Description

## Sistem description
This diagram shows the relations between database tables in the Hunter system.

## Entity-Relationship Diagram

```mermaid
erDiagram
    ip_addresses {
        VARCHAR address PK
        BOOLEAN is_anycast
        BOOLEAN is_bogon
    }
    
    tracks{
        INTEGER id PK "SERIAL"
        INTEGER status "NOT NULL"
        VARCHAR status_description
        DATETIME timestamp
        VARCHAR ip_address FK
    }
    
    measurements {
        INTEGER id PK
        DATE timestamp
        INTEGER track_id FK
    }
    
    traceroutes_results {
        INTEGER id PK "SERIAL"
        DATETIME timestamp 
        INTEGER probe_id
        VARCHAR origin_ip
        VARCHAR destination_ip
        INTEGER measurement_id FK
    }
    
    traceroutes_hops {
        INTEGER id PK "SERIAL"
        INTEGER hop_position
        INTEGER traceroute_id FK
    }

    hops_reponses {
        INTEGER id PK "SERIAL"
        VARCHAR ip 
        VARCHAR hostname
        FLOAT rtt_ms
        INTEGER hop_id FK
    }

    pings_results {
        INTEGER id PK "SERIAL"
        DATETIME timestamp
        INTEGER probe_id
        VARCHAR origin_ip
        VARCHAR destination_ip
        FLOAT max_rtt_ms
        FLOAT min_rtt_ms
        FLOAT average_rtt_ms
        INTEGER measurement_id FK
    }
    
    %% Relations
    ip_addresses ||--o{ tracks : "IP is tracked"
    tracks ||--o{ measurements : "track using measurements"
    measurements ||--o{ traceroutes_results : "traceroute results of measurement"
    traceroutes_results ||--o{ traceroutes_hops : "hops"
    traceroutes_hops ||--o{ hops_reponses : "reponses"
    measurements ||--o{ pings_results : "ping results of measurement"
```

### Symbols legend
- `PK`: Primary Key
- `FK`: Foreign Key
- `UK`: Unique Key
- `||--o{`: One-to-Many relation
- `}o--o{`: Many-to-Many relation
