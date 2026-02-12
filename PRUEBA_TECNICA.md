# Prueba Técnica — Gestión de Usuarios (Flask + Docker)

## Contexto

Se te entrega un sistema de gestión de usuarios desarrollado en Flask con PostgreSQL, dockerizado y listo para levantar con `docker compose up --build`. La aplicación funciona, pero los usuarios han reportado varios problemas. Tu trabajo es **identificar dónde está el problema en el código, explicar qué lo causa y proponer cómo lo resolverías**.

No necesitas escribir código, solo indicar:
- **Qué archivo(s) y qué sección modificarías**
- **Qué enfoque tomarías para resolverlo**
- **Qué consideraciones técnicas hay que tener en cuenta**

---

## Estructura del Proyecto

```
app/
├── __init__.py                  # Factory de la aplicación
├── database.py                  # Conexión a PostgreSQL
├── models/
│   └── user.py                  # Modelo User
├── dtos/
│   └── user_dto.py              # Data Transfer Object
├── repositories/
│   └── user_repository.py       # Acceso a datos (SQL directo)
├── routes/
│   └── user_routes.py           # Rutas / controlador
└── templates/
    ├── base.html                # Layout base
    └── users.html               # Vista principal
config.py                        # Configuración
docker-compose.yml               # Orquestación
Dockerfile                       # Imagen de la app
init.sql                         # Datos iniciales (300 usuarios)
```

---

## Problema 1 — Carga lenta de la página principal

**Reporte del usuario:**
> "La página principal tarda mucho en cargar. Tenemos 300 usuarios y se siente pesado. Antes teníamos 20 y andaba rápido."

**Preguntas para el candidato:**
1. ¿Qué está causando la lentitud?
2. ¿En qué archivo(s) y en qué parte del código implementarías la solución?
3. ¿Cómo debería reflejarse la paginación en la URL para que el equipo de soporte pueda compartir enlaces a páginas específicas? (Por ejemplo, si un usuario de soporte quiere decirle a otro "revisa la página 5")
4. ¿Qué pasa con la paginación cuando el usuario está buscando? ¿Cómo convivirían ambas funcionalidades?

---

## Problema 2 — No se puede buscar usuarios por ID

**Reporte del usuario:**
> "El equipo de soporte necesita buscar usuarios por su número de ID. Cuando escribo un número como '42' en el buscador, no me encuentra al usuario con ID 42, solo me muestra usuarios que tengan '42' en su nombre o email."

**Preguntas para el candidato:**
1. ¿En qué parte del código está la lógica de búsqueda y por qué no funciona con IDs?
2. ¿Qué cambios harías y dónde?
3. Si el usuario busca "12", ¿debería mostrar solo el usuario con ID 12, o también usuarios con "12" en su nombre/email? Justifica tu decisión.
4. ¿Cómo interactúa esto con la paginación del Problema 1? ¿Los resultados de búsqueda también deberían paginarse?

---

## Problema 3 — Caracteres especiales en el buscador

**Reporte del usuario:**
> "Cuando escribo ciertos caracteres en el buscador se comporta raro. A veces me muestra todos los usuarios, a veces no muestra ninguno."

**Preguntas para el candidato:**
1. Revisa la lógica de búsqueda. ¿Qué caracteres podrían causar este comportamiento y por qué?
2. ¿Dónde implementarías la solución?
3. ¿Hay caracteres que sí deberían permitirse en la búsqueda a pesar de ser "especiales"? ¿Cuáles y por qué?
4. ¿Qué impacto de seguridad podrían tener estos caracteres si no se manejan correctamente?

---

## Problema 4 — Validación de datos al crear usuarios

**Reporte del usuario:**
> "Un compañero creó un usuario con el email 'hola' y el sistema lo aceptó cuando lo hizo desde una herramienta externa. Desde el navegador no lo deja, pero queremos asegurarnos de que no pase."

**Preguntas para el candidato:**
1. ¿Dónde se está validando actualmente el formato del email? ¿Es suficiente?
2. ¿En qué capa(s) de la aplicación agregarías validación y por qué?
3. ¿Qué pasa si alguien envía un nombre de 500 caracteres? ¿El sistema lo maneja correctamente?
4. ¿Qué diferencia hay entre validación del lado del cliente y del lado del servidor en este contexto?

---

## Problema 5 — Conexiones a la base de datos

**Reporte del usuario:**
> "Cuando hay varios usuarios usando la aplicación al mismo tiempo, a veces da errores de conexión a la base de datos."

**Preguntas para el candidato:**
1. Revisa cómo se manejan las conexiones a la base de datos. ¿Qué patrón se está usando actualmente?
2. ¿Qué problema tiene este enfoque cuando hay múltiples usuarios concurrentes?
3. ¿Qué solución propondrías y en qué archivo la implementarías?
4. ¿Qué es un pool de conexiones y cómo ayudaría aquí?

---

## Criterios de Evaluación

| Criterio | Peso |
|---|---|
| Identifica correctamente la ubicación del problema en el código | 25% |
| Propone una solución técnica coherente | 25% |
| Considera efectos secundarios e interacciones entre funcionalidades | 20% |
| Demuestra conocimiento de buenas prácticas (seguridad, rendimiento) | 15% |
| Claridad en la comunicación de la solución | 15% |

---

## Notas para el entrevistador

### Problema 1 (Paginación)
- **Ubicación:** `user_repository.py` (query sin LIMIT/OFFSET), `user_routes.py` (no recibe parámetro de página), `users.html` (no tiene controles de paginación).
- **URL esperada:** `/?page=2` o `/?page=3&q=carlos` cuando se combina con búsqueda.
- La búsqueda debería resetear a página 1.

### Problema 2 (Búsqueda por ID)
- **Ubicación:** `user_repository.py` método `search()` — solo filtra por `name` y `email` con LIKE, no tiene condición para `id`.
- Buena respuesta: detectar si el query es numérico y agregar `OR id = %s` a la consulta.
- Punto extra: discutir si el match por ID debería ser exacto vs. parcial.

### Problema 3 (Caracteres especiales)
- **Ubicación:** `user_repository.py` método `search()` — el `%` se pasa directo al LIKE sin escapar.
- El `%` es wildcard de SQL LIKE: buscar `%` devuelve todos los resultados.
- El `_` también es wildcard (cualquier carácter individual).
- **Trampa:** el `@` SÍ debería funcionar porque es un carácter literal en LIKE. Buscar por email parcial como `juan@` debería ser válido. Un candidato que bloquee el `@` no está pensando en el caso de uso.
- Solución: escapar `%` y `_` antes de interpolar en el LIKE.

### Problema 4 (Validación)
- La validación actual es solo `type="email"` en el HTML (lado del cliente).
- En `user_routes.py` solo se valida que no estén vacíos.
- La DB tiene `VARCHAR(100)` para name y `VARCHAR(120)` para email — un string largo haría fallar la query con un error no controlado.
- Buena respuesta: validar formato de email y longitud máxima en la ruta o en una capa de servicio/validación.

### Problema 5 (Conexiones)
- **Ubicación:** `database.py` — cada llamada crea una nueva conexión con `psycopg2.connect()` y la cierra al finalizar.
- Sin pooling, bajo carga se agotan las conexiones de PostgreSQL (por defecto 100).
- Solución: usar `psycopg2.pool.SimpleConnectionPool` o `ThreadedConnectionPool` en `database.py`.
