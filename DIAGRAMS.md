# Restaurant Reservation System - Diagrams and Visual Documentation

## 1. Application Flow Chart

This flowchart shows the complete user journey and system workflow for both customers and administrators.

```mermaid
graph TD
    A[Customer Visits Website] --> B{User Type?}
    B -->|New Customer| C[Customer Portal]
    B -->|Admin/Staff| D[Login Page]
    
    C --> E[Select Date & Time]
    E --> F[Enter Party Size]
    F --> G[Check Table Availability]
    G --> H{Tables Available?}
    H -->|Yes| I[Display Available Tables]
    H -->|No| J[Show No Tables Message]
    
    I --> K[Auto-Select Best Table]
    K --> L[Enter Customer Details]
    L --> M[Submit Reservation]
    M --> N[Create Customer Record]
    N --> O[Create Reservation Record]
    O --> P[Show Confirmation]
    
    D --> Q[Enter Credentials]
    Q --> R{Valid Login?}
    R -->|No| S[Show Error Message]
    R -->|Yes| T[Admin Dashboard]
    
    S --> Q
    
    T --> U[View Today Reservations]
    T --> V[Manage All Reservations]
    T --> W[Manage Tables]
    T --> X[View Statistics]
    
    U --> Y{Action Required?}
    Y -->|Confirm| Z[Update Status to Confirmed]
    Y -->|Cancel| AA[Update Status to Cancelled]
    Y -->|Search| BB[Filter Reservations]
    
    V --> CC[View All Reservations]
    CC --> DD[Search by Name Phone]
    CC --> EE[Bulk Operations]
    
    W --> FF[Add New Table]
    W --> GG[Update Table Status]
    W --> HH[Modify Table Capacity]
    
    X --> II[Occupancy Rate]
    X --> JJ[Revenue Statistics]
    X --> KK[Customer Analytics]
    
    Z --> LL[Send Confirmation]
    AA --> MM[Send Cancellation Notice]
    
    LL --> NN[Update Dashboard]
    MM --> NN
    BB --> NN
    
    style A fill:#e1f5fe
    style C fill:#f3e5f5
    style D fill:#fff3e0
    style T fill:#e8f5e8
    style P fill:#e8f5e8
    style NN fill:#fff9c4
```

## 2. Entity Relationship Diagram (ERD)

This ERD shows the database structure and relationships between entities.

```mermaid
erDiagram
    CUSTOMERS ||--o{ RESERVATIONS : makes
    TABLES ||--o{ RESERVATIONS : assigned_to
    USERS ||--o{ RESERVATIONS : manages
    
    CUSTOMERS {
        int customer_id PK
        varchar first_name
        varchar last_name
        varchar phone UK
        varchar email UK
        datetime created_at
        datetime updated_at
    }
    
    TABLES {
        int table_id PK
        int table_number UK
        int capacity
        enum status
        varchar location
        datetime created_at
        datetime updated_at
    }
    
    RESERVATIONS {
        int reservation_id PK
        int customer_id FK
        int table_id FK
        date reservation_date
        time reservation_time
        int party_size
        enum status
        text special_requests
        datetime created_at
        datetime updated_at
    }
    
    USERS {
        int user_id PK
        varchar username UK
        varchar password_hash
        enum role
        varchar email UK
        datetime created_at
        datetime last_login
    }
```

## 3. System Architecture Diagram

This diagram illustrates the overall system architecture and component relationships.

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Customer Portal<br/>HTML/CSS/JS]
        B[Admin Dashboard<br/>HTML/CSS/JS]
        C[Mobile Interface<br/>Responsive Design]
    end
    
    subgraph "Application Layer"
        D[Flask Web Framework]
        E[Authentication<br/>Flask-Login]
        F[ORM Layer<br/>SQLAlchemy]
        G[API Endpoints<br/>RESTful Services]
    end
    
    subgraph "Business Logic"
        H[Reservation Manager]
        I[Table Assignment Logic]
        J[Customer Management]
        K[User Authentication]
        L[Notification System]
    end
    
    subgraph "Database Layer"
        M[(MySQL Database)]
        N[Customers Table]
        O[Tables Table]
        P[Reservations Table]
        Q[Users Table]
    end
    
    subgraph "External Services"
        R[Cloud Hosting<br/>Railway/Render]
        S[Domain/DNS<br/>Cloudflare]
        T[Version Control<br/>GitHub]
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> E
    D --> F
    D --> G
    
    E --> K
    F --> H
    F --> I
    F --> J
    G --> L
    
    H --> M
    I --> M
    J --> M
    K --> M
    
    M --> N
    M --> O
    M --> P
    M --> Q
    
    D --> R
    R --> S
    D --> T
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style M fill:#e8f5e8
    style R fill:#fff9c4
```

## Diagram Explanations

### Application Flow Chart
- **Blue**: Entry points and user interactions
- **Purple**: Customer-facing processes
- **Orange**: Administrative processes
- **Green**: Success states and dashboard
- **Yellow**: System updates and notifications

### ERD Relationships
- **One-to-Many**: One customer can have many reservations
- **One-to-Many**: One table can have many reservations
- **One-to-Many**: One user can manage many reservations
- **Constraints**: Unique constraints on phone, email, username
- **Keys**: Primary keys (PK), Foreign keys (FK), Unique keys (UK)

### System Architecture
- **Frontend Layer**: User interface components
- **Application Layer**: Core Flask framework and services
- **Business Logic**: Application-specific business rules
- **Database Layer**: Data persistence and management
- **External Services**: Deployment and hosting infrastructure

## Technical Specifications

### Database Constraints
- **Primary Keys**: Auto-increment integers for all tables
- **Foreign Keys**: Referential integrity between related tables
- **Unique Constraints**: Prevent duplicate customers and table assignments
- **Check Constraints**: Ensure positive values for capacity and party size
- **Indexes**: Optimized for common query patterns

### API Endpoints
- **GET /api/tables/available**: Check table availability
- **POST /api/reservations**: Create new reservation
- **PUT /api/reservations/{id}/confirm**: Confirm reservation
- **PUT /api/reservations/{id}/cancel**: Cancel reservation
- **GET /api/stats**: System statistics

### Security Features
- **Authentication**: Flask-Login session management
- **Authorization**: Role-based access control
- **Data Protection**: Input validation and sanitization
- **SQL Injection Prevention**: ORM parameterized queries
