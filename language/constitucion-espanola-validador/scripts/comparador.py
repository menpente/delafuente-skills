#!/usr/bin/env python3
"""
Script para generar comparaciones lado a lado entre texto original y reescritura
de artículos constitucionales, con detección automática de cambios.
"""

import difflib
import re
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class Cambio:
    """Representa un cambio detectado entre original y reescritura"""
    tipo: str  # 'adicion', 'eliminacion', 'modificacion'
    original: str
    reescritura: str
    posicion: int
    severidad: str = "menor"  # 'critico', 'moderado', 'menor'
    explicacion: str = ""


def normalizar_texto(texto: str) -> str:
    """Normaliza el texto para comparación"""
    # Eliminar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    # Eliminar espacios antes de puntuación
    texto = re.sub(r'\s+([.,;:])', r'\1', texto)
    return texto.strip()


def tokenizar_juridico(texto: str) -> List[str]:
    """
    Tokeniza el texto preservando unidades jurídicas importantes.
    Mantiene juntas expresiones como 'ley orgánica', 'tres quintos', etc.
    """
    # Patrones de expresiones jurídicas a mantener juntas
    expresiones_juridicas = [
        r'ley orgánica',
        r'ley ordinaria',
        r'decreto[\s-]ley',
        r'decreto legislativo',
        r'mayoría absoluta',
        r'mayoría simple',
        r'tres quintos',
        r'dos tercios',
        r'mitad más uno',
        r'Tribunal Constitucional',
        r'Cortes Generales',
        r'Consejo General del Poder Judicial',
        r'Defensor del Pueblo',
        r'recurso de amparo',
        r'moción de censura',
        r'cuestión de confianza',
        r'sin perjuicio de',
        r'en todo caso',
        r'en su caso',
        r'salvo que',
    ]
    
    # Crear marcadores temporales para expresiones jurídicas
    texto_marcado = texto
    marcadores = {}
    for i, expresion in enumerate(expresiones_juridicas):
        patron = re.compile(expresion, re.IGNORECASE)
        for match in patron.finditer(texto_marcado):
            marcador = f"__EXPR_{i}_{match.start()}__"
            marcadores[marcador] = match.group()
            texto_marcado = texto_marcado[:match.start()] + marcador + texto_marcado[match.end():]
    
    # Tokenizar por palabras
    tokens = texto_marcado.split()
    
    # Restaurar expresiones jurídicas
    tokens_restaurados = []
    for token in tokens:
        if token in marcadores:
            tokens_restaurados.append(marcadores[token])
        else:
            tokens_restaurados.append(token)
    
    return tokens_restaurados


def detectar_cambios_semanticos(original: str, reescritura: str) -> List[Cambio]:
    """
    Detecta cambios semánticos importantes entre original y reescritura.
    Usa difflib para comparación detallada.
    """
    cambios = []
    
    # Normalizar textos
    orig_norm = normalizar_texto(original)
    reesc_norm = normalizar_texto(reescritura)
    
    # Tokenizar
    tokens_orig = tokenizar_juridico(orig_norm)
    tokens_reesc = tokenizar_juridico(reescritura)
    
    # Usar SequenceMatcher para detectar diferencias
    matcher = difflib.SequenceMatcher(None, tokens_orig, tokens_reesc)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'delete':
            cambio = Cambio(
                tipo='eliminacion',
                original=' '.join(tokens_orig[i1:i2]),
                reescritura='',
                posicion=i1
            )
            cambios.append(cambio)
        
        elif tag == 'insert':
            cambio = Cambio(
                tipo='adicion',
                original='',
                reescritura=' '.join(tokens_reesc[j1:j2]),
                posicion=j1
            )
            cambios.append(cambio)
        
        elif tag == 'replace':
            cambio = Cambio(
                tipo='modificacion',
                original=' '.join(tokens_orig[i1:i2]),
                reescritura=' '.join(tokens_reesc[j1:j2]),
                posicion=i1
            )
            cambios.append(cambio)
    
    return cambios


def clasificar_severidad(cambio: Cambio) -> str:
    """
    Clasifica la severidad de un cambio basándose en patrones conocidos.
    Esta es una clasificación automática básica; el análisis jurídico
    final debe hacerse manualmente.
    """
    original_lower = cambio.original.lower()
    reescritura_lower = cambio.reescritura.lower()
    
    # Patrones críticos
    patrones_criticos = [
        (r'ley orgánica', r'ley'),  # Eliminación de "orgánica"
        (r'deberá', r'podrá'),  # Cambio de obligación a facultad
        (r'podrá', r'deberá'),  # Cambio de facultad a obligación
        (r'españoles', r'todos'),  # Cambio de titularidad
        (r'todos', r'españoles'),  # Cambio de titularidad
        (r'tres quintos', r'mayoría'),  # Cambio de mayoría cualificada
        (r'dos tercios', r'mayoría'),  # Cambio de mayoría cualificada
        (r'mayoría absoluta', r'mayoría'),  # Cambio de tipo de mayoría
    ]
    
    for patron_orig, patron_reesc in patrones_criticos:
        if re.search(patron_orig, original_lower) and re.search(patron_reesc, reescritura_lower):
            return 'critico'
        if re.search(patron_reesc, original_lower) and re.search(patron_orig, reescritura_lower):
            return 'critico'
    
    # Patrones moderados
    patrones_moderados = [
        r'sin perjuicio de',
        r'en todo caso',
        r'salvo que',
        r'en su caso',
        r'los términos que establezca la ley',
    ]
    
    for patron in patrones_moderados:
        if re.search(patron, original_lower) and not re.search(patron, reescritura_lower):
            return 'moderado'
    
    # Por defecto
    return 'menor'


