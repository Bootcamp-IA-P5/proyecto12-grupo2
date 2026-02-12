# Guía de Contribución

## Cómo Contribuir al Proyecto

### 1. Setup Inicial

```bash
# Clonar repositorio
git clone <repo-url>
cd proyecto12-grupo2

# Crear rama de feature
git checkout -b feature/tu-feature-aqui

# Setup ambiente (ver ENVIRONMENT.md)
```

### 2. Desarrollo

#### Frontend
```bash
cd frontend
npm install
npm run dev
# Abre http://localhost:5173
```

#### Backend
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run_api.py
```

#### Con Docker
```bash
docker-compose -f docker-compose-demo.yml up --build
```

### 3. Antes de Hacer Commit

```bash
# Frontend - Lint
cd frontend
npm run lint
npm run build  # Verificar que compila

# Backend - Tests
python test_api.py
```

### 4. Commit y Push

```bash
# Commits atómicos con mensajes claros
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/tu-feature-aqui
```

### 5. Pull Request

1. Ir a GitHub
2. Crear PR contra rama `development`
3. Llenar template de PR con:
   - Descripción de cambios
   - Issues relacionados
   - Screenshots si aplica
4. Esperar revisión del equipo

## Convenciones

### Commits

Usar [Conventional Commits](https://www.conventionalcommits.org/es/):

```
feat:    Nueva característica
fix:     Bug fix
docs:    Cambios en documentación
style:   Cambios de formato (no afectan código)
refactor: Refactoring de código
test:    Agregar/modificar tests
chore:   Cambios en dependencias, config, etc
```

Ejemplos:
```
feat: agregar componente LoginForm
fix: corregir validación de imágenes
docs: actualizar README con instrucciones
```

### Ramas

```
feature/nombre-descripcion      # Nuevas features
bugfix/nombre-bug              # Bug fixes
refactor/nombre-cambio         # Refactorings
docs/nombre-documentacion      # Documentación
```

### Código

**Python:**
- PEP 8 compliant
- Type hints donde sea posible
- Docstrings en funciones

**React/JavaScript:**
- ESLint rules (ver eslint.config.js)
- Componentes funcionales con hooks
- Props validadas con PropTypes o TypeScript

## Estructura de PRs

```markdown
## Descripción
Qué cambió y por qué

## Tipo de Cambio
- [ ] New feature
- [ ] Bug fix
- [ ] Breaking change
- [ ] Documentation

## Testing
Cómo se probó:
- [ ] Tests locales pasados
- [ ] Build sin errores
- [ ] Lint pasado

## Screenshots/Demo (si aplica)
[Agregar screenshots]

## Checklist
- [ ] Título de PR descriptivo
- [ ] Commits atómicos
- [ ] Sin archivos .env con secretos
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado
```

## Reporte de Bugs

Si encuentras un bug:

1. Verificar que no esté reportado
2. Crear issue con:
   - Título descriptivo
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Ambiente (OS, versión, etc)

Ejemplo:
```
Título: ImageUpload falla con archivos > 10MB

Pasos:
1. Abrir frontend
2. Click en upload
3. Seleccionar imagen de 15MB

Esperado: Carga la imagen
Actual: Error "File too large"

Ambiente: Windows 11, Chrome 120
```

## Preguntas?

- Abre una **Discussion** en GitHub
- Contacta al equipo en el canal Slack
- Revisa la documentación en `/docs`

¡Gracias por contribuir! 🎉
