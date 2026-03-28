---
name: constitucion-espanola-validador
description: Validación jurídica rigurosa de reescrituras de la Constitución Española en lenguaje claro. Detecta cambios en derechos fundamentales, procedimientos constitucionales, jerarquías normativas y competencias. Genera comparaciones lado a lado con clasificación de problemas (críticos, moderados, menores). Use cuando el usuario necesite validar que una reescritura en lenguaje sencillo de artículos constitucionales preserva el significado jurídico original sin alterar derechos, procedimientos, mayorías, competencias o términos técnicos esenciales de la Constitución Española de 1978.
---

# Validador de Reescrituras de la Constitución Española

Esta skill permite validar si reescrituras en lenguaje claro de la Constitución Española mantienen la fidelidad jurídica al texto original.

## Workflow de Validación

### 1. Recepción de Textos

Solicitar al usuario:
- **Artículo(s) a validar**: Número de artículo constitucional
- **Texto original**: De la Constitución Española de 1978
- **Texto reescrito**: Versión en lenguaje claro a validar

Si el usuario solo proporciona el artículo reescrito, buscar el texto original del artículo correspondiente de la Constitución.

### 2. Análisis Automatizado Inicial

Ejecutar el script de comparación para detectar cambios:

```bash
python3 scripts/comparador.py
```

El script detecta automáticamente:
- Eliminaciones de texto
- Adiciones de texto
- Modificaciones léxicas
- Clasificación preliminar de severidad

### 3. Validación Jurídica Profunda

**OBLIGATORIO**: Leer los criterios jurídicos de referencia:

```bash
view references/criterios_juridicos.md
```

Aplicar los siguientes análisis en orden:

#### A. Validación de Derechos Fundamentales (si aplica)

Si el artículo está en el Título I (arts. 10-55):

1. **Verificar titularidad**:
   - ¿Quién tiene el derecho? (todos, españoles, extranjeros)
   - ¿Se ha cambiado la titularidad?

2. **Comprobar núcleo esencial**:
   - ¿Se preserva el contenido del derecho?
   - ¿Se mantienen las limitaciones expresas?

3. **Garantías jurisdiccionales**:
   - Para arts. 14-29: ¿Se mantiene la posibilidad de amparo constitucional?
   - ¿Se preserva la reserva de ley orgánica?

#### B. Validación de Procedimientos (si aplica)

Si el artículo establece un procedimiento constitucional:

1. **Secuencia de pasos**:
   - ¿Se mantiene el orden de actuaciones?
   - ¿Se han fusionado pasos que deben ser secuenciales?

2. **Mayorías y quórums**:
   - Mayoría absoluta ≠ mayoría simple ≠ 3/5 ≠ 2/3
   - ¿Se especifica correctamente el tipo de mayoría?

3. **Actores del procedimiento**:
   - ¿Quién inicia? ¿Quién vota? ¿Quién puede vetar?
   - ¿Se han omitido actores necesarios?

4. **Plazos**:
   - ¿Se preservan los períodos temporales?

#### C. Validación de Jerarquías Normativas

1. **Tipos de leyes**:
   - "Ley orgánica" ≠ "ley" ≠ "decreto-ley"
   - ¿Se ha simplificado inadecuadamente?

2. **Competencias**:
   - Exclusivas del Estado vs. autonómicas vs. concurrentes
   - ¿Se mantienen las distinciones?

#### D. Validación Lingüística-Jurídica

Verificar fórmulas con significado jurídico preciso:

- **"Podrá"** → facultad discrecional
- **"Deberá"** → obligación
- **"Sin perjuicio de"** → salvaguarda
- **"En todo caso"** → obligación mínima
- **"Los términos que establezca la ley"** → desarrollo legislativo

¿Se han sustituido o eliminado estas expresiones?

### 4. Clasificación de Problemas

Clasificar cada problema detectado:

**CRÍTICO** (impide el uso de la reescritura):
- Altera derechos fundamentales o su titularidad
- Cambia tipos de mayorías o procedimientos
- Modifica competencias o jerarquías normativas
- Invierte obligaciones/facultades (podrá ↔ deberá)
- Omite requisitos esenciales

**MODERADO** (requiere corrección antes de uso):
- Ambigüedad que permite múltiples interpretaciones jurídicas
- Omisión de matices importantes ("sin perjuicio de", "en su caso")
- Simplificación excesiva de condiciones

**MENOR** (mejora recomendada):
- Imprecisión terminológica sin impacto sustantivo
- Estilo mejorable
- Redundancia innecesaria

