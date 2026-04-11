#!/usr/bin/env python3
"""
Script to transform Dis_Exp_idoneidad_modelo.html into SPA format
matching the style of Diseno_Exp_Semana_I.html
"""
import re

# Read the original file
with open('Dis_Exp_idoneidad_modelo.html', 'r', encoding='utf-8') as f:
    original = f.read()

# Extract content blocks using regex
def extract_between(html, start_marker, end_marker):
    """Extract content between two markers."""
    pattern = re.compile(re.escape(start_marker) + r'(.*?)' + re.escape(end_marker), re.DOTALL)
    match = pattern.search(html)
    return match.group(1) if match else ''

# Extract each article's inner content
def extract_article(html, article_id):
    pattern = re.compile(r'<article\s+id="' + article_id + r'">(.*?)</article>', re.DOTALL)
    match = pattern.search(html)
    return match.group(1).strip() if match else ''

def extract_section(html, section_id, tag='section'):
    pattern = re.compile(r'<' + tag + r'\s+id="' + section_id + r'"[^>]*>(.*?)</' + tag + r'>', re.DOTALL)
    match = pattern.search(html)
    return match.group(1).strip() if match else ''

# Extract the summary box
def extract_summary(html):
    pattern = re.compile(r'<div class="summary-box">(.*?)</div>\s*(?=\s*<!--)', re.DOTALL)
    match = pattern.search(html)
    return match.group(0).strip() if match else ''

clase1 = extract_article(original, 'clase1')
clase2 = extract_article(original, 'clase2')
clase3 = extract_article(original, 'clase3')
clase4 = extract_article(original, 'clase4')
ejercicios = extract_section(original, 'ejercicios')
referencias = extract_section(original, 'referencias')
summary_box = extract_summary(original)

# Remove the <h2> from each article (we'll add our own header)
def remove_first_h2(content):
    return re.sub(r'<h2>.*?</h2>\s*', '', content, count=1)

clase1 = remove_first_h2(clase1)
clase2 = remove_first_h2(clase2)
clase3 = remove_first_h2(clase3)
clase4 = remove_first_h2(clase4)
ejercicios_content = re.sub(r'<h2>.*?</h2>\s*', '', ejercicios, count=1)

# Remap CSS classes to new style
def remap_classes(content):
    """Remap old CSS classes to new SPA-style classes."""
    # definition-box -> concepto-clave
    content = content.replace('class="definition-box"', 'class="concepto-clave"')
    content = content.replace('class="term"', 'style="color:#3D008D;font-weight:600;margin-bottom:0.5rem;"')
    # theorem-box -> ejercicio style
    content = content.replace('class="theorem-box"', 'class="ejercicio"')
    content = content.replace('<p class="title">', '<h4 style="color:#3D008D;margin-top:0;">')
    content = content.replace('</p>\n                    <p>', '</h4>\n                    <p>')
    # formula -> formula-box
    content = content.replace('class="formula"', 'class="formula-box"')
    # note-box -> aside
    content = content.replace('<div class="note-box">', '<aside>')
    content = content.replace('</div>\n            </section>', '</aside>\n            </section>')
    # warning-box -> aside with warning style
    content = content.replace('<div class="warning-box">', '<aside style="border-left-color:#ED1E79;background:linear-gradient(135deg, rgba(237,30,121,0.1) 0%, rgba(237,30,121,0.05) 100%);">')
    # example-box stays similar
    content = content.replace('class="example-box"', 'class="concepto-clave" style="border-left-color:#FDB913;"')
    content = content.replace('class="example-context"', 'class="nota"')
    # interpretation-box -> nota
    content = content.replace('class="interpretation-box"', 'class="nota"')
    # diagram-box
    content = content.replace('class="diagram-box"', 'class="concepto-clave"')
    content = content.replace('class="diagram-step"', 'style="display:flex;align-items:center;margin-bottom:1rem;"')
    content = content.replace('class="diagram-number"', 'style="background:#3D008D;color:white;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:600;margin-right:1rem;flex-shrink:0;"')
    content = content.replace('class="diagram-content"', 'style="flex:1;"')
    content = content.replace('class="diagram-arrow"', 'style="text-align:center;color:#3D008D;font-size:1.5rem;margin:0.5rem 0;"')
    # formula-block
    content = content.replace('class="formula-block"', 'class="formula-box"')
    # notation-list
    content = content.replace('class="notation-list"', 'style="background:#F8FAFC;padding:1.5rem;border-radius:12px;margin:1rem 0;"')
    # exercises
    content = content.replace('class="exercise"', 'class="ejercicio"')
    content = content.replace('class="exercise-number"', 'style="background:#ED1E79;color:white;padding:2px 10px;border-radius:4px;font-weight:600;font-size:0.85rem;"')
    content = content.replace('class="solution-hint"', 'class="nota"')
    # table-caption
    content = content.replace('class="table-caption"', 'style="text-align:center;font-style:italic;color:#64748B;font-size:0.9rem;margin-top:0.5rem;"')
    # code-title stays
    # summary-box remap
    content = content.replace('class="summary-box"', 'class="concepto-clave" style="background:linear-gradient(135deg,#001A4D 0%,#3D008D 100%);color:white;border:none;"')
    # Fix remaining note-box closings that weren't caught
    # references
    content = content.replace('class="references-list"', 'style="list-style:none;counter-reset:ref-counter;"')
    content = content.replace('class="author"', 'style="font-weight:600;"')
    content = content.replace('class="title"', 'style="font-style:italic;"')
    content = content.replace('class="publisher"', 'style="color:#64748B;"')
    content = content.replace('class="year"', 'style="color:#64748B;"')
    return content

