# 🏗️ Arquitectura del Sistema SistPROF

Este diagrama muestra cómo interactúan los usuarios con el frontend, la lógica del backend en Flask y la base de datos PostgreSQL.

```mermaid
graph TD
    %% Estilos
    classDef user fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef frontend fill:#e1f5fe,stroke:#03a9f4,stroke-width:2px;
    classDef backend fill:#fff3e0,stroke:#ff9800,stroke-width:2px;
    classDef db fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    classDef ext fill:#fce4ec,stroke:#e91e63,stroke-width:2px;

    %% Usuarios
    subgraph Actors
        direction TB
        U_Admin["👤 Admin / Superadmin"]:::user
        U_Doc["👨‍ Docente"]:::user
        U_Acu["👪 Acudiente"]:::user
        U_Est["🎓 Estudiante"]:::user
    end

    %% Aplicación
    subgraph SistPROF_SaaS
        direction LR
        
        subgraph Frontend_Layer["Frontend Web"]
            F_Browser["🌐 Navegador Web"]:::frontend
            F_Temp["📄 Plantillas Jinja2 / CSS"]:::frontend
        end

        subgraph Backend_Layer["Backend Flask"]
            B_App["⚙️ App Logic Routes"]:::backend
            B_Auth["🔐 Auth Service"]:::backend
            B_Service["🛠️ Business Services"]:::backend
            B_MW["🛡️ Middleware Roles"]:::backend
        end

        subgraph DB_Layer["Base de Datos"]
            DB_PG["(🐘 PostgreSQL)"]:::db
            DB_Admin["🗄️ PGAdmin"]:::db
        end
        
        %% Módulos Internos
        M_Auth["🔑 Autenticación"]:::backend
        M_Esc["🏫 Gestión Escolar"]:::backend
        M_Aca["📚 Académico"]:::backend
        M_Seg["📋 Seguimiento"]:::backend
        M_Eva["📝 Evaluación"]:::backend
    end

    %% Externos
    subgraph Externos["Servicios Externos"]
        EXT_File["📂 Archivos Storage"]:::ext
        EXT_API["🔗 APIs Externas"]:::ext
        EXT_AI["🤖 AI Services"]:::ext
    end

    %% Relaciones
    U_Admin -->|HTTPS| F_Browser
    U_Doc -->|HTTPS| F_Browser
    U_Acu -->|HTTPS| F_Browser
    U_Est -->|HTTPS| F_Browser

    F_Browser <-->|HTTP REST| B_App
    F_Temp <--> B_App

    B_App --> B_Auth
    B_App --> B_Service
    B_MW -.-> B_App

    B_Service <--> DB_PG
    DB_Admin <--> DB_PG

    %% Conexión Módulos a DB
    M_Auth <--> DB_PG
    M_Esc <--> DB_PG
    M_Aca <--> DB_PG
    M_Seg <--> DB_PG
    M_Eva <--> DB_PG

    %% Conexiones Externas
    M_Eva <--> EXT_AI
    M_Esc <--> EXT_File
    B_Service <--> EXT_API