### 5. Generación del Reporte

Crear un reporte en formato HTML usando la plantilla:

```python
# Cargar template
with open('assets/template_reporte.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Generar contenido para cada artículo
# Insertar en el contenedor de artículos
```

Estructura del reporte:

1. **Resumen ejecutivo**:
   - Total de artículos analizados
   - Número de problemas críticos/moderados/menores
   - Conclusión sobre viabilidad de uso

2. **Por cada artículo**:
   - Comparación lado a lado (original vs reescritura)
   - Lista de cambios detectados con severidad
   - Explicación jurídica de cada problema
   - Recomendaciones de corrección

3. **Conclusión general**:
   - ¿Es utilizable la reescritura?
   - ¿Qué correcciones son imprescindibles?

### 6. Presentación de Resultados

Presentar el reporte HTML al usuario:

```python
# Guardar el reporte
ruta_reporte = '/mnt/user-data/outputs/validacion_constitucion.html'
# Usar present_files para compartir
```

Acompañar con un resumen textual que destaque:
- Problemas críticos que impiden el uso
- Sugerencias de corrección específicas
- Artículos que están correctamente reescritos

## Ejemplos de Uso

### Ejemplo 1: Artículo con Problema Crítico

**Original (Art. 116.1)**: "Una ley orgánica regulará los estados de alarma, de excepción y de sitio, y las competencias y limitaciones correspondientes."

**Reescritura Incorrecta**: "La ley regulará los estados de emergencia."

**Problemas Detectados**:
- 🔴 **CRÍTICO**: Omisión de "orgánica" (cambia tipo de ley y mayoría requerida)
- 🔴 **CRÍTICO**: "Estados de emergencia" no es término constitucional (debe ser: alarma, excepción, sitio)
- 🔴 **CRÍTICO**: Omite "competencias y limitaciones"

**Recomendación**: Reescribir como: "Una ley orgánica regulará los tres estados excepcionales (alarma, excepción y sitio), estableciendo qué competencias tiene el Estado en cada uno y qué límites existen."

### Ejemplo 2: Artículo Correcto

**Original (Art. 14)**: "Los españoles son iguales ante la ley, sin que pueda prevalecer discriminación alguna por razón de nacimiento, raza, sexo, religión, opinión o cualquier otra condición o circunstancia personal o social."

**Reescritura Correcta**: "Todas las personas españolas son iguales ante la ley. No puede haber discriminación por motivos de nacimiento, raza, sexo, religión, opinión ni por ninguna otra condición personal o social."

**Análisis**:
- ✅ Mantiene la titularidad ("españoles")
- ✅ Preserva el derecho a la igualdad
- ✅ Conserva toda la lista de motivos prohibidos
- ✅ Lenguaje más claro sin pérdida de contenido

## Criterios Críticos de Validación

### No Simplificar Sin Equivalente

**Términos que NUNCA deben simplificarse**:
- Ley orgánica → "ley" ❌
- Tres quintos → "mayoría" ❌
- Mayoría absoluta → "mayoría" ❌
- Decreto-ley → "decreto" ❌
- Tribunal Constitucional → "corte" ❌
- Recurso de amparo → "recurso" ❌

### Preservar Todas las Condiciones

Expresiones condicionales y limitativas NO pueden omitirse:
- "Sin perjuicio de..."
- "En todo caso..."
- "Salvo que..."
- "En los términos que establezca la ley..."
- "Cuando..."
- "Si..."

### Mantener Actores y Procedimientos

En artículos procedimentales:
- Identificar TODOS los actores (Rey, Congreso, Senado, Presidente, etc.)
- Preservar la SECUENCIA de pasos
- Especificar MAYORÍAS exactas
- Mantener PLAZOS temporales

## Recursos Adicionales

- **Criterios jurídicos completos**: `references/criterios_juridicos.md`
- **Script de comparación**: `scripts/comparador.py`
- **Plantilla de reporte**: `assets/template_reporte.html`

## Limitaciones

Esta skill proporciona validación técnica pero NO sustituye la revisión por juristas constitucionalistas. Los problemas críticos detectados son indicativos pero la validación final debe ser realizada por profesionales del derecho constitucional.

## Notas para Usuarios

- La skill está optimizada para la Constitución Española de 1978
- Puede validar desde un artículo individual hasta títulos completos
- Genera reportes interactivos en HTML con comparaciones lado a lado
- Clasifica automáticamente la severidad de cada problema detectado
