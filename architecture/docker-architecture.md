# Docker Container Architecture

```mermaid
graph TB
    subgraph "Docker Compose Network: app-network"
        subgraph "web container"
            DJANGO[Django 6.0.3<br/>Python 3.12]
            DRF[Django REST Framework]
            ENTRYPOINT[entrypoint.sh]
            MIGRATIONS[Database Migrations]
            IMPORT_CMD[import_data command]
            SERVER[Development Server<br/>0.0.0.0:8000]
        end

        subgraph "celery container"
            CELERY_WORKER[Celery Worker]
            CELERY_TASKS[Background Tasks]
        end

        subgraph "db container"
            POSTGRES[PostgreSQL 15]
            PG_DATA[(Persistent Volume:<br/>postgres_data)]
            HEALTHCHECK_DB[Health Check:<br/>pg_isready]
        end

        subgraph "redis container"
            REDIS_SERVER[Redis 7 Alpine]
            REDIS_DATA[(In-Memory Store)]
            HEALTHCHECK_REDIS[Health Check:<br/>redis-cli ping]
        end
    end

    subgraph "Host Machine"
        PORT_8000[localhost:8000]
        PORT_5432[localhost:5432]
        PORT_6379[localhost:6379]
        VOLUME_MOUNT[Project Files<br/>Bind Mount: .:/app]
        EXCEL_FILES[customer_data.xlsx<br/>loan_data.xlsx]
    end

    ENTRYPOINT -->|1. Wait for DB| HEALTHCHECK_DB
    ENTRYPOINT -->|2. Run| MIGRATIONS
    ENTRYPOINT -->|3. Execute| IMPORT_CMD
    ENTRYPOINT -->|4. Start| SERVER

    DJANGO -->|SQL| POSTGRES
    DJANGO -->|Enqueue| REDIS_SERVER
    CELERY_WORKER -->|Dequeue| REDIS_SERVER
    CELERY_WORKER -->|Process| POSTGRES

    PORT_8000 -.->|HTTP| SERVER
    PORT_5432 -.->|TCP| POSTGRES
    PORT_6379 -.->|TCP| REDIS_SERVER
    
    VOLUME_MOUNT -.->|Mount| DJANGO
    VOLUME_MOUNT -.->|Mount| CELERY_WORKER
    EXCEL_FILES -.->|Available at| IMPORT_CMD

    PG_DATA -->|Persist| POSTGRES

    style DJANGO fill:#bbdefb
    style POSTGRES fill:#fff9c4
    style REDIS_SERVER fill:#ffccbc
    style CELERY_WORKER fill:#c5e1a5
    style PORT_8000 fill:#e1f5ff
    style EXCEL_FILES fill:#f8bbd0
    style PG_DATA fill:#ffe082
```

## Container Dependencies

```mermaid
graph LR
    DB[db container] -->|healthy| WEB[web container]
    REDIS[redis container] -->|healthy| WEB
    WEB -->|started| CELERY[celery container]
    DB -->|healthy| CELERY
    REDIS -->|healthy| CELERY

    style DB fill:#fff9c4
    style REDIS fill:#ffccbc
    style WEB fill:#bbdefb
    style CELERY fill:#c5e1a5
```

## Startup Sequence

1. **db** and **redis** containers start
2. Health checks verify services are ready
3. **web** container starts after dependencies are healthy
4. `entrypoint.sh` executes:
   - Waits for PostgreSQL connection
   - Runs database migrations
   - Imports Excel data
   - Starts Django server
5. **celery** container starts after web is ready
