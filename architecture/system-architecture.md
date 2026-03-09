# System Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        CLIENT[API Client/Postman/cURL]
    end

    subgraph "Docker Environment"
        subgraph "Application Layer"
            WEB[Django Web Server<br/>Port 8000]
            CELERY[Celery Worker<br/>Background Tasks]
        end

        subgraph "Data Layer"
            DB[(PostgreSQL Database<br/>Port 5432)]
            REDIS[(Redis Cache<br/>Port 6379)]
        end

        subgraph "Static Files"
            EXCEL[Excel Files<br/>customer_data.xlsx<br/>loan_data.xlsx]
        end
    end

    CLIENT -->|HTTP/REST API| WEB
    WEB -->|SQL Queries| DB
    WEB -->|Enqueue Tasks| REDIS
    CELERY -->|Dequeue Tasks| REDIS
    CELERY -->|Data Processing| DB
    EXCEL -.->|Initial Import| WEB

    style CLIENT fill:#e1f5ff
    style WEB fill:#bbdefb
    style CELERY fill:#c5e1a5
    style DB fill:#fff9c4
    style REDIS fill:#ffccbc
    style EXCEL fill:#f8bbd0
```

## Key Components

- **Django Web Server**: Handles API requests and business logic
- **Celery Worker**: Processes background tasks asynchronously
- **PostgreSQL**: Primary data store for customers and loans
- **Redis**: Message broker for Celery task queue
- **Excel Files**: Source data for initial system setup
