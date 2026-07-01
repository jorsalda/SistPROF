# 📋 GUÍA DE MIGRACIÓN FLASK + FLY.IO + SUPABASE

## RESUMEN DE DIFICULTADES Y SOLUCIONES

| # | COMANDO / ACCIÓN | DESCRIPCIÓN DEL PROCESO Y PROBLEMAS ENCONTRADOS |
|---|---|---|
| **1** | `flask db migrate -m "descripcion"` | **PROCESO:** Genera archivo de migración comparando modelos locales con BD conectada en `.env`. **DIFICULTAD:** Si `.env` apunta a BD local, la migración NO sirve para producción. **SOLUCIÓN:** Verificar que `SQLALCHEMY_DATABASE_URI` en `.env` apunte a Supabase (sin `#` al inicio). |
| **2** | `grep SQLALCHEMY_DATABASE_URI .env` | **VERIFICACIÓN:** Confirmar que la línea NO tenga `#` al inicio. Si está comentada, Flask usará otra BD por defecto y la migración será incorrecta. |
| **3** | `rm migrations/versions/XXXX_archivo.py` | **DIFICULTAD:** Si generaste migración con BD equivocada, BÓRRALA antes de continuar. No la subas a GitHub. |
| **4** | `git add migrations/versions/XXXX.py`<br>`git add -u`<br>`git commit -m "mensaje"`<br>`git push origin main` | **PROCESO:** Sube archivo de migración a GitHub. **IMPORTANTE:** Solo sube migraciones verificadas que apunten a la BD correcta. |
| **5** | `fly deploy` | **PROCESO:** Despliega código en Fly.io. **DIFICULTAD:** Puede tardar 3-10 minutos. Si se queda pegado más de 5 min, presiona `Ctrl+C` y vuelve a ejecutar. |
| **6** | `fly machine start` | **PROCESO:** Inicia máquinas detenidas en Fly.io. **DIFICULTAD:** Si aparece menú interactivo, usa flecha `→` para seleccionar todas y Enter. Si falla, usa `fly machine start ID_MAQUINA` directamente. |
| **7** | `fly ssh console -C "sh -c 'export LD_LIBRARY_PATH=/layers/paketo-buildpacks_cpython/cpython/lib && export PYTHONPATH=/layers/paketo-buildpacks_pip-install/packages/lib/python3.10/site-packages && /layers/paketo-buildpacks_pip-install/packages/bin/flask db upgrade'"` | **PROCESO:** Ejecuta migración en Fly.io. **DIFICULTAD:** Se puede quedar pegado por el pooler de Supabase (puerto 6543). **SOLUCIÓN:** Si tarda más de 3 min, cancelar con `Ctrl+C` y ejecutar `flask db upgrade` desde tu terminal local. |
| **8** | `flask db upgrade` (en local) | **ALTERNATIVA:** Si la migración falla en Fly.io, ejecutarla desde tu PC local (siempre que `.env` apunte a Supabase). Es más rápido y evita bloqueos del pooler. |
| **9** | `python3 -c "f='ruta_archivo'; text=open(f).read(); text=text.replace('texto_viejo','texto_nuevo'); open(f,'w').write(text)"` | **DIFICULTAD:** Errores en archivo de migración (FK incorrectas, typos). **SOLUCIÓN:** Usar Python para reemplazar texto automáticamente sin abrir editor. Más seguro que `nano`. |
| **10** | **Error: `InvalidForeignKey: no unique constraint matching`** | **CAUSA:** Foreign key compuesta `['sede_id', 'colegio_id']` referencia tabla `sedes` que no tiene UNIQUE en esa combinación. **SOLUCIÓN:** Simplificar FK a solo `['sede_id']` (el ID ya es único). |
| **11** | **Error: `there is no unique constraint matching given keys`** | **CAUSA:** Tu modelo `Coordinador` usa `ForeignKeyConstraint` compuesta. **SOLUCIÓN:** Editar archivo de migración y cambiar FK compuesta por FK simple. |
| **12** | `pip install -r requirements.txt` | **PROCESO:** Después de agregar paquete nuevo a `requirements.txt`, instalarlo localmente. Si no, PyCharm mostrará advertencia amarilla. |

---

## ✅ FLUJO CORRECTO DE TRABAJO (PASO A PASO)

| PASO | COMANDO | QUÉ HACE |
|---|---|---|
| **1** | Verificar `.env` apunta a Supabase | Asegura que migraciones se harán contra BD correcta |
| **2** | `flask db migrate -m "descripcion"` | Genera archivo de migración comparando modelos con Supabase |
| **3** | Revisar archivo generado | Verificar que NO tenga FK compuestas problemáticas |
| **4** | `flask db upgrade` (local) | Aplica cambios a Supabase desde tu PC (más rápido que Fly.io) |
| **5** | `git add . && git commit -m "mensaje"` | Guarda cambios en Git local |
| **6** | `git push origin main` | Sube código a GitHub |
| **7** | `fly deploy` | Despliega código nuevo en Fly.io |
| **8** | Verificar en navegador | Confirmar que aplicación funciona en producción |

---

## ⚠️ REGLAS DE ORO PARA NO PERDER DATOS

| REGLA | EXPLICACIÓN |
|---|---|
| **NUNCA eliminar tablas/columnas en producción** | Si ya no se usan, dejarlas en BD. El código simplemente deja de usarlas. |
| **Siempre hacer backup antes de `flask db upgrade`** | En Supabase: Database → Backups → New Backup |
| **Las migraciones deben ser ADITIVAS** | Solo `CREATE TABLE`, `ADD COLUMN`. Nunca `DROP`. |
| **Usar "Soft Delete" para usuarios** | En lugar de borrar, agregar columna `activo = False` |
| **Probar migración en local primero** | Ejecutar `flask db upgrade` en local antes de producción |

---

## 🔧 COMANDOS DE EMERGENCIA

| SITUACIÓN | COMANDO |
|---|---|
| Máquina detenida en Fly.io | `fly machine start ID_MAQUINA` |
| Ver estado de máquinas | `fly status` |
| Ver logs de la app | `fly logs` |
| Cancelar proceso pegado | `Ctrl + C` |
| Restaurar backup en Supabase | Panel Supabase → Database → Backups → Restore |
| Ver qué migraciones están aplicadas | `flask db current` |
| Ver historial de migraciones | `flask db history` |

---

## 📌 NOTAS IMPORTANTES

1. **Dos cosas separadas:**
   - **Código** (Flask/HTML/jQuery) → Se actualiza con `git push` + `fly deploy`
   - **Base de datos** (tablas/columnas) → Se actualiza con `flask db migrate` + `flask db upgrade`

2. **El archivo de migración es un "plan":**
   - `flask db migrate` = Genera el plan
   - `flask db upgrade` = Ejecuta el plan

3. **Siempre verificar antes de ejecutar:**
   - ¿`.env` apunta a Supabase?
   - ¿El archivo de migración tiene FK compuestas?
   - ¿Hay comandos `DROP` que puedan borrar datos importantes?

---

**Última actualización:** 11 de junio de 2026  
**Proyecto:** SistPROF  
**Estado:** ✅ Migración completada exitosamente