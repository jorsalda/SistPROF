# 📘 Guía de Actualización Segura de Repositorios — SistPROF

**Autor:** Tutor de SistPROF  
**Fecha:** 2026-08-19  
**Propósito:** Evitar que secretos, backups o archivos duplicados entren en los commits y bloqueen los pushes a GitHub/GitLab.

---

## 🎯 Antes de empezar

> **Regla de oro:** Nunca hagas `git add .` sin revisar primero. Siempre verifica qué vas a subir.

---

## 📋 Protocolo paso a paso

| # | Comando | Explicación |
|---|---------|-------------|
| 1 | `cd ~/PycharmProjects/SistPROF` | Asegúrate de estar en la raíz del proyecto. Si estás en una subcarpeta (ej. `static/js`), las rutas se verán raras y puedes cometer errores. |
| 2 | `git status` | **Paso más importante.** Te muestra exactamente qué archivos cambiaste, cuáles son nuevos y cuáles están en el área de stage. Revisa con calma antes de hacer `git add`. |
| 3 | `git restore --staged archivo.back` | Si ves archivos con extensiones `.back`, `.Back`, `.bak`, `.1`, `.2` o similares en "Cambios a ser confirmados", sácalos del stage. Son duplicados o backups que no deben entrar al repo. |
| 4 | `git add app/routes/docente_routes.py` | Agrega **uno por uno** (o en grupos pequeños) los archivos que SÍ quieres subir. Nunca uses `git add .` a ciegas. |
| 5 | `git diff --cached | grep -i -E "(api_key|apikey|secret|password|token|clave)" | grep -v ".env" | head -20` | **Verificación de seguridad.** Revisa que no haya claves API, contraseñas o tokens hardcodeados en lo que vas a commitear. Si aparece algo, revisa si es código legítimo (ej. `csrf_token()`) o un secreto real. |
| 6 | `git commit -m "feat: descripción clara del cambio"` | Crea el commit con un mensaje descriptivo. Usa prefijos como `feat:`, `fix:`, `security:`, `chore:` para organizar el historial. |
| 7 | `git push origin main` | Sube el commit a **GitHub** primero. Si GitHub no bloquea, significa que no hay secretos expuestos. |
| 8 | `git push gitlab main` | Sube el mismo commit a **GitLab** para mantener ambos repositorios sincronizados. |
| 9 | `rm app/templates/examenes/crear_examen.html.back` | (Opcional) Elimina del disco los archivos de backup que quedaron como "sin seguimiento". Solo si ya no los necesitas localmente. |
| 10 | `git status` | Verificación final. Debe decir: *"nada para hacer commit, el árbol de trabajo está limpio"*. |

---

## 🔐 ¿Qué hacer si encuentras un secreto hardcodeado?

Si el paso 5 (`git diff --cached | grep`) te muestra una **clave real** (ej. `AIza...`, `AQ.Ab...`, `sk-...`, una contraseña real), **NO hagas commit**. Sigue este protocolo:

| Paso | Qué hacer | Explicación |
|------|-----------|-------------|
| 1 | **Aborta el commit** | No crees el commit con el secreto. Una vez en el historial, es mucho más difícil de eliminar. |
| 2 | **Mueve el secreto a `.env`** | Abre tu archivo `.env` y agrega la variable: `NOMBRE_CLAVE=tu_clave_aqui`. El `.env` ya debe estar en `.gitignore` para que no se suba. |
| 3 | **Modifica el código** para leer desde `.env` | Cambia el archivo para que use `os.getenv("NOMBRE_CLAVE")` en lugar del valor hardcodeado. Usa `from dotenv import load_dotenv` y `load_dotenv()` al inicio. |
| 4 | **Guarda y prueba** que el archivo funcione | Ejecuta localmente para verificar que la aplicación lee bien la clave desde `.env`. |
| 5 | **Haz `git add` del archivo limpio** | Ahora sí, agrega solo el archivo que ya no tiene el secreto. |
| 6 | **Vuelve a ejecutar el `grep` de verificación** | `git diff --cached | grep -i -E "(api_key|apikey|secret|password|token|clave)" | grep -v ".env" | head -20` — debe mostrar solo código legítimo. |
| 7 | **Commit y push normal** | Ahora sí puedes hacer commit y push con seguridad. |
| 8 | **Si el secreto ya fue expuesto** (ya está en GitHub o en commits anteriores) | Ve a la sección **"Protocolo de emergencia"** más abajo. Debes rotar la clave (generar una nueva) porque ya está comprometida. |