clase1 = remap_classes(clase1)
clase2 = remap_classes(clase2)
clase3 = remap_classes(clase3)
clase4 = remap_classes(clase4)
ejercicios_content = remap_classes(ejercicios_content)
referencias = remap_classes(referencias)
summary_box = remap_classes(summary_box)

def make_module_header(num, title, objective):
    return f'''<div class="animate-fade-in">
            <div class="border-b border-gray-100 pb-6 mb-6">
                <div class="flex items-center space-x-2 text-sm text-secondary font-semibold mb-2 uppercase tracking-wide">
                    <span>Módulo {num}</span>
                </div>
                <h2 class="text-3xl font-bold text-gray-900 mb-4" style="border:none; padding:0;">{title}</h2>
                <div class="bg-gray-50 rounded-lg p-4 border border-gray-200 flex items-start gap-3">
                    <span class="text-xl">🎯</span>
                    <div>
                        <h3 class="font-bold text-gray-800 text-sm" style="margin:0;">Objetivo</h3>
                        <p class="text-gray-600 text-sm" style="margin:0;">{objective}</p>
                    </div>
                </div>
            </div>'''

# Build the complete HTML
HEAD = '''<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description"
        content="Material de estudio autónomo sobre diagnosis y validación del modelo en diseño de experimentos">
    <meta name="author" content="Z.ai">
    <title>Diagnosis y Validación del Modelo en Diseño de Experimentos</title>

    <!-- Preconnect for performance -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <!-- External Resources -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&display=swap"
        rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">

    <!-- KaTeX for LaTeX rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>

    <!-- Tailwind Configuration -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Montserrat', 'Helvetica Neue', 'Helvetica', 'Arial', 'sans-serif'],
                    },
                    colors: {
                        primary: '#3D008D',
                        secondary: '#ED1E79',
                        navy: '#001A4D',
                        gold: '#FDB913',
                        bg: '#F8FAFC',
                        surface: '#FFFFFF',
                    }
                }
            }
        }
    </script>

    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background-color: #F8FAFC;
            color: #1E293B;
            scroll-behavior: smooth;
        }

        code,
        pre {
            font-family: 'Fira Code', monospace;
        }

        /* USTA Gradient Background */
        .usta-gradient {
            background: linear-gradient(140deg, #3D008D 0%, #ED1E79 100%);
        }

        /* USTA Navy Header */
        .usta-header {
            background: linear-gradient(180deg, #001A4D 0%, #002868 100%);
        }

        /* USTA Card Style */
        .usta-card {
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }

        .usta-card:hover {
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
            transform: translateY(-4px);
        }

        /* Tip box USTA style */
        .tip-box {
            background: linear-gradient(135deg, rgba(61, 0, 141, 0.08) 0%, rgba(237, 30, 121, 0.08) 100%);
            border: 1px solid rgba(61, 0, 141, 0.2);
        }

        /* Step connector for pipeline */
        .step-connector::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, #3D008D, #ED1E79);
            opacity: 0.3;
            z-index: -1;
        }

        .step-connector:last-child::after {
            display: none;
        }

        /* ===== SIDEBAR DARK STYLE ===== */
        #sidebar-panel {
            background: linear-gradient(180deg, #001A4D 0%, #002868 100%);
            flex-shrink: 0;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            width: 16rem;
            min-width: 16rem;
            transition: width 0.3s ease, min-width 0.3s ease, opacity 0.25s ease;
            z-index: 40;
        }

        #sidebar-panel.collapsed {
            width: 0;
            min-width: 0;
            opacity: 0;
            overflow: hidden;
        }

        .sidebar-brand {
            padding: 1.5rem;
            padding-top: 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .sidebar-brand h2 {
            color: white;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 0;
            padding: 0;
            border: none;
        }

        .sidebar-brand p {
            font-size: 0.7rem;
            color: rgba(255, 255, 255, 0.5);
            margin-top: 0.25rem;
            margin-bottom: 0;
            text-align: left;
        }

        .sidebar-nav {
            padding: 1rem;
        }

        .sidebar-nav-item {
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            padding: 0.65rem 0.75rem;
            font-size: 0.8rem;
            font-weight: 500;
            border-radius: 0.5rem;
            text-align: left;
            margin-bottom: 0.25rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            color: rgba(255, 255, 255, 0.6);
            background: transparent;
        }

        .sidebar-nav-item:hover {
            color: white;
            background: rgba(255, 255, 255, 0.1);
        }

        .sidebar-nav-item.active {
            color: white;
            background: linear-gradient(140deg, #3D008D 0%, #ED1E79 100%);
            box-shadow: 0 4px 12px rgba(61, 0, 141, 0.3);
        }

        .sidebar-nav-item .check-mark {
            color: #10B981;
            flex-shrink: 0;
        }

        /* Floating sidebar toggle button */
        .sidebar-toggle-btn {
            position: fixed;
            top: 1rem;
            left: 1rem;
            z-index: 50;
            width: 2.5rem;
            height: 2.5rem;
            background: linear-gradient(140deg, #3D008D 0%, #ED1E79 100%);
            color: white;
            border: none;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(61, 0, 141, 0.4);
            transition: all 0.2s ease;
        }

        .sidebar-toggle-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 18px rgba(61, 0, 141, 0.5);
        }

        /* Layout adjustment */
        .main-layout {
            display: flex;
            flex-grow: 1;
            width: 100%;
        }

        /* Scroll to top button */
        .scroll-to-top {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 3.5rem;
            height: 3.5rem;
            background: linear-gradient(140deg, #3D008D 0%, #ED1E79 100%);
            color: white;
            border-radius: 50%;
            display: none;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 6px 15px rgba(61, 0, 141, 0.4);
            transition: all 0.3s ease;
            z-index: 50;
            border: none;
        }

        .scroll-to-top.visible {
            display: flex;
        }

        .scroll-to-top:hover {
            background: linear-gradient(140deg, #4A00A8 0%, #FF2D8A 100%);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(61, 0, 141, 0.5);
        }

        /* Fade-in animation */
        .animate-fade-in {
            animation: fadeIn 0.4s ease-out forwards;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #3D008D, #ED1E79);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #4A00A8, #FF2D8A);
        }

        /* Code scrollbar */
        .code-scroll::-webkit-scrollbar {
            height: 8px;
        }

        .code-scroll::-webkit-scrollbar-track {
            background: #2d2d2d;
        }

        .code-scroll::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #3D008D, #ED1E79);
            border-radius: 4px;
        }

        /* Focus styles for accessibility */
        button:focus-visible,
        a:focus-visible {
            outline: 2px solid #ED1E79;
            outline-offset: 2px;
        }

        /* Syntax highlighting */
        .syntax-kwd {
            color: #c678dd;
            font-weight: bold;
        }

        .syntax-cls {
            color: #e5c07b;
        }

        .syntax-str {
            color: #98c379;
        }

        .syntax-com {
            color: #5c6370;
            font-style: italic;
        }

        .syntax-func {
            color: #61afef;
        }

        .syntax-self {
            color: #e06c75;
            font-style: italic;
        }

        .syntax-num {
            color: #d19a66;
        }

        /* Content Styling */
        .module-content h2 {
            color: #3D008D;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1.25rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid #ED1E79;
        }

        .module-content h3 {
            color: #3D008D;
            font-size: 1.25rem;
            font-weight: 600;
            margin: 1.75rem 0 1rem 0;
        }

        .module-content h4 {
            color: #ED1E79;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 1.5rem 0 0.75rem 0;
        }

        .module-content p {
            margin-bottom: 1rem;
            text-align: justify;
            line-height: 1.8;
        }

        .module-content ul,
        .module-content ol {
            margin-left: 1.5rem;
            margin-bottom: 1rem;
        }

        .module-content li {
            margin-bottom: 0.5rem;
            line-height: 1.7;
        }

        .module-content aside {
            background: linear-gradient(135deg, rgba(253, 185, 19, 0.1) 0%, rgba(253, 185, 19, 0.05) 100%);
            border-left: 4px solid #FDB913;
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin: 1.5rem 0;
        }

        .module-content aside strong {
            color: #B8860B;
        }

        .module-content .formula-box {
            background: linear-gradient(135deg, rgba(61, 0, 141, 0.03) 0%, rgba(237, 30, 121, 0.03) 100%);
            padding: 1.25rem;
            border-radius: 12px;
            margin: 1rem 0;
            border: 1px solid rgba(61, 0, 141, 0.15);
            overflow-x: auto;
        }

        .module-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95rem;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }

        .module-content th,
        .module-content td {
            padding: 1rem 1.25rem;
            text-align: center;
        }

        .module-content th {
            background: linear-gradient(140deg, #3D008D 0%, #ED1E79 100%);
            color: white;
            font-weight: 600;
        }

        .module-content tr:nth-child(even) {
            background: rgba(61, 0, 141, 0.03);
        }

        .module-content tr:hover {
            background: rgba(61, 0, 141, 0.08);
        }

        .module-content pre {
            background: #1e1e2e;
            color: #cdd6f4;
            padding: 1.25rem;
            border-radius: 12px;
            overflow-x: auto;
            margin: 1rem 0;
            border: 1px solid rgba(61, 0, 141, 0.2);
        }

        .module-content pre code {
            font-family: 'Fira Code', monospace;
            font-size: 0.875rem;
            line-height: 1.6;
            color: #cdd6f4;
        }

        .module-content code {
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            color: #3D008D;
            background: rgba(61, 0, 141, 0.08);
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
        }

        .module-content pre code {
            background: transparent;
            padding: 0;
        }

        .module-content .output {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
            padding: 1rem 1.25rem;
            border-radius: 10px;
            border-left: 4px solid #10B981;
            margin: 1rem 0;
            font-family: 'Fira Code', monospace;
            font-size: 0.85rem;
            white-space: pre-wrap;
        }

        /* Tooltip Styles */
        .tooltip-term {
            position: relative;
            border-bottom: 2px dotted #ED1E79;
            cursor: help;
            font-weight: 600;
            color: #3D008D;
        }

        .tooltip-term:hover::after {
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #3D008D 0%, #2D0066 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: 400;
            width: 280px;
            text-align: left;
            line-height: 1.5;
            box-shadow: 0 10px 25px rgba(61, 0, 141, 0.3);
            z-index: 1000;
            margin-bottom: 8px;
        }

        .tooltip-term:hover::before {
            content: '';
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            border: 8px solid transparent;
            border-top-color: #3D008D;
            margin-bottom: -8px;
            z-index: 1001;
        }

        .module-content .ejercicio {
            background: linear-gradient(135deg, rgba(61, 0, 141, 0.08) 0%, rgba(237, 30, 121, 0.05) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #ED1E79;
            margin: 1.5rem 0;
        }

        .module-content .ejercicio h4 {
            color: #3D008D;
            margin-top: 0;
        }

        .module-content .resumen {
            background: linear-gradient(135deg, rgba(61, 0, 141, 0.06) 0%, rgba(237, 30, 121, 0.04) 100%);
            padding: 1.25rem;
            border-radius: 12px;
            border-left: 4px solid #3D008D;
            margin-bottom: 1.5rem;
        }

        .module-content .resumen h4 {
            margin-top: 0;
            color: #3D008D;
        }

        .module-content strong {
            color: #3D008D;
        }

        .module-content em {
            color: #ED1E79;
        }

        /* KaTeX display */
        .katex-display {
            margin: 1.25em 0;
            overflow-x: auto;
        }

        /* Concepto clave box */
        .concepto-clave {
            background: linear-gradient(135deg, rgba(61, 0, 141, 0.06) 0%, rgba(237, 30, 121, 0.04) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #3D008D;
            margin: 1.5rem 0;
        }

        .concepto-clave h4 {
            color: #3D008D;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Nota box */
        .nota {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(16, 185, 129, 0.04) 100%);
            padding: 1.25rem;
            border-radius: 12px;
            border-left: 4px solid #10B981;
            margin: 1.5rem 0;
        }

        .nota h4 {
            color: #059669;
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Code title bar */
        .code-title {
            background: #001A4D;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 12px 12px 0 0;
            font-size: 0.85rem;
            font-weight: 500;
            margin-bottom: 0;
        }

        .code-title + pre {
            border-radius: 0 0 12px 12px;
            margin-top: 0;
        }

        /* Syntax colors kept from original */
        .kwd { color: #c678dd; font-weight: bold; }
        .cls { color: #e5c07b; }
        .str { color: #98c379; }
        .com { color: #5c6370; font-style: italic; }
        .func { color: #61afef; }
        .num { color: #d19a66; }
        .op { color: #56b6c2; }
        .var { color: #e06c75; }

        /* Formula number */
        .formula-number {
            float: right;
            color: #64748B;
            font-size: 0.9rem;
        }
    </style>
</head>
'''

