# 🧠 Comandos Git Útiles para Proyectos Académicos con Python

Este documento resume comandos esenciales para usar Git en proyectos de aprendizaje de Python, especialmente en contextos académicos y personales.

---

## 📦 1. Inicializar un repositorio

```bash
git init
```

> Inicializa Git en el directorio actual.

---

## 📁 2. Añadir archivos al área de preparación

```bash
git add archivo.py
git add .
```

> Añade uno o todos los archivos para ser parte del próximo commit.

---

## 📝 3. Guardar cambios (commit)

```bash
git commit -m "Descripción del cambio"
```

> Registra los cambios con un mensaje claro.

---

## 🔎 4. Ver estado del repositorio

```bash
git status
```

> Muestra archivos modificados, nuevos, o en staging.

---

## 📂 5. Ver historial de cambios

```bash
git log --oneline --graph --all
```

> Muestra un resumen visual del historial.

---

## 🧪 6. Crear y cambiar de rama (para pruebas o nuevas ideas)

```bash
git branch nueva-rama
git checkout nueva-rama
```

> Las ramas permiten experimentar sin dañar el código principal.

---

## 🧪 6.5. Verificar rama local y remota

```bash
git branch
git branch -vv
```

> Las ramas permiten experimentar sin dañar el código principal.

---

## 🔄 7. Fusionar una rama al main

```bash
git checkout main
git merge nueva-rama
```

---

## 🗑️ 8. Revertir cambios

```bash
git restore archivo.py
git checkout -- archivo.py
```

> Restaura un archivo al último commit.

---

## ☁️ 9. Enlazar repositorio con GitHub (una sola vez)

```bash
git remote add origin https://github.com/tu_usuario/tu_repo.git
```

---

## 🚀 10. Subir cambios a GitHub

```bash
git push -u origin main
```

---

## 📥 11. Obtener cambios del repositorio remoto

```bash
git pull origin main
```

---

## 🔍 12. Ignorar archivos no deseados

Crear archivo `.gitignore` y añadir líneas como:

```
__pycache__/
*.pyc
.env
.ipynb_checkpoints/
```

---

## 🎓 Recomendación para proyectos académicos

1. Cada tema puede estar en una carpeta separada con su propio README.md.
2. Usa commits pequeños y frecuentes.
3. Nombra ramas según el contenido: `tema-clases`, `ejercicios-listas`, `proyecto-final`, etc.
4. Agrega un README con tus objetivos de aprendizaje.

---

## ✅ Buenas prácticas

- `git pull` antes de comenzar a trabajar.
- `git push` después de cada sesión significativa.
- Documenta tus scripts con comentarios y markdown.

---
