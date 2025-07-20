from docx import Document
from docx.shared import Pt
from docx.shared import RGBColor

# Crear un nuevo documento para la versión completa
doc = Document()

# Formato base
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Funciones reutilizables
def add_heading(text, size=14):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 51, 153)

def add_subheading(text, size=12):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = True
    run.font.color.rgb = RGBColor(0, 51, 153)

def add_content(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)

def add_bullet(text):
    doc.add_paragraph(text, style='List Bullet')

# Encabezado
add_heading("JHON ALEXANDER VALENCIA MARULANDA, Ingeniero Mecánico")
doc.add_paragraph("Manizales, 170001, Colombia, (57) 311 3398444, jhonalexanderv@gmail.com, https://www.linkedin.com/in/jhonalexanderv/")

# RESUMEN
add_subheading("\nRESUMEN")
add_content(
    "Profesional altamente capacitado en Ingeniería Mecánica con más de 10 años de experiencia en mantenimiento industrial. "
    "Especialista en implementación de planes de mantenimiento preventivo y predictivo, logrando mejoras del 45% en la producción. "
    "Experiencia en liderazgo de equipos multidisciplinarios y optimización de procesos. Habilidades en diseño y ejecución de proyectos de ingeniería "
    "en ambientes desafiantes. Comprometido con la calidad y seguridad en el trabajo, puedo aportar significativamente a las necesidades de su organización."
)

# EXPERIENCIA LABORAL
add_subheading("\nEXPERIENCIA LABORAL")

# Lista de experiencias resumidas (desde imágenes)
experiencias = [
    ("10/2024 – 04/2025", "Jefe de Mantenimiento Mecánico, Mina El Gran Porvenir", "Líbano - Tolima", [
        "Implementé un plan de mantenimiento preventivo que mejoró la producción y disponibilidad de la planta.",
        "Lideré el estudio de ingeniería y la selección de equipos en Henan Baichy Machinery (Zhengzhou, China).",
        "Gestioné la importación de una Trituradora Cónica HP200, Molino 8x12 ft, y Celdas de flotación GF-20.",
        "Diseñé y construí obras civiles, además del montaje de equipos requeridos.",
        "Instalé compresores en el interior de la mina.",
        "Logré un incremento del 45% en la producción mediante optimización de procesos."
    ]),
    ("05/2024 – 09/2024", "Jefe de Mantenimiento Mecánico, EGM Colombia S.A.S.", "Santa Rosa de Osos - Antioquia", [
        "Desarrollé y ejecuté planes de mantenimiento preventivo y predictivo.",
        "Dirigí equipos multidisciplinarios de técnicos y operarios.",
        "Realicé análisis de fallas y propuse mejoras.",
        "Evalué necesidades de nuevos equipos y maquinaria.",
        "Diseñé y ejecuté proyectos de mejora de planta.",
        "Supervisé calidad del mantenimiento y proyectos.",
        "Aseguré estándares de seguridad y medio ambiente.",
        "Preparé informes de gestión y presentaciones.",
        "Logré generación de producción en menos de 4 meses."
    ]),
    ("12/2023 – 04/2024", "Especialista Mecánico, Consorcio PTAP Tibitoc 20", "Zipaquirá - Cundinamarca", [
        "Ejecución de revisiones de ingeniería y programación de montaje.",
        "Instalación de sistemas de tratamiento de agua garantizando funcionalidad."
    ]),
    ("11/2023 – 12/2023", "Coordinador de Ingeniería, Schrader Camargo", "Sopó - Cundinamarca", [
        "Desarrollé ingeniería de líneas de servicio para cervecería del Atlántico."
    ]),
    ("05/2023 – 08/2023", "Ingeniero Presupuesto, Schrader Camargo", "Sopó - Cundinamarca", [
        "Apoyo al departamento de operaciones en obra O-I Peldar."
    ]),
    ("04/2022 – 05/2023", "Ingeniero Mecánico Senior, O-I Peldar", "Zipaquirá - Cundinamarca", [
        "Revisiones de ingeniería para planta GLP y HFO.",
        "Supervisión de montaje de horno, sistemas de agua y transportadores verticales."
    ]),
    ("02/2022 – 04/2022", "Ingeniero Mecánico, China Harbour Engineering Company", "Dabeiba - Antioquia", [
        "Montaje de sistemas de ventilación y red contra incendios.",
        "Montaje de subestaciones de bombeo en túneles."
    ]),
    ("03/2021 – 01/2022", "Líder de obra, Compañía de Ingeniería y Montajes SAS CIM", "Dorada - Antioquia", [
        "Mantenimiento preventivo y correctivo en hornos, molinos, balsas y bandas transportadoras."
    ]),
    ("11/2018 – 11/2020", "Coordinador de Montaje Mecánico y Estructural, Merit Consultants", "Burrica - Antioquia", [
        "Supervisión de trituración, molienda, lixiviación, filtración, CCDs, Merrill Crowe, planta de pasta, WTP.",
        "Monitoreo de contratos y cronogramas de montaje."
    ]),
    ("03/2011 – 09/2014", "Ingeniero de Proyectos, TEPSA S.A.", "La Estrella - Antioquia", [
        "Cambio de sistema de sedimentadores en planta de tratamiento de agua.",
        "Supervisión de ventilación en planta Knight.",
        "Cambio de clarificador en Kimberly Clark.",
        "Montaje de torres de lavado, generación de agua desmineralizada y planta de residuos.",
        "Desmontaje y traslado de planta Nopco.",
        "Montaje de explosivos en mina PLJ.",
        "Ampliación de planta Proplas y planta de alimentos en Bogotá."
    ]),
    ("05/2008 – 05/2010", "Contratista, Drill Metal Ingeniería y Servicios EU", "Manizales - Caldas", [
        "Tratamiento térmico, mantenimiento correctivo, montaje de pasamanos y mecanizado.",
        "Fabricación Winkler y reparación Molino Pendular."
    ]),
    ("03/2008 – 07/2008", "Contratista Montaje, Pioneros Ingeniería S.A.", "Manizales - Caldas", [
        "Montaje de estructura del Polipasto Bibalva."
    ]),
    ("03/2007 – 12/2007", "Ingeniero de Montaje, Mastil Ingeniería Ltda.", "Pereira - Risaralda", [
        "Montaje de planta de gas natural.",
        "Instalación de refrigeración en Danone-Alquería."
    ]),
    ("01/2002 – 12/2006", "Docente de Instrumentación Industrial", "Antofagasta - Chile", [
        "Instructor en elementos de control industrial."
    ]),
    ("01/2005 – 12/2006", "Supervisor área Hidráulica, Hidromec Ltda.", "Tocopilla - Chile", [
        "Supervisión de proyectos hidráulicos.",
        "Reparación de molino de bolas en Bolivia y trabajos en Escondida."
    ]),
    ("01/2002 – 12/2003", "Jefe de Control y Calidad, Conymet Dunlop-Simsa", "Antofagasta - Chile", [
        "Supervisión de obras metamecánicas y planos para tolvas Caterpillar y Komatsu."
    ])
]

