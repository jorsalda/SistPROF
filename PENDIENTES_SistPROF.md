
---

## TEMA-029: Migración de Almacenamiento Local a Object Storage (Producción)

**Prioridad:** Media
**Estado:** Pendiente (Idea para futuro)
**Fecha de registro:** 2026-11-04
**Origen:** Chat Docente-Estud (Módulo de Exámenes - Contexto)

### Contexto
Actualmente, los archivos de contexto (imágenes y videos) de las preguntas se guardan en la carpeta local \`static/uploads/contexto/\`. Esto funciona bien para desarrollo y despliegues de una sola instancia (como el plan actual en Fly.io). Sin embargo, si el sistema escala a múltiples instancias o el volumen de archivos crece significativamente (especialmente videos), el almacenamiento local puede convertirse en un cuello de botella.

### Consecuencia
- **Límite de disco:** Los volúmenes de Fly.io tienen un costo y un límite. Si muchos docentes suben videos, el disco se llenará.
- **Problemas de concurrencia:** Si se despliegan múltiples instancias (máquinas) para manejar más usuarios, los archivos subidos a una instancia no serán visibles en las otras.
- **Rendimiento:** Servir archivos estáticos grandes desde el servidor de la aplicación puede consumir recursos de CPU y memoria.

### Plan de tratamiento (Futuro)
1.  **Definir umbral:** Establecer un límite de uso (ej. 5 colegios o 50 GB) que dispare la migración.
2.  **Elegir proveedor:** Seleccionar un Object Storage (AWS S3, Cloudflare R2, Google Cloud Storage, etc.).
3.  **Adaptar Backend:** Modificar la lógica de guardado en \`nueva_pregunta_banco\` (y cualquier otra ruta que suba archivos) para que, en lugar de guardar en el disco local, envíe el archivo al proveedor externo y guarde solo la URL pública en la base de datos.
4.  **Migrar archivos existentes:** Script que mueva los archivos actuales de \`static/uploads/\` al nuevo proveedor y actualice las rutas en la base de datos.
5.  **Configurar CORS:** Asegurar que el frontend pueda cargar las imágenes/videos desde el dominio del proveedor externo.

### Reglas
- No modificar la lógica de subida actual hasta que se decida el proveedor y se haga el análisis de costos.
- Mantener compatibilidad con el código actual (el campo \`contexto\` en la BD seguirá guardando una URL, ya sea local o externa).

