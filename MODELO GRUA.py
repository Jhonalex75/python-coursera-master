import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función auxiliar para convertir grados a radianes
def to_radians(angle):
    """Convierte un ángulo de grados a radianes."""
    return math.radians(angle)

class LiftingPlanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guía de Estudio: Plan de Izaje Seguro")
        self.geometry("1000x750") # Ajustado para mejor visualización inicial

        # --- Estilo de la Aplicación ---
        self.style = ttk.Style(self)
        self.style.theme_use('clam') # Un tema moderno para la interfaz
        
        # Configuración de estilos para diferentes elementos de la UI
        self.style.configure("Header.TLabel", font=("Helvetica", 20, "bold"), padding=10)
        self.style.configure("SubHeader.TLabel", font=("Helvetica", 16, "bold"), padding=5)
        self.style.configure("SectionTitle.TLabel", font=("Helvetica", 14, "bold"), foreground="#003366", padding=10)
        self.style.configure("Accordion.TButton", font=("Helvetica", 12, "bold"), width=60, anchor="w")
        self.style.configure("Input.TLabel", font=("Helvetica", 10, "bold"))
        self.style.configure("Result.TLabel", font=("Helvetica", 10))
        self.style.configure("Critical.TLabel", font=("Helvetica", 10, "bold"), foreground="red")
        self.style.configure("Safe.TLabel", font=("Helvetica", 10, "bold"), foreground="green")
        self.style.configure("Warning.TLabel", font=("Helvetica", 10, "bold"), foreground="orange")
        self.style.configure("Nav.TButton", font=("Helvetica", 11, "bold"), padding=5)
        self.style.configure("Quiz.TButton", font=("Helvetica", 10), padding=5, width=30)
        self.style.configure("QuizQuestion.TLabel", font=("Helvetica", 12), wraplength=500)
        self.style.configure("Correct.TLabel", font=("Helvetica", 10, "bold"), foreground="green")
        self.style.configure("Incorrect.TLabel", font=("Helvetica", 10, "bold"), foreground="red")
        self.style.configure("Correct.TButton", foreground="white", background="green", font=("Helvetica", 10, "bold")) # Estilo para botón correcto
        self.style.configure("Incorrect.TButton", foreground="white", background="red", font=("Helvetica", 10, "bold")) # Estilo para botón incorrecto


        # --- Variables de estado y UI ---
        # Controla la sección activa mostrada en la interfaz
        self.active_section_name = tk.StringVar(value="standards")
        # Configura las variables para la sección de herramienta interactiva
        self.setup_interactive_tool_vars()
        # Configura las variables para la sección de cuestionario
        self.setup_quiz_vars()

        # --- Layout Principal de la Aplicación ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Encabezado principal de la aplicación
        header = ttk.Label(main_frame, text="Guía de Estudio: Plan de Izaje Seguro", style="Header.TLabel", anchor="center")
        header.pack(pady=10)
        
        # Subencabezado descriptivo
        subheader = ttk.Label(main_frame, text="Aprende y analiza los principios de las operaciones de izaje industrial.", style="SubHeader.TLabel", anchor="center")
        subheader.pack(pady=(0,10))

        # --- Barra de Navegación entre Secciones ---
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(pady=10)

        # Definición de los botones de navegación
        buttons_info = [
            ("Estándares", "standards", "📚"),
            ("Elementos del Plan", "plan-elements", "🎓"),
            ("Herramienta Interactiva", "interactive-tool", "⚙️"),
            ("Cuestionario", "quiz", "❓")
        ]

        self.nav_buttons = {}
        for text, section_name, icon in buttons_info:
            btn = ttk.Button(nav_frame, text=f"{icon} {text}", style="Nav.TButton",
                             command=lambda s=section_name: self.show_section(s))
            btn.pack(side=tk.LEFT, padx=5)
            self.nav_buttons[section_name] = btn
        
        # --- Contenedor para las diferentes secciones de contenido ---
        self.sections_container = ttk.Frame(main_frame)
        self.sections_container.pack(expand=True, fill=tk.BOTH, pady=10)

        self.sections = {}
        # Creación de cada sección de la aplicación
        self.create_standards_section()
        self.create_plan_elements_section()
        self.create_interactive_tool_section()
        self.create_quiz_section()

        # --- Pie de página (Footer) ---
        footer = ttk.Label(main_frame, text="© 2025 Guía de Estudio de Izaje Seguro. Todos los derechos reservados.", font=("Helvetica", 8), anchor="center")
        footer.pack(pady=10, side=tk.BOTTOM)

        # Mostrar la sección de estándares al inicio
        self.show_section("standards")

    def setup_interactive_tool_vars(self):
        """Configura las variables de Tkinter para la sección de la herramienta interactiva.
        Todas las unidades se manejan internamente en kg, m, kPa para consistencia.
        """
        self.load_weight_var = tk.DoubleVar(value=10000) # Peso de la carga en kg
        self.crane_capacity_var = tk.DoubleVar(value=20000) # Capacidad nominal de la grúa en kg
        self.boom_length_var = tk.DoubleVar(value=30) # Longitud de la pluma en metros (m)
        self.radius_var = tk.DoubleVar(value=15) # Radio de operación en metros (m)
        self.sling_angle_horizontal_var = tk.DoubleVar(value=60) # Ángulo de la eslinga con la horizontal en grados (°)
        self.num_sling_legs_var = tk.IntVar(value=2) # Número de patas de la eslinga
        self.outrigger_pad_length_var = tk.DoubleVar(value=1) # Longitud de la zapata del estabilizador en metros (m)
        self.outrigger_pad_width_var = tk.DoubleVar(value=1) # Ancho de la zapata del estabilizador en metros (m)
        self.ground_bearing_capacity_var = tk.DoubleVar(value=200) # Capacidad portante del terreno en kiloPascales (kPa)
        self.crane_weight_var = tk.DoubleVar(value=15000) # Peso de la grúa para cálculo de estabilizadores en kg
        self.safety_factor_var = tk.DoubleVar(value=1.25) # Factor de seguridad de izaje (adimensional)

        # Variables para mostrar los resultados de los cálculos
        self.crane_capacity_percentage_str = tk.StringVar(value="0.00%") # % de capacidad de grúa utilizada
        self.is_critical_lift_str = tk.StringVar(value="") # Indicador de izaje crítico
        self.sling_leg_tension_str = tk.StringVar(value="0.00 kg") # Tensión por pata de eslinga en kg
        self.pressure_per_outrigger_str = tk.StringVar(value="0.00 kPa") # Presión por estabilizador en kPa
        self.outrigger_capacity_percentage_str = tk.StringVar(value="0.00%") # % de capacidad portante del terreno utilizada
        self.derated_crane_capacity_str = tk.StringVar(value="0.00 kg") # Capacidad derateada de la grúa en kg

        # Registrar callbacks para que los cálculos se actualicen automáticamente al cambiar los inputs
        for var in [self.load_weight_var, self.crane_capacity_var, self.boom_length_var, 
                    self.radius_var, self.sling_angle_horizontal_var, self.num_sling_legs_var,
                    self.outrigger_pad_length_var, self.outrigger_pad_width_var,
                    self.ground_bearing_capacity_var, self.crane_weight_var, self.safety_factor_var]:
            var.trace_add("write", self.update_interactive_calculations)

    def setup_quiz_vars(self):
        """Configura las variables de Tkinter y los datos para la sección del cuestionario."""
        self.quiz_started = tk.BooleanVar(value=False)
        self.current_question_index = tk.IntVar(value=0)
        self.quiz_results = {} # Almacenará los resultados de cada pregunta: {index: is_correct}
        self.quiz_score_str = tk.StringVar(value="Puntuación: 0%")
        # Definición de las preguntas y respuestas del cuestionario
        self.quiz_questions = [
            {
                "question": "¿Qué norma ASME B30 cubre las Grúas Móviles y Locomotoras?",
                "options": ["ASME B30.9", "ASME B30.5", "ASME B30.10", "ASME B30.26"],
                "answer": "ASME B30.5"
            },
            {
                "question": "¿Cuál es el factor clave para determinar si un izaje es 'crítico' según la capacidad de la grúa (considerando el factor de seguridad)?",
                "options": ["Más del 50% de la capacidad derateada", "Más del 75% de la capacidad derateada", "Más del 90% de la capacidad derateada", "Cualquier izaje con más de 10 toneladas"],
                "answer": "Más del 75% de la capacidad derateada"
            },
            {
                "question": "¿Qué tipo de inspección de eslingas debe realizarse 'antes de cada turno/uso intensivo'?",
                "options": ["Inicial", "Periódica", "Frecuente", "Anual"],
                "answer": "Frecuente"
            },
            {
                "question": "¿Cuál es la velocidad máxima de viento generalmente aceptable para las operaciones de grúa?",
                "options": ["20 km/hr", "30 km/hr", "40 km/hr", "50 km/hr"],
                "answer": "40 km/hr"
            },
            {
                "question": "Si una eslinga tiene un ángulo de estrangulación menor a 120 grados, ¿cómo afecta esto su capacidad nominal?",
                "options": ["Aumenta la capacidad", "No tiene efecto", "Reduce la capacidad", "Depende del material de la eslinga"],
                "answer": "Reduce la capacidad"
            }
        ]
        # Variables para mostrar la pregunta y opciones del quiz en la UI
        self.quiz_question_label_var = tk.StringVar()
        self.quiz_options_vars = [tk.StringVar() for _ in range(4)] # Asumiendo un máximo de 4 opciones por pregunta
        self.quiz_feedback_vars = [tk.StringVar() for _ in range(4)]
        self.quiz_result_details_var = tk.StringVar()


    def show_section(self, section_name):
        """Muestra la sección de la aplicación correspondiente al nombre dado."""
        self.active_section_name.set(section_name)
        for name, frame in self.sections.items():
            if name == section_name:
                frame.pack(expand=True, fill=tk.BOTH)
            else:
                frame.pack_forget()
        
        # Actualizar el estilo del botón de navegación activo
        for name, btn in self.nav_buttons.items():
            if name == section_name:
                btn.state(['pressed']) # Marca el botón como presionado
            else:
                btn.state(['!pressed']) # Desmarca los otros botones

        # Si la sección mostrada es la herramienta interactiva, actualizar los cálculos
        if section_name == "interactive-tool":
            self.update_interactive_calculations()


    def create_standards_section(self):
        """Crea la sección de Estándares Clave de Izaje."""
        frame = ttk.Frame(self.sections_container, padding="10")
        self.sections["standards"] = frame

        ttk.Label(frame, text="Estándares Clave de Izaje", style="SectionTitle.TLabel").pack(anchor="w")
        
        content_text = """
Las normas de la serie ASME B30 y las regulaciones de OSHA son fundamentales para la seguridad en las operaciones de izaje. Aunque voluntarias, son guías desarrolladas por expertos para prevenir lesiones y asegurar un entorno de trabajo seguro.

Normas ASME B30:
  • ASME B30.5: Grúas Móviles y Locomotoras
  • ASME B30.9: Eslingas
  • ASME B30.10: Ganchos
  • ASME B30.26: Herrajes de Aparejo
  • ASME B30.23: Sistemas de Elevación de Personal (en casos excepcionales)
  Estas normas son revisadas y modificadas periódicamente.

Regulaciones OSHA:
  • 29 CFR 1910.184: Eslingas
  • 29 CFR 1926.550: Grúas, Torres, Enganches, Elevadores y Transportadores
  Las regulaciones de OSHA son obligatorias y establecen requisitos mínimos.

Importancia de las Normas:
  Estas normas son cruciales para prevenir o minimizar lesiones al guiar a fabricantes, propietarios, empleadores y operarios en la implementación de prácticas seguras.
        """
        ttk.Label(frame, text=content_text, wraplength=800, justify=tk.LEFT, font=("Helvetica", 10)).pack(anchor="w", pady=5)

    def create_plan_elements_section(self):
        """Crea la sección de Elementos de un Plan de Izaje Seguro con un acordeón interactivo."""
        frame = ttk.Frame(self.sections_container, padding="10")
        self.sections["plan-elements"] = frame
        
        ttk.Label(frame, text="Elementos de un Plan de Izaje Seguro", style="SectionTitle.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Un plan de izaje seguro implica considerar una serie de temas, problemas y factores.", wraplength=800, justify=tk.LEFT, font=("Helvetica", 10)).pack(anchor="w", pady=(0,10))

        # Contenedor para el acordeón con scrollbar para manejar contenido extenso
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Datos para las secciones del acordeón
        sections_data = [
            ("1. Evaluación de la Carga", 
             "Determinar el peso y el centro de gravedad (CG) de la carga es el primer paso crítico. Un cálculo preciso de la masa es fundamental.\nEjemplo: Para objetos regulares, Masa = Volumen x Densidad."),
            ("2. Selección del Equipo", 
             "Elegir la grúa y los accesorios adecuados. Considerar capacidad, longitud de pluma, tipo de eslingas, condiciones del terreno."),
            ("3. Inspección de Equipos y Accesorios", 
             "Tipos: Inicial, Frecuente (antes de cada turno), Periódica (por persona calificada).\nPuntos comunes: Controles, sistema hidráulico, frenos, pluma, cables, ganchos, eslingas (etiqueta, cortes, nudos), grilletes."),
            ("4. Condiciones del Área de Trabajo", 
             "Evaluar: Estabilidad del terreno (presión portante), condiciones ambientales (viento < 40 km/hr), delimitación, obstáculos (líneas eléctricas)."),
            ("5. Configuración del Izaje", 
             "Planificar: Posición inicial y final, radio de operación, ángulo y longitud de pluma. Consultar tablas de carga."),
            ("6. Cálculos Críticos", 
             "Ejemplos: Carga en patas de eslinga (aumenta con menor ángulo horizontal), reducción de capacidad en estrangulamiento (<120°), trigonometría."),
            ("7. Comunicación y Señales", 
             "Utilizar señales manuales estandarizadas (ASME B30.5), comunicación radial si es necesario, un único señalero."),
            ("8. Personal Calificado", 
             "Operador de grúa, Rigger/Aparejador, Señalero. Capacitación en funcionamiento, elementos, señales, tablas, riesgos, emergencias.")
        ]

        self.accordion_sections = {} # Diccionario para almacenar las frames de contenido del acordeón
        for title, content in sections_data:
            btn = ttk.Button(scrollable_frame, text=f"▼ {title}", style="Accordion.TButton", 
                             command=lambda t=title: self.toggle_accordion_section(t, scrollable_frame))
            btn.pack(fill="x", pady=2)
            
            content_frame = ttk.Frame(scrollable_frame, padding=(20, 5, 5, 5)) # Frame para el contenido de la sección
            ttk.Label(content_frame, text=content, wraplength=700, justify=tk.LEFT, font=("Helvetica", 9)).pack(anchor="w")
            self.accordion_sections[title] = {"button": btn, "frame": content_frame, "open": False}

        # Sección de Riesgos Comunes
        ttk.Label(scrollable_frame, text="Riesgos Comunes a Evitar", font=("Helvetica", 11, "bold"), foreground="darkred").pack(anchor="w", pady=(15,5))
        risks_text = """
• Uso de equipo no estándar o defectuoso.
• Sobrecarga de la grúa o los accesorios.
• Terreno inestable o preparación inadecuada.
• Falta de delimitación y señalización.
• Comunicación deficiente o personal no calificado.
• Accesorios de izaje defectuosos.
• Falta de capacitación en cálculos y tablas de carga.
        """
        ttk.Label(scrollable_frame, text=risks_text, wraplength=700, justify=tk.LEFT, font=("Helvetica", 9)).pack(anchor="w")


    def toggle_accordion_section(self, title, parent_frame):
        """Expande o contrae una sección del acordeón."""
        section = self.accordion_sections[title]
        if section["open"]:
            section["frame"].pack_forget()
            section["button"].config(text=f"▼ {title}")
            section["open"] = False
        else:
            section["frame"].pack(fill="x", after=section["button"])
            section["button"].config(text=f"▲ {title}")
            section["open"] = True
        
        # Forzar la actualización del canvas para que el scrollbar se ajuste correctamente
        parent_frame.master.update_idletasks() 
        parent_frame.master.configure(scrollregion=parent_frame.master.bbox("all"))


    def create_interactive_tool_section(self):
        """Crea la sección de la herramienta interactiva para cálculos de izaje."""
        frame = ttk.Frame(self.sections_container, padding="10")
        self.sections["interactive-tool"] = frame
        
        ttk.Label(frame, text="Análisis Interactivo de Plan de Izaje", style="SectionTitle.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Ingresa los parámetros del izaje para visualizar los cálculos críticos y el impacto en la seguridad.", wraplength=800, justify=tk.LEFT, font=("Helvetica", 10)).pack(anchor="w", pady=(0,10))

        # --- Layout en dos columnas: Inputs y Resultados/Visualizaciones ---
        main_paned_window = ttk.PanedWindow(frame, orient=tk.HORIZONTAL)
        main_paned_window.pack(expand=True, fill=tk.BOTH)

        # --- Columna de Inputs ---
        inputs_frame_container = ttk.Frame(main_paned_window, padding="10", relief="groove", borderwidth=2)
        main_paned_window.add(inputs_frame_container, weight=1)

        ttk.Label(inputs_frame_container, text="Parámetros del Izaje", style="SubHeader.TLabel").pack(pady=5)

        # Canvas y Scrollbar para los campos de entrada
        inputs_canvas = tk.Canvas(inputs_frame_container)
        inputs_scrollbar = ttk.Scrollbar(inputs_frame_container, orient="vertical", command=inputs_canvas.yview)
        inputs_scrollable_frame = ttk.Frame(inputs_canvas)
        inputs_scrollable_frame.bind("<Configure>", lambda e: inputs_canvas.configure(scrollregion=inputs_canvas.bbox("all")))
        inputs_canvas.create_window((0, 0), window=inputs_scrollable_frame, anchor="nw")
        inputs_canvas.configure(yscrollcommand=inputs_scrollbar.set)
        
        inputs_canvas.pack(side="left", fill="both", expand=True)
        inputs_scrollbar.pack(side="right", fill="y")

        # Definición de los campos de entrada con sus etiquetas, variables y tipos de widget
        input_fields = [
            ("Peso de la Carga (kg):", self.load_weight_var),
            ("Capacidad Nominal Grúa (kg):", self.crane_capacity_var),
            ("Factor de Seguridad Izaje:", self.safety_factor_var), 
            ("Longitud de la Pluma (m):", self.boom_length_var),
            ("Radio de Operación (m):", self.radius_var),
            ("Ángulo Eslinga (horizontal, °):", self.sling_angle_horizontal_var, (10, 89), "scale"), # Rango para slider
            ("Número de Patas de Eslinga:", self.num_sling_legs_var, [1, 2, 3, 4], "combobox"), # Opciones para combobox
            ("Peso de la Grúa (kg):", self.crane_weight_var),
            ("Longitud Zapata Estabilizador (m):", self.outrigger_pad_length_var),
            ("Ancho Zapata Estabilizador (m):", self.outrigger_pad_width_var),
            ("Capacidad Portante Terreno (kPa):", self.ground_bearing_capacity_var),
        ]

        # Creación dinámica de los widgets de entrada
        for item in input_fields:
            label_text = item[0]
            var = item[1]
            
            row_frame = ttk.Frame(inputs_scrollable_frame)
            row_frame.pack(fill="x", pady=3)
            ttk.Label(row_frame, text=label_text, style="Input.TLabel").pack(side=tk.LEFT, padx=5, anchor="w")

            if len(item) > 3 and item[3] == "scale": # Si es un slider (escala)
                min_val, max_val = item[2]
                scale_val_frame = ttk.Frame(row_frame)
                scale_val_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
                scale = ttk.Scale(scale_val_frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL, variable=var, length=120)
                scale.pack(side=tk.LEFT, fill="x", expand=True)
                ttk.Label(scale_val_frame, textvariable=var, width=5).pack(side=tk.LEFT, padx=(5,0))
            elif len(item) > 3 and item[3] == "combobox": # Si es un combobox
                options = item[2]
                combo = ttk.Combobox(row_frame, textvariable=var, values=options, state="readonly", width=10)
                combo.pack(side=tk.LEFT, padx=5)
            else: # Si es un campo de entrada de texto normal
                entry = ttk.Entry(row_frame, textvariable=var, width=15)
                entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        # --- Columna de Resultados y Visualizaciones ---
        results_viz_frame = ttk.Frame(main_paned_window, padding="10")
        main_paned_window.add(results_viz_frame, weight=2)

        # Resultados del Análisis
        results_frame = ttk.Frame(results_viz_frame, padding="10", relief="groove", borderwidth=2)
        results_frame.pack(fill="x", pady=(0,10))

        results_title_label = ttk.Label(results_frame, text="Resultados del Análisis", style="SubHeader.TLabel")
        results_title_label.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")

        # Mostrar capacidad derateada de la grúa
        ttk.Label(results_frame, text="Capacidad Derateada Grúa:", style="Result.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.derated_cap_label = ttk.Label(results_frame, textvariable=self.derated_crane_capacity_str, style="Result.TLabel")
        self.derated_cap_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Mostrar porcentaje de capacidad de grúa utilizada e indicador de izaje crítico
        ttk.Label(results_frame, text="% Capacidad Grúa Utilizada (sobre derateada):", style="Result.TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.cap_perc_label = ttk.Label(results_frame, textvariable=self.crane_capacity_percentage_str) 
        self.cap_perc_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        self.critical_lift_label = ttk.Label(results_frame, textvariable=self.is_critical_lift_str)
        self.critical_lift_label.grid(row=2, column=2, sticky="w", padx=5, pady=2)

        # Mostrar tensión por pata de eslinga
        ttk.Label(results_frame, text="Tensión por Pata de Eslinga:", style="Result.TLabel").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(results_frame, textvariable=self.sling_leg_tension_str, style="Result.TLabel").grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        # Mostrar presión por estabilizador
        ttk.Label(results_frame, text="Presión por Estabilizador:", style="Result.TLabel").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(results_frame, textvariable=self.pressure_per_outrigger_str, style="Result.TLabel").grid(row=4, column=1, sticky="w", padx=5, pady=2)

        # Mostrar porcentaje de capacidad portante del terreno utilizada
        ttk.Label(results_frame, text="% Capacidad Portante Terreno Utilizada:", style="Result.TLabel").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.outrigger_perc_label = ttk.Label(results_frame, textvariable=self.outrigger_capacity_percentage_str) 
        self.outrigger_perc_label.grid(row=5, column=1, sticky="w", padx=5, pady=2)
        
        # Nota importante sobre WLL de eslingas
        ttk.Label(results_frame, text="Nota: Asegúrese de que las eslingas y accesorios tengan un WLL adecuado con su propio factor de seguridad.", font=("Helvetica", 8, "italic")).grid(row=6, column=0, columnspan=3, sticky="w", padx=5, pady=(10,5))

        # Configurar la columna 1 para que se expanda y alinee los valores
        results_frame.columnconfigure(1, weight=1)


        # Visualización Simplificada de la Grúa y la Carga
        viz_frame = ttk.Frame(results_viz_frame, padding="10", relief="groove", borderwidth=2)
        viz_frame.pack(fill="x", pady=10)
        ttk.Label(viz_frame, text="Posición de la Grúa y la Carga (Simplificado)", style="SubHeader.TLabel").pack()
        self.crane_canvas = tk.Canvas(viz_frame, width=380, height=230, bg="white")
        self.crane_canvas.pack(pady=5)
        ttk.Label(viz_frame, text="*El ángulo de pluma se calcula para que la punta esté sobre la carga al radio dado.", font=("Helvetica", 8, "italic")).pack()

        # Gráfico de Tensión de Eslinga vs. Ángulo (Matplotlib)
        chart_frame = ttk.Frame(results_viz_frame, padding="10", relief="groove", borderwidth=2)
        chart_frame.pack(fill="both", expand=True, pady=10)
        ttk.Label(chart_frame, text="Tensión de Eslinga vs. Ángulo", style="SubHeader.TLabel").pack()
        
        self.fig, self.ax = plt.subplots(figsize=(5, 3.5)) 
        self.fig.subplots_adjust(bottom=0.2, left=0.25, right=0.95, top=0.9) # Ajustar márgenes para etiquetas
        self.line_tension, = self.ax.plot([], [], label="Tensión Eslinga (kg)")
        self.ax.set_xlabel("Ángulo (horizontal, °)", fontsize=9)
        self.ax.set_ylabel("Tensión por Pata (kg)", fontsize=9)
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        self.ax.legend(fontsize=8)
        self.ax.grid(True)

        self.canvas_mpl = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas_mpl_widget = self.canvas_mpl.get_tk_widget()
        self.canvas_mpl_widget.pack(fill=tk.BOTH, expand=True)
        self.canvas_mpl.draw()

        # Realizar los cálculos iniciales al cargar la sección
        self.update_interactive_calculations() 

    def update_interactive_calculations(self, *args):
        """Realiza todos los cálculos de ingeniería y actualiza la interfaz de usuario.
        Las unidades de entrada y salida se manejan para ser consistentes (kg, m, kPa).
        """
        try:
            # Obtener valores de las variables de entrada
            load_w = self.load_weight_var.get() # kg
            crane_cap = self.crane_capacity_var.get() # kg
            boom_l = self.boom_length_var.get() # m
            rad = self.radius_var.get() # m
            sling_angle_h = self.sling_angle_horizontal_var.get() # grados
            num_legs = self.num_sling_legs_var.get() # adimensional
            pad_l = self.outrigger_pad_length_var.get() # m
            pad_w = self.outrigger_pad_width_var.get() # m
            ground_cap = self.ground_bearing_capacity_var.get() # kPa
            crane_w = self.crane_weight_var.get() # kg
            safety_f = self.safety_factor_var.get() # adimensional

            # Asegurar que el factor de seguridad sea al menos 1.0 para evitar divisiones por cero o resultados ilógicos
            if safety_f <= 0: safety_f = 1.0 

            # --- Cálculo de Capacidad de Grúa Derateada ---
            # La capacidad derateada es la capacidad nominal dividida por el factor de seguridad.
            # Esto asegura que la grúa no se opere al 100% de su capacidad teórica, añadiendo un margen de seguridad.
            derated_crane_capacity = crane_cap / safety_f if crane_cap > 0 and safety_f > 0 else 0
            self.derated_crane_capacity_str.set(f"{derated_crane_capacity:.2f} kg")

            # --- Cálculo del Porcentaje de Capacidad de Grúa Utilizada ---
            # Indica qué tan cerca está el peso de la carga de la capacidad derateada de la grúa.
            crane_cap_perc = (load_w / derated_crane_capacity) * 100 if derated_crane_capacity > 0 else float('inf')
            self.crane_capacity_percentage_str.set(f"{crane_cap_perc:.2f}%")
            
            # Determinar si el izaje es crítico (generalmente > 75% de la capacidad derateada)
            is_critical = crane_cap_perc > 75
            self.is_critical_lift_str.set("(¡Izaje Crítico!)" if is_critical else "(Izaje No Crítico)")
            # Actualizar el estilo de la etiqueta según si es crítico o no
            self.cap_perc_label.configure(style="Critical.TLabel" if is_critical else "Safe.TLabel")
            self.critical_lift_label.configure(style="Critical.TLabel" if is_critical else "Safe.TLabel")


            # --- Cálculo de Tensión por Pata de Eslinga ---
            # La tensión en cada pata de la eslinga aumenta a medida que el ángulo horizontal disminuye.
            # Se usa la componente vertical de la fuerza para distribuir la carga.
            sling_leg_tension = 0 # kg
            if num_legs > 0 and 0 < sling_angle_h < 90:
                # Convertir el ángulo horizontal a ángulo vertical para el cálculo trigonométrico
                sling_angle_v = 90 - sling_angle_h 
                cos_val = math.cos(to_radians(sling_angle_v))
                if cos_val != 0: 
                    # Tensión = (Peso de la Carga / Número de Patas) / cos(Ángulo Vertical)
                    sling_leg_tension = (load_w / num_legs) / cos_val
            self.sling_leg_tension_str.set(f"{sling_leg_tension:.2f} kg")

            # --- Cálculo de Presión por Estabilizador (Outrigger) ---
            # Es crucial para asegurar que el terreno puede soportar el peso combinado de la grúa y la carga.
            outrigger_pad_area = pad_l * pad_w # Área de una zapata en m^2
            # Carga total sobre los estabilizadores (peso de la carga + peso de la grúa) en kg
            # Convertir a Newtons (N) multiplicando por la gravedad (9.81 m/s^2)
            total_outrigger_load_N = (load_w + crane_w) * 9.81 
            # Presión = Fuerza / Área. Dividir por 4 porque hay 4 estabilizadores.
            # Convertir a kPa dividiendo por 1000 (ya que el área está en m^2 y la fuerza en N, el resultado es Pa)
            pressure_per_outrigger_kPa = (total_outrigger_load_N / 4) / (outrigger_pad_area * 1000) if outrigger_pad_area > 0 else 0
            self.pressure_per_outrigger_str.set(f"{pressure_per_outrigger_kPa:.2f} kPa")

            # --- Cálculo del Porcentaje de Capacidad Portante del Terreno Utilizada ---
            outrigger_cap_perc = (pressure_per_outrigger_kPa / ground_cap) * 100 if ground_cap > 0 else float('inf')
            self.outrigger_capacity_percentage_str.set(f"{outrigger_cap_perc:.2f}%")
            # Actualizar el estilo de la etiqueta según el porcentaje de uso del terreno
            if outrigger_cap_perc > 100:
                 self.outrigger_perc_label.configure(style="Critical.TLabel") # Excede la capacidad
            elif outrigger_cap_perc > 80: 
                 self.outrigger_perc_label.configure(style="Warning.TLabel") # Cerca del límite
            else:
                 self.outrigger_perc_label.configure(style="Safe.TLabel") # Dentro de límites seguros

            # Actualizar las visualizaciones
            self.draw_crane_visualization(boom_l, rad)
            self.update_sling_tension_chart(load_w, num_legs)

        except tk.TclError: 
            # Este error puede ocurrir si las variables no están completamente inicializadas al inicio.
            # Se ignora, ya que los callbacks se ejecutarán de nuevo cuando los valores sean válidos.
            pass 
        except Exception as e:
            # Captura cualquier otra excepción durante los cálculos y la imprime (útil para depuración)
            # print(f"Error en cálculos: {e}") 
            pass
            
    def draw_crane_visualization(self, boom_length, radius):
        """Dibuja una representación simplificada de la grúa y la carga en el canvas.
        Las unidades de entrada son metros.
        """
        # Asegurarse que el canvas está completamente renderizado antes de dibujar
        self.crane_canvas.update_idletasks() 
        canvas = self.crane_canvas
        canvas.delete("all") # Limpiar dibujos anteriores
        
        # Obtener dimensiones del canvas
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <=1 or h <=1: 
            # Si el canvas aún no tiene dimensiones válidas, reintentar después de un breve retraso
            self.after(50, lambda: self.draw_crane_visualization(boom_length, radius)) 
            return

        # Definir el nivel del suelo y la base de la grúa
        ground_level = h - 20
        crane_base_x = w * 0.25 
        crane_base_y = ground_level
        
        # Dibujar el suelo y la base de la grúa
        canvas.create_line(0, ground_level, w, ground_level, fill="black", width=2)
        canvas.create_rectangle(crane_base_x - 15, ground_level - 20, crane_base_x + 15, ground_level, fill="gray", outline="black")

        # Validaciones básicas para la pluma y el radio
        if boom_length <= 0 or radius <= 0:
            canvas.create_text(w/2, h/2, text="Longitud de pluma y radio\ndeben ser > 0", fill="red", justify="center", font=("Helvetica", 9))
            return
        if radius > boom_length:
            canvas.create_text(w/2, h/2, text="Radio no puede ser mayor\nque Longitud Pluma", fill="red", justify="center", font=("Helvetica", 9))
            return

        try:
            # Calcular el ángulo de la pluma con la vertical (desde el pivote de la grúa)
            # Esto se basa en la relación trigonométrica entre el radio, la longitud de la pluma y el ángulo.
            angle_boom_vertical_rad = math.acos(radius / boom_length)
        except ValueError: 
             canvas.create_text(w/2, h/2, text="Error cálculo ángulo (Radio > Pluma)", fill="red", justify="center", font=("Helvetica", 9))
             return

        # Convertir a ángulo horizontal y grados para visualización
        angle_boom_horizontal_rad = math.pi/2 - angle_boom_vertical_rad
        angle_boom_horizontal_deg = math.degrees(angle_boom_horizontal_rad)

        # Escalar las dimensiones para que se ajusten al canvas
        # Se calcula un factor de escala para que la pluma y el radio se vean bien dentro del área de dibujo.
        drawing_width_available = w - crane_base_x - 20 
        scale_factor = drawing_width_available / (boom_length * 1.2) 
        if radius * scale_factor > drawing_width_available * 0.8 : 
            scale_factor = (drawing_width_available * 0.8) / radius

        boom_viz_length = boom_length * scale_factor
        radius_viz = radius * scale_factor
        
        # Coordenadas del pivote de la pluma (ligeramente por encima de la base de la grúa)
        boom_pivot_x = crane_base_x
        boom_pivot_y = crane_base_y - 10

        # Coordenadas del extremo de la pluma
        boom_end_x = boom_pivot_x + boom_viz_length * math.cos(angle_boom_horizontal_rad)
        boom_end_y = boom_pivot_y - boom_viz_length * math.sin(angle_boom_horizontal_rad)

        # Dibujar la pluma
        canvas.create_line(boom_pivot_x, boom_pivot_y, boom_end_x, boom_end_y, fill="blue", width=5, capstyle=tk.ROUND)

        # Dibujar la carga (colgando verticalmente de la punta de la pluma)
        canvas.create_line(boom_end_x, boom_end_y, boom_end_x, boom_end_y + 15, fill="black", width=1.5) # Cable corto
        canvas.create_rectangle(boom_end_x - 10, boom_end_y + 15, boom_end_x + 10, boom_end_y + 35, fill="orange", outline="black") # Carga

        # Línea y texto para el Radio de Operación
        canvas.create_line(boom_pivot_x, ground_level, boom_end_x, ground_level, fill="red", arrow=tk.BOTH, width=1.5)
        canvas.create_text(boom_pivot_x + (boom_end_x - boom_pivot_x)/2, ground_level - 10, text=f"Radio: {radius:.1f}m", fill="black", font=("Helvetica", 8), anchor="s")
        
        # Texto para Longitud y Ángulo de Pluma
        text_boom_x = boom_pivot_x + (boom_viz_length/2) * math.cos(angle_boom_horizontal_rad) + 5 * math.sin(angle_boom_horizontal_rad)
        text_boom_y = boom_pivot_y - (boom_viz_length/2) * math.sin(angle_boom_horizontal_rad) - 5 * math.cos(angle_boom_horizontal_rad)
        canvas.create_text(text_boom_x, text_boom_y, text=f"{boom_length:.1f}m\n{angle_boom_horizontal_deg:.1f}°", fill="blue", font=("Helvetica", 8), anchor="center", justify="center")


    def update_sling_tension_chart(self, load_weight, num_sling_legs):
        """Actualiza el gráfico de tensión de eslinga vs. ángulo.
        Las unidades de entrada son kg y el gráfico muestra kg.
        """
        angles_h = list(range(10, 90)) # Rango de ángulos horizontales de 10 a 89 grados
        tensions = []

        if num_sling_legs <= 0: 
            # Si no hay patas de eslinga válidas, limpiar el gráfico y ajustar el título
            self.line_tension.set_data([], [])
            self.ax.set_ylim(0, 100 if load_weight == 0 else load_weight * 2) 
            self.ax.set_title(f"Tensión Eslinga (Carga: {load_weight:.0f}kg, Patas: {num_legs}) - Inválido", fontsize=9)
            self.canvas_mpl.draw_idle() 
            return

        for angle_h in angles_h:
            if 0 < angle_h < 90: # Asegurar que el ángulo horizontal es válido para el cálculo
                sling_angle_v = 90 - angle_h # Calcular el ángulo vertical
                cos_angle_v = math.cos(to_radians(sling_angle_v))
                if cos_angle_v != 0:
                    # Fórmula de tensión de eslinga: T = (Peso / Num_Patas) / cos(Ángulo Vertical)
                    tension = (load_weight / num_legs) / cos_angle_v
                    # Limitar la tensión máxima a mostrar para evitar valores extremos con ángulos muy bajos
                    tensions.append(min(tension, load_weight * 10) if math.isfinite(tension) else 0) 
                else:
                    # Si el coseno es cero (ángulo vertical 90, eslinga horizontal), la tensión es teóricamente infinita
                    tensions.append(load_weight * 10) # Representar como un valor muy alto
            else:
                tensions.append(0) # Tensión cero para ángulos no válidos
        
        # Actualizar los datos de la línea en el gráfico
        self.line_tension.set_data(angles_h, tensions)
        
        # Reajustar los límites del eje Y automáticamente
        self.ax.relim()
        self.ax.autoscale_view(scalex=False) 
        
        if tensions: 
            # Encontrar la tensión máxima y mínima válida para ajustar el rango del eje Y
            max_valid_tension = max(t for t in tensions if t is not None and math.isfinite(t) and t > 0) if any(t > 0 for t in tensions if t is not None and math.isfinite(t)) else load_weight
            # min_valid_tension = min(t for t in tensions if t is not None and math.isfinite(t) and t > 0) if any(t > 0 for t in tensions if t is not None and math.isfinite(t)) else 0

            if max_valid_tension > 0 :
                 self.ax.set_ylim(0, max_valid_tension * 1.15) # Añadir un 15% de margen superior
            else: 
                 self.ax.set_ylim(0, load_weight * 1.5 if load_weight > 0 else 100)
        else:
            self.ax.set_ylim(0, load_weight * 1.5 if load_weight > 0 else 100)

        # Actualizar el título del gráfico
        self.ax.set_title(f"Tensión Eslinga (Carga: {load_weight:.0f}kg, Patas: {num_legs})", fontsize=9)
        self.canvas_mpl.draw_idle()


    def create_quiz_section(self):
        """Crea la sección del cuestionario de seguridad en izaje."""
        self.quiz_main_frame = ttk.Frame(self.sections_container, padding="10")
        self.sections["quiz"] = self.quiz_main_frame
        self.display_quiz_content()


    def display_quiz_content(self):
        """Muestra el contenido del cuestionario (inicio, pregunta actual o resultados finales)."""
        # Limpiar el frame del cuestionario antes de mostrar nuevo contenido
        for widget in self.quiz_main_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.quiz_main_frame, text="Cuestionario de Seguridad en Izaje", style="SectionTitle.TLabel").pack(anchor="w", pady=10)

        if not self.quiz_started.get():
            # Mostrar pantalla de inicio del cuestionario o resultados anteriores
            start_quiz_frame = ttk.Frame(self.quiz_main_frame)
            start_quiz_frame.pack(pady=20, expand=True)

            ttk.Label(start_quiz_frame, text="Evalúa tus conocimientos", font=("Helvetica", 14, "bold")).pack(pady=10)
            ttk.Label(start_quiz_frame, text="Ponte a prueba con este cuestionario sobre los principios de izaje seguro.", wraplength=400, justify="center").pack(pady=10)
            
            ttk.Button(start_quiz_frame, text="❓ Iniciar Cuestionario", command=self.start_quiz, style="Quiz.TButton").pack(pady=20)

            if self.quiz_results: # Si ya se ha completado un cuestionario, mostrar los resultados
                results_frame = ttk.Frame(start_quiz_frame, padding="10", relief="groove")
                results_frame.pack(pady=20)
                ttk.Label(results_frame, text="Resultados del Cuestionario:", font=("Helvetica", 12, "bold")).pack()
                ttk.Label(results_frame, textvariable=self.quiz_score_str, font=("Helvetica", 11)).pack(pady=5)
                
                details_text = ""
                for i, q_data in enumerate(self.quiz_questions):
                    is_correct = self.quiz_results.get(i, False)
                    status = "Correcta" if is_correct else f"Incorrecta (Respuesta: {q_data['answer']})"
                    details_text += f"{i+1}. {q_data['question'][:50]}...: {status}\n"
                
                self.quiz_result_details_var.set(details_text.strip())
                ttk.Label(results_frame, textvariable=self.quiz_result_details_var, justify=tk.LEFT, font=("Helvetica", 9)).pack(pady=5)

        else:
            # Mostrar la pregunta actual del cuestionario
            question_frame = ttk.Frame(self.quiz_main_frame)
            question_frame.pack(pady=20, expand=True, fill="x")

            q_idx = self.current_question_index.get()
            question_data = self.quiz_questions[q_idx]

            ttk.Label(question_frame, text=f"Pregunta {q_idx + 1} de {len(self.quiz_questions)}", font=("Helvetica", 10, "italic")).pack()
            self.quiz_question_label_var.set(question_data["question"])
            ttk.Label(question_frame, textvariable=self.quiz_question_label_var, style="QuizQuestion.TLabel").pack(pady=15)

            self.quiz_option_buttons = []
            button_frame = ttk.Frame(question_frame) # Frame para centrar los botones de opción
            button_frame.pack()

            for i, option_text in enumerate(question_data["options"]):
                btn = ttk.Button(button_frame, text=option_text, style="Quiz.TButton",
                                 command=lambda opt=option_text: self.handle_quiz_answer(opt))
                btn.pack(pady=3, padx=5, ipadx=10) 
                self.quiz_option_buttons.append(btn)
            
            self.quiz_feedback_frame = ttk.Frame(question_frame)
            self.quiz_feedback_frame.pack(pady=10)


    def start_quiz(self):
        """Inicia un nuevo cuestionario, reseteando el estado."""
        self.quiz_started.set(True)
        self.current_question_index.set(0)
        self.quiz_results = {}
        self.quiz_score_str.set("Puntuación: 0%")
        self.quiz_result_details_var.set("")
        self.display_quiz_content()

    def handle_quiz_answer(self, selected_option):
        """Maneja la respuesta del usuario a una pregunta del cuestionario."""
        q_idx = self.current_question_index.get()
        question_data = self.quiz_questions[q_idx]
        is_correct = (selected_option == question_data["answer"])
        self.quiz_results[q_idx] = is_correct

        # Deshabilitar botones y mostrar feedback visual
        for btn in self.quiz_option_buttons:
            btn.state(['disabled']) 
            original_text = btn.cget("text")
            if original_text == selected_option: 
                if is_correct:
                    btn.configure(style="Correct.TButton")
                    btn.config(text=f"✔ {original_text}")
                else:
                    btn.configure(style="Incorrect.TButton")
                    btn.config(text=f"✘ {original_text}")
            elif original_text == question_data["answer"]: 
                 btn.configure(style="Correct.TButton") 
                 btn.config(text=f"✔ {original_text}")

        # Mostrar feedback textual (Correcto/Incorrecto)
        for widget in self.quiz_feedback_frame.winfo_children(): 
            widget.destroy()

        if is_correct:
            ttk.Label(self.quiz_feedback_frame, text="¡Correcto!", style="Correct.TLabel").pack()
        else:
            ttk.Label(self.quiz_feedback_frame, text=f"Incorrecto. La respuesta correcta es: {question_data['answer']}", style="Incorrect.TLabel").pack()

        # Botón para la siguiente pregunta o para ver resultados finales
        if q_idx < len(self.quiz_questions) - 1:
            ttk.Button(self.quiz_feedback_frame, text="Siguiente Pregunta →", command=self.next_question, style="Nav.TButton").pack(pady=10)
        else:
            ttk.Button(self.quiz_feedback_frame, text="Ver Resultados Finales", command=self.finish_quiz, style="Nav.TButton").pack(pady=10)


    def next_question(self):
        """Avanza a la siguiente pregunta del cuestionario."""
        self.current_question_index.set(self.current_question_index.get() + 1)
        self.display_quiz_content()

    def finish_quiz(self):
        """Finaliza el cuestionario y calcula la puntuación final."""
        self.quiz_started.set(False)
        correct_answers = sum(1 for res in self.quiz_results.values() if res)
        score_percentage = (correct_answers / len(self.quiz_questions)) * 100 if len(self.quiz_questions) > 0 else 0
        self.quiz_score_str.set(f"Puntuación: {score_percentage:.0f}%")
        self.display_quiz_content() 


if __name__ == '__main__':
    app = LiftingPlanApp()
    app.mainloop()