BODY_START = '''
<body class="bg-gray-50 text-gray-800 min-h-screen flex flex-col">

    <!-- Floating Sidebar Toggle Button -->
    <button class="sidebar-toggle-btn" id="sidebarToggleBtn" title="Mostrar/Ocultar menú" aria-label="Toggle sidebar">
        <i class="fas fa-bars text-sm" id="sidebarToggleIcon"></i>
    </button>

    <div class="main-layout">

        <!-- Sidebar Navigation -->
        <div id="sidebar-panel">
            <div class="sidebar-brand">
                <h2><i class="fas fa-microscope text-secondary"></i> Diagnosis <span style="color: #FDB913;">ANOVA</span></h2>
                <p>Diseño de Experimentos • Idoneidad del Modelo • USTA</p>
            </div>
            <nav class="sidebar-nav" id="module-nav">
                <!-- Nav items injected via JS -->
            </nav>
        </div>

        <!-- Main Content Area -->
        <div class="flex-grow flex flex-col" style="min-width:0;">
            <main class="flex-grow bg-white rounded-tl-xl shadow-sm border border-gray-200 overflow-hidden">
                <div id="content-area" class="p-6 md:p-10 module-content">
                    <!-- Content injected via JS -->
                </div>
            </main>
        </div>
    </div>

    <!-- Footer -->
    <footer class="usta-header mt-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <i class="fas fa-book-open"></i> Referencias Bibliográficas
            </h3>
            <ul class="space-y-3 text-white/90 text-sm">
                <li class="flex items-start gap-2">
                    <i class="fas fa-bookmark text-secondary mt-1"></i>
                    <span>Montgomery, D. C. (2017). <em class="text-gold">Design and Analysis of Experiments</em> (9th ed.). Wiley.</span>
                </li>
                <li class="flex items-start gap-2">
                    <i class="fas fa-bookmark text-secondary mt-1"></i>
                    <span>Box, G.E.P. & Cox, D.R. (1964). An analysis of transformations. <em class="text-gold">Journal of the Royal Statistical Society, Series B</em>, 26(2), 211-252.</span>
                </li>
                <li class="flex items-start gap-2">
                    <i class="fas fa-bookmark text-secondary mt-1"></i>
                    <span>Scheffé, H. (1959). <em class="text-gold">The Analysis of Variance</em>. Wiley.</span>
                </li>
                <li class="flex items-start gap-2">
                    <i class="fas fa-bookmark text-secondary mt-1"></i>
                    <span>Bartlett, M.S. (1937). Properties of sufficiency and statistical tests. <em class="text-gold">Proceedings of the Royal Society of London, Series A</em>, 160, 268-282.</span>
                </li>
                <li class="flex items-start gap-2">
                    <i class="fas fa-bookmark text-secondary mt-1"></i>
                    <span>Hartley, H.O. (1950). The maximum F-ratio as a short-cut test for heterogeneity of variance. <em class="text-gold">Biometrika</em>, 37, 308-312.</span>
                </li>
                <li class="flex items-start gap-2">
                    <i class="fas fa-bookmark text-secondary mt-1"></i>
                    <span>Cochran, W.G. (1941). The distribution of the largest of a set of estimated variances as a fraction of their total. <em class="text-gold">Annals of Eugenics</em>, 11, 47-52.</span>
                </li>
            </ul>
            <div class="mt-6 pt-6 border-t border-white/20 text-center">
                <p class="text-white font-medium">Material de Estudio — <span class="text-gold">USTA</span></p>
                <p class="text-xs mt-1 text-white/60">Diseño de Experimentos • Diagnosis y Validación del Modelo</p>
            </div>
        </div>
    </footer>

    <!-- Scroll to Top Button -->
    <button class="scroll-to-top" id="scrollToTopBtn" aria-label="Volver arriba">
        <i class="fas fa-arrow-up"></i>
    </button>

    <!-- Module Content Templates -->
'''

