# 📘 TUTORIAL: MIGRACIONES Y DEPLOYS EN SISTPROF

Este documento es la guía oficial y el registro de las reglas de oro para desplegar SistPROF sin romper la base de datos ni la aplicación.

---

## 🚨 Las 3 Reglas de Oro (Aprendidas a la fuerza)

1. **Nunca uses `--autogenerate` a ciegas:** La BD local tiene mucha historia (tablas manuales, columnas viejas). Si lo usas, Alembic intentará borrar todo lo que no esté en los modelos de Python. Siempre revisa el archivo generado antes de aplicarlo.
2. **Verifica Supabase antes de hacer `stamp`:** Producción es sagrado. Si la tabla o columna no existe en Supabase, créala manualmente con SQL antes de hacer el `stamp`.
3. **Python 3.12 en Fly.io:** El `fly.toml` debe tener el builder `jammy-base` y la variable `BP_CPYTHON_VERSION = "3.12.*"`. Sin esto, las librerías modernas (como `supabase-py`) fallarán en el build.

---

## 📋 Flujo de Trabajo (Paso a Paso)

### FASE 1: PREPARACIÓN Y MIGRACIÓN LOCAL

| 💻 COMANDO | 📖 EXPLICACIÓN / REGLA |
| :--- | :--- |
| `git status` | **Regla de Oro:** Antes de tocar la BD, mira qué archivos has modificado. Asegúrate de saber qué modelos SQLAlchemy (`app/models/`) cambiaron. |
| `alembic -c migrations/alembic.ini revision --autogenerate -m "nombre_migracion"` | Genera el archivo de migración. **OJO:** Solo úsalo si estás seguro de que la BD local está sincronizada. Si hay muchas tablas viejas, **NO lo uses** (crea un archivo vacío con `alembic revision -m "..."` y escríbelo a mano). |
| *(Revisar archivo en `migrations/versions/`)* | **CRÍTICO:** Abre el archivo generado. Verifica que el `upgrade()` cree lo que quieres y el `downgrade()` lo borre. Si ves `op.drop_table()` de tablas que no quieres borrar, **detente**. |
| `alembic -c migrations/alembic.ini upgrade head` | Aplica los cambios a la **BD Local**. Si falla con "DuplicateColumn", significa que alguien ya creó esa columna a mano. En ese caso, **NO insistas**, pasa al `stamp`. |
| `alembic -c migrations/alembic.ini stamp <ID_MIGRACION>` | **El truco del almendruco:** Si la BD local ya tiene los cambios manualmente, este comando "miente" a Alembic y le dice "ya lo apliqué", sin ejecutar el SQL de nuevo. (Úsalo solo si verificaste en DBeaver que las columnas/tablas ya existen). |

### FASE 2: SINCRONIZACIÓN CON SUPABASE

| 💻 COMANDO | 📖 EXPLICACIÓN / REGLA |
| :--- | :--- |
| *(Revisar en SQL Editor de Supabase)* | Antes de tocar producción, verifica en Supabase con consultas `SELECT` si las columnas o tablas de tu migración ya existen o no. |
| `ALTER TABLE ...` (Vía SQL Editor) | **Si faltan cosas en Supabase:** No corras `upgrade` contra Supabase. Escribe el SQL manualmente en el editor de Supabase para crear solo lo que falta (columnas, tablas, FKs). |
| `export SUPABASE_URI="postgresql://..."` | **Nunca olvides esto.** Si no cargas la variable, el `stamp` se irá a Local en lugar de a Supabase. Verifica con `echo "$SUPABASE_URI"`. |
| `SQLALCHEMY_DATABASE_URI="$SUPABASE_URI" alembic -c migrations/alembic.ini stamp <ID_MIGRACION>` | Le dice a Supabase: "Ya tienes los cambios, márcalos como aplicados". **No toca el schema**, solo actualiza la tabla `alembic_version`. |
| `SELECT * FROM alembic_version;` | Verifica en Supabase que el ID de la migración quedó registrado correctamente. |

### FASE 3: COMMIT Y DEPLOY (FLY.IO)

| 💻 COMANDO | 📖 EXPLICACIÓN / REGLA |
| :--- | :--- |
| `git add -A`<br>`git commit -m "feat: descripcion"` | Guarda todos los cambios (modelos, migraciones, templates). |
| `git push origin main`<br>`git push gitlab main` | Sube el código a GitHub y GitLab. |
| `fly deploy --app sistprof` | **El despliegue final.** Empaqueta la app y la sube a Fly.io. |
| *(Si falla por versión de Python)* | **Regla de Oro:** Si ves un error de `contourpy` o `multidict` en el deploy, es porque Fly.io está usando Python 3.10. Abre `fly.toml` y asegúrate de tener: `builder = "paketobuildpacks/builder-jammy-base"` y `BP_CPYTHON_VERSION = "3.12.*"`. |

### FASE 4: ALMACENAMIENTO (SUPABASE STORAGE)

| 💻 CÓDIGO PYTHON | 📖 EXPLICACIÓN / REGLA |
| :--- | :--- |
| `supabase.storage.from_("contexto").upload(...)` | En lugar de guardar archivos en `static/uploads/`, usamos Supabase Storage. Esto evita que las imágenes/videos se borren en cada deploy. |
| `supabase.storage.from_("contexto").get_public_url(...)` | Obtenemos la URL pública de la imagen/video y la guardamos en la base de datos. |