### Ejemplo: antes y después

**❌ ANTES (hardcodeado — NUNCA hagas esto):**
```python
API_KEY = "REDACTED_API_KEY"
```

**✅ DESPUÉS (lee desde `.env`):**
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")
```

**Y en tu `.env` (nunca se sube al repo):**
```bash
GEMINI_API_KEY=REDACTED_API_KEY
```

---

## ⚠️ Señales de alerta — NO hagas commit si ves esto

| Problema | Qué hacer |
|----------|-----------|
| Archivos `.back`, `.Back`, `.bak`, `.1`, `.2` en stage | `git restore --staged` y luego `rm` si no los necesitas. |
| `git diff --cached` muestra una clave real (ej. `AIza...`, `AQ.Ab...`) | Aborta el commit. Mueve la clave a `.env` y limpia el archivo antes de continuar (ver sección "¿Qué hacer si encuentras un secreto?" arriba). |
| GitHub bloquea el push con "Push cannot contain secrets" | El secreto ya está en el historial. Usa `git-filter-repo` para limpiar el historial completo (ver sección de emergencia). |
| `git status` muestra rutas con `../../` o `../` | Estás en una subcarpeta. Ve a la raíz con `cd ~/PycharmProjects/SistPROF`. |

---

## 🚨 Protocolo de emergencia: secreto ya commiteado

Si accidentalmente commiteaste un secreto y GitHub lo bloquea:

| Paso | Comando | Explicación |
|------|---------|-------------|
| 1 | `git branch backup-YYYY-MM-DD` | Crea un backup de tu rama actual por seguridad. |
| 2 | `pip install git-filter-repo` | Instala la herramienta que reescribe el historial de Git. |
| 3 | `echo 'CLAVE_REAL==>REDACTED_KEY' > replacements.txt` | Crea el archivo de reemplazo. **Nunca copies la clave real en el chat.** Hazlo directo en tu terminal. |
| 4 | `git filter-repo --replace-text replacements.txt --force` | Reescribe TODO el historial del repo, reemplazando la clave en todos los commits. |
| 5 | `rm replacements.txt` | Elimina el archivo temporal. |
| 6 | `git remote add origin https://github.com/jorsalda/SistPROF.git` | Reconecta GitHub (filter-repo borra los remotes). |
| 7 | `git push origin main --force` | Sube el historial limpio a GitHub. |
| 8 | `git push gitlab main --force` | Sube el historial limpio a GitLab. Si GitLab rechaza el force push, desprotege temporalmente `main` en Settings > Repository > Protected branches. |
| 9 | **Rotar la clave** | Ve a Google AI Studio / Google Cloud Console y genera una nueva clave. La vieja está comprometida. |

---

## 📝 Buenas prácticas de SistPROF

| Práctica | Por qué importa |
|----------|-----------------|
| **Claves en `.env`**, nunca en el código | GitHub escanea automáticamente los repos. Si detecta una clave, bloquea el push para siempre. |
| **`.env` en `.gitignore`** | Evita que tu archivo de variables locales se suba accidentalmente. |
| **No subir archivos `.backup`** | Ensucian el repo, confunden al equipo y pueden contener código viejo con bugs o secretos. |
| **Mensajes de commit descriptivos** | Facilita saber qué cambió y cuándo. Usa: `feat:`, `fix:`, `security:`, `chore:`, `docs:`. |
| **GitHub primero, GitLab después** | Si GitHub bloquea, lo descubres antes de tocar GitLab. |
| **Revisar `git status` antes de cada commit** | Es tu última oportunidad de detectar errores antes de que queden en el historial. |

---

## ✅ Checklist rápido antes de cada push

- [ ] Estoy en la raíz del proyecto (`~/PycharmProjects/SistPROF`)
- [ ] Revisé `git status` y no hay archivos `.back`, `.bak`, `.1`, `.2`
- [ ] Los archivos en stage son solo los que realmente quiero subir
- [ ] Verifiqué con `git diff --cached | grep` que no hay secretos hardcodeados
- [ ] Si encontré un secreto, lo moví a `.env` y el código ahora usa `os.getenv()`
- [ ] El mensaje de commit describe bien el cambio
- [ ] Hice push a GitHub primero (verifiqué que no bloqueó)
- [ ] Hice push a GitLab después (ambos quedaron sincronizados)
- [ ] El árbol de trabajo quedó limpio (`git status` sin archivos sin seguimiento importantes)

---

*Documento generado para Jorge Saldaña — Proyecto SistPROF.*