# Module 1: Fundamentos
m1_header = make_module_header(1, 'Fundamentos de la Diagnosis del Modelo', 
    'Comprender la motivación, hipótesis básicas y proceso secuencial de validación del modelo ANOVA.')
MODULE1 = f'''    <template id="module-1">
        {m1_header}

            {clase1}
        </div>
    </template>
'''

# Module 2: Análisis de Residuos
m2_header = make_module_header(2, 'Análisis de Residuos',
    'Dominar las técnicas de análisis de residuos: independencia, normalidad, detección de outliers y diagnóstico gráfico.')
MODULE2 = f'''    <template id="module-2">
        {m2_header}

            {clase2}
        </div>
    </template>
'''

# Module 3: Heterocedasticidad
m3_header = make_module_header(3, 'Diagnosis de Heterocedasticidad',
    'Aprender a detectar y evaluar la heterocedasticidad mediante tests de Bartlett, Cochran y Hartley.')
MODULE3 = f'''    <template id="module-3">
        {m3_header}

            {clase3}
        </div>
    </template>
'''

# Module 4: Transformaciones
m4_header = make_module_header(4, 'Transformaciones de Datos',
    'Conocer las transformaciones para estabilizar varianza y normalizar datos, incluyendo Box-Cox.')
MODULE4 = f'''    <template id="module-4">
        {m4_header}

            {clase4}
        </div>
    </template>
'''

