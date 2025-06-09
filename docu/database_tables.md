# Diagrama ER - Sistema de Biblioteca

## Descripción del Sistema
Este diagrama muestra las relaciones entre las tablas principales de un sistema de gestión de biblioteca.

## Diagrama de Entidad-Relación

```mermaid
erDiagram
    USUARIOS {
        int id_usuario PK
        varchar nombre
        varchar email UK
        varchar telefono
        date fecha_registro
        enum tipo_usuario
    }
    
    LIBROS {
        int id_libro PK
        varchar titulo
        varchar isbn UK
        int año_publicacion
        int numero_paginas
        int id_editorial FK
        enum estado_libro
    }
    
    AUTORES {
        int id_autor PK
        varchar nombre_completo
        date fecha_nacimiento
        varchar nacionalidad
        text biografia
    }
    
    EDITORIALES {
        int id_editorial PK
        varchar nombre_editorial
        varchar direccion
        varchar telefono
        varchar email
    }
    
    PRESTAMOS {
        int id_prestamo PK
        int id_usuario FK
        int id_libro FK
        date fecha_prestamo
        date fecha_devolucion_esperada
        date fecha_devolucion_real
        enum estado_prestamo
    }
    
    LIBRO_AUTOR {
        int id_libro FK
        int id_autor FK
    }
    
    CATEGORIAS {
        int id_categoria PK
        varchar nombre_categoria
        text descripcion
    }
    
    LIBRO_CATEGORIA {
        int id_libro FK
        int id_categoria FK
    }

    %% Relaciones
    USUARIOS ||--o{ PRESTAMOS : "realiza"
    LIBROS ||--o{ PRESTAMOS : "es prestado"
    LIBROS }o--|| EDITORIALES : "publicado por"
    LIBROS }o--o{ AUTORES : "escrito por"
    LIBROS }o--o{ CATEGORIAS : "pertenece a"
    AUTORES }o--o{ LIBROS : "escribe"
    CATEGORIAS }o--o{ LIBROS : "contiene"
```

## Explicación de las Relaciones

### Relaciones Principales:
- **USUARIOS → PRESTAMOS**: Un usuario puede tener múltiples préstamos (1:N)
- **LIBROS → PRESTAMOS**: Un libro puede ser prestado múltiples veces (1:N)
- **EDITORIALES → LIBROS**: Una editorial puede publicar múltiples libros (1:N)

### Relaciones Muchos a Muchos:
- **LIBROS ↔ AUTORES**: Un libro puede tener varios autores y un autor puede escribir varios libros
- **LIBROS ↔ CATEGORIAS**: Un libro puede pertenecer a varias categorías y una categoría puede contener varios libros

### Tablas de Unión:
- **LIBRO_AUTOR**: Resuelve la relación muchos a muchos entre libros y autores
- **LIBRO_CATEGORIA**: Resuelve la relación muchos a muchos entre libros y categorías

## Leyenda de Símbolos
- `PK`: Primary Key (Clave Primaria)
- `FK`: Foreign Key (Clave Foránea)
- `UK`: Unique Key (Clave Única)
- `||--o{`: Relación uno a muchos
- `}o--o{`: Relación muchos a muchos
- `}o--||`: Relación muchos a uno