def generar_comparacion_html(articulo: str, original: str, reescritura: str, 
                             cambios: List[Cambio]) -> str:
    """
    Genera una tabla HTML de comparación lado a lado con resaltado de cambios.
    """
    html = f"""
<div class="comparacion-articulo">
    <h3>Artículo {articulo}</h3>
    <table class="comparacion">
        <thead>
            <tr>
                <th>Texto Original</th>
                <th>Reescritura en Lenguaje Claro</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="original">{original}</td>
                <td class="reescritura">{reescritura}</td>
            </tr>
        </tbody>
    </table>
    
    <div class="cambios-detectados">
        <h4>Cambios Detectados</h4>
"""
    
    if not cambios:
        html += "<p class='sin-cambios'>No se detectaron cambios significativos.</p>"
    else:
        for i, cambio in enumerate(cambios, 1):
            severidad_class = cambio.severidad.lower()
            html += f"""
        <div class="cambio {severidad_class}">
            <span class="severidad-badge">{cambio.severidad.upper()}</span>
            <strong>Cambio {i} ({cambio.tipo}):</strong><br>
"""
            if cambio.original:
                html += f"            <span class='original-text'>Original: \"{cambio.original}\"</span><br>\n"
            if cambio.reescritura:
                html += f"            <span class='reescrito-text'>Reescritura: \"{cambio.reescritura}\"</span><br>\n"
            if cambio.explicacion:
                html += f"            <p class='explicacion'>{cambio.explicacion}</p>\n"
            html += "        </div>\n"
    
    html += """
    </div>
</div>

<style>
    .comparacion-articulo {
        margin: 20px 0;
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 5px;
    }
    
    .comparacion {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }
    
    .comparacion th {
        background-color: #f0f0f0;
        padding: 10px;
        text-align: left;
        border: 1px solid #ddd;
    }
    
    .comparacion td {
        padding: 10px;
        border: 1px solid #ddd;
        vertical-align: top;
    }
    
    .original {
        background-color: #fff8dc;
    }
    
    .reescritura {
        background-color: #e8f4f8;
    }
    
    .cambios-detectados {
        margin-top: 15px;
    }
    
    .cambio {
        margin: 10px 0;
        padding: 10px;
        border-left: 4px solid #ccc;
        background-color: #f9f9f9;
    }
    
    .cambio.critico {
        border-left-color: #d32f2f;
        background-color: #ffebee;
    }
    
    .cambio.moderado {
        border-left-color: #f57c00;
        background-color: #fff3e0;
    }
    
    .cambio.menor {
        border-left-color: #1976d2;
        background-color: #e3f2fd;
    }
    
    .severidad-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 3px;
        font-size: 0.8em;
        font-weight: bold;
        margin-right: 5px;
    }
    
    .critico .severidad-badge {
        background-color: #d32f2f;
        color: white;
    }
    
    .moderado .severidad-badge {
        background-color: #f57c00;
        color: white;
    }
    
    .menor .severidad-badge {
        background-color: #1976d2;
        color: white;
    }
    
    .original-text {
        color: #c62828;
    }
    
    .reescrito-text {
        color: #0277bd;
    }
    
    .sin-cambios {
        color: #2e7d32;
        font-style: italic;
    }
</style>
"""
    
    return html


def analizar_articulo(articulo: str, original: str, reescritura: str) -> Dict:
    """
    Analiza un artículo completo y retorna un diccionario con los resultados.
    """
    cambios = detectar_cambios_semanticos(original, reescritura)
    
    # Clasificar severidad de cada cambio
    for cambio in cambios:
        cambio.severidad = clasificar_severidad(cambio)
    
    # Ordenar por severidad
    orden_severidad = {'critico': 0, 'moderado': 1, 'menor': 2}
    cambios_ordenados = sorted(cambios, key=lambda c: orden_severidad[c.severidad])
    
    return {
        'articulo': articulo,
        'original': original,
        'reescritura': reescritura,
        'cambios': cambios_ordenados,
        'tiene_cambios_criticos': any(c.severidad == 'critico' for c in cambios_ordenados),
        'tiene_cambios_moderados': any(c.severidad == 'moderado' for c in cambios_ordenados),
        'total_cambios': len(cambios_ordenados)
    }


if __name__ == '__main__':
    # Ejemplo de uso
    ejemplo_original = """Los españoles son iguales ante la ley, sin que pueda 
    prevalecer discriminación alguna por razón de nacimiento, raza, sexo, religión, 
    opinión o cualquier otra condición o circunstancia personal o social."""
    
    ejemplo_reescritura = """Todas las personas son iguales ante la ley. 
    No puede haber discriminación por ningún motivo."""
    
    resultado = analizar_articulo("14", ejemplo_original, ejemplo_reescritura)
    
    print(f"Artículo {resultado['articulo']}")
    print(f"Total de cambios: {resultado['total_cambios']}")
    print(f"Cambios críticos: {resultado['tiene_cambios_criticos']}")
    print(f"Cambios moderados: {resultado['tiene_cambios_moderados']}")
    
    html = generar_comparacion_html(
        resultado['articulo'],
        resultado['original'],
        resultado['reescritura'],
        resultado['cambios']
    )
    
    print("\n" + html)