# Module 5: Ejercicios
m5_header = make_module_header(5, 'Ejercicios de Autoevaluación',
    'Aplicar los conceptos aprendidos en problemas prácticos de diagnosis del modelo.')
MODULE5 = f'''    <template id="module-5">
        {m5_header}

            {ejercicios_content}
        </div>
    </template>
'''

# Module 6: Resumen y Referencias
m6_header = make_module_header(6, 'Resumen y Referencias',
    'Revisar los conceptos clave del proceso de diagnosis y las fuentes bibliográficas.')
MODULE6 = f'''    <template id="module-6">
        {m6_header}

            {summary_box}

            <h3>Referencias Bibliográficas</h3>
            {referencias}
        </div>
    </template>
'''

SCRIPT = '''
    <script>

        // --- COURSE DATA ---
        const courseData = {
            title: "Diagnosis y Validación del Modelo",
            modules: [
                { id: 1, title: "Fundamentos de la Diagnosis", shortTitle: "Fundamentos", duration: "20 min" },
                { id: 2, title: "Análisis de Residuos", shortTitle: "Residuos", duration: "25 min" },
                { id: 3, title: "Diagnosis de Heterocedasticidad", shortTitle: "Heterocedasticidad", duration: "25 min" },
                { id: 4, title: "Transformaciones de Datos", shortTitle: "Transformaciones", duration: "25 min" },
                { id: 5, title: "Ejercicios de Autoevaluación", shortTitle: "Ejercicios", duration: "15 min" },
                { id: 6, title: "Resumen y Referencias", shortTitle: "Resumen", duration: "10 min" }
            ]
        };

        // --- STATE MANAGEMENT ---
        let currentModuleIndex = 0;
        let completedModules = new Set();

        // --- DOM ELEMENTS ---
        const moduleNav = document.getElementById('module-nav');
        const contentArea = document.getElementById('content-area');

        // --- INIT ---
        function init() {
            renderNav();
            loadModule(0);
        }

        function renderNav() {
            moduleNav.innerHTML = '';
            courseData.modules.forEach((mod, index) => {
                const btn = document.createElement('button');
                const isActive = index === currentModuleIndex;
                const isDone = completedModules.has(index);
                btn.className = `sidebar-nav-item${isActive ? ' active' : ''}`;

                btn.innerHTML = `
                    <span style="line-height:1.3;">${mod.title}</span>
                    ${isDone ? '<span class="check-mark">✓</span>' : ''}
                `;
                btn.onclick = () => loadModule(index);
                moduleNav.appendChild(btn);
            });
        }

        function loadModule(index) {
            currentModuleIndex = index;
            renderNav();

            // Get template content
            const template = document.getElementById(`module-${index + 1}`);
            if (template) {
                contentArea.innerHTML = '';
                const content = template.content.cloneNode(true);
                contentArea.appendChild(content);

                // Add navigation buttons
                const navButtons = document.createElement('div');
                navButtons.className = 'mt-10 pt-6 border-t border-gray-200 flex justify-between items-center';
                navButtons.innerHTML = `
                    ${index > 0 ? `
                    <button onclick="loadModule(${index - 1})" class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 hover:text-secondary transition-colors">
                        <span>←</span> Anterior
                    </button>` : '<div></div>'}
                    <button onclick="markComplete(${index})" class="px-4 py-2 text-sm font-medium text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors ${completedModules.has(index) ? 'opacity-50' : ''}">
                        ${completedModules.has(index) ? '✓ Completado' : 'Marcar como completado'}
                    </button>
                    ${index < courseData.modules.length - 1 ? `
                    <button onclick="loadModule(${index + 1})" class="flex items-center gap-2 px-4 py-2 bg-secondary hover:bg-secondary/90 text-white rounded-lg text-sm font-medium transition-colors">
                        Siguiente Módulo <span>→</span>
                    </button>` : `
                    <div class="text-center">
                        <span class="text-emerald-600 font-bold">🎉 ¡Tema Completado!</span>
                    </div>`}
                `;
                contentArea.appendChild(navButtons);

                // Render LaTeX
                if (typeof renderMathInElement !== 'undefined') {
                    renderMathInElement(contentArea, {
                        delimiters: [
                            { left: '$$', right: '$$', display: true },
                            { left: '$', right: '$', display: false }
                        ],
                        throwOnError: false
                    });
                }
            }

            // Scroll to top of content
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function markComplete(index) {
            if (!completedModules.has(index)) {
                completedModules.add(index);
                renderNav();
                loadModule(index);
            }
        }

        // Scroll to Top Button functionality
        const scrollToTopBtn = document.getElementById('scrollToTopBtn');

        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollToTopBtn.classList.add('visible');
            } else {
                scrollToTopBtn.classList.remove('visible');
            }
        });

        scrollToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // ===== Sidebar Toggle =====
        const sidebarPanel = document.getElementById('sidebar-panel');
        const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
        const sidebarToggleIcon = document.getElementById('sidebarToggleIcon');
        let sidebarOpen = true;

        sidebarToggleBtn.addEventListener('click', () => {
            sidebarOpen = !sidebarOpen;
            if (sidebarOpen) {
                sidebarPanel.classList.remove('collapsed');
                sidebarPanel.style.opacity = '1';
                sidebarToggleIcon.className = 'fas fa-times text-sm';
            } else {
                sidebarPanel.classList.add('collapsed');
                sidebarPanel.style.opacity = '0';
                sidebarToggleIcon.className = 'fas fa-bars text-sm';
            }
        });

        // Wait for KaTeX to load, then init
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(init, 100);
        });
    </script>
</body>

</html>
'''

# Assemble the full HTML
full_html = HEAD + BODY_START + MODULE1 + MODULE2 + MODULE3 + MODULE4 + MODULE5 + MODULE6 + SCRIPT

# Write the output
with open('Dis_Exp_idoneidad_modelo.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"✅ File written successfully! Size: {len(full_html)} bytes")
print(f"   Modules: 6")
print(f"   Module 1 (Fundamentos): {len(clase1)} chars of content")
print(f"   Module 2 (Residuos): {len(clase2)} chars of content")
print(f"   Module 3 (Heteroced.): {len(clase3)} chars of content")
print(f"   Module 4 (Transform.): {len(clase4)} chars of content")
print(f"   Module 5 (Ejercicios): {len(ejercicios_content)} chars of content")
print(f"   Module 6 (Resumen): {len(summary_box) + len(referencias)} chars of content")