# Agregar experiencias
for fecha, cargo, ciudad, logros in experiencias:
    add_content(f"{fecha} — {cargo} \t\t {ciudad}")
    for logro in logros:
        add_bullet(logro)

# EDUCACIÓN
add_subheading("\nEDUCACIÓN")
educacion = [
    ("01/2003 – 12/2006", "Universidad Antofagasta", "Antofagasta, Chile", "Magíster en Ciencias de la Ingeniería, Mención Procesamiento de Minerales"),
    ("01/1994 – 12/1999", "Universidad Autónoma de Manizales", "Manizales, Colombia", "Ingeniero Mecánico"),
    ("01/2015 – 12/2015", "University of California, Irvine", "California", "Certificación en Project Management Principles (Coursera)"),
    ("01/1999 – 12/1999", "SENA", "Manizales, Colombia", "Técnico en Automatización y Control"),
    ("02/2006 – 04/2006", "Universidad Antofagasta", "Antofagasta, Chile", "Curso: Innovación y Desarrollo de Productos Químicos y Bioproductos")
]
for fecha, inst, loc, grado in educacion:
    add_content(f"{fecha} — {inst} \t\t {loc}")
    add_bullet(grado)

# CONOCIMIENTOS
add_subheading("\nCONOCIMIENTOS")
skills = [
    "Microsoft Office", "Matlab", "VBA", "Python", "Solidworks", "Inventor",
    "AutoCAD Plant 3D", "Trabajo en Equipo", "Liderazgo", "Toma de decisiones",
    "Habilidad de aprendizaje", "Creatividad"
]
doc.add_paragraph(", ".join(skills))

# IDIOMAS
add_subheading("\nIDIOMAS")
add_content("English (70% hablado y escrito)")

# REFERENCIAS
add_subheading("\nREFERENCIAS")
referencias = [
    "Dr. Luis Alberto Cisternas Arapio – Universidad Católica del Norte – lcisternas@uantof.cl",
    "Franklin Gonzalez Gomez – Continental Goldcorp – ingfgg@gmail.com – +34 642414997",
    "Nicholas Blanchette – Merit Consultants – nick.blanchette@cementation.com",
    "Alexander Valencia – Asesor SENA – 3206888811",
    "Carlos Roure – Schrader Camargo – 3002161814",
    "Dereck Seah – Independiente – +59 171325296"
]
for ref in referencias:
    add_bullet(ref)

# Guardar archivo completo
doc.save("Hoja_de_Vida_Jhon_Valencia_COMPLETA.docx")

print("Hoja de vida generada exitosamente: Hoja_de_Vida_Jhon_Valencia_COMPLETA.docx")