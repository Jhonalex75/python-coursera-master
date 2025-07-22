import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Helper function to convert degrees to radians
def to_radians(angle):
    return math.radians(angle)

class LiftingPlanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guía de Estudio: Plan de Izaje Seguro")
        self.geometry("1000x750") # Ajustado para mejor visualización inicial

        # --- Estilo ---
        self.style = ttk.Style(self)
        self.style.theme_use('clam') # Un tema moderno
        
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
        self.active_section_name = tk.StringVar(value="standards")
        self.setup_interactive_tool_vars()
        self.setup_quiz_vars()

        # --- Layout Principal ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        header = ttk.Label(main_frame, text="Guía de Estudio: Plan de Izaje Seguro", style="Header.TLabel", anchor="center")
        header.pack(pady=10)
        
        subheader = ttk.Label(main_frame, text="Aprende y analiza los principios de las operaciones de izaje industrial.", style="SubHeader.TLabel", anchor="center")
        subheader.pack(pady=(0,10))

        # --- Navegación ---
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(pady=10)

        buttons_info = [
            ("Estándares", "standards", "📚"),
            ("Elementos del Plan", "plan-elements", "🎓"),
            ("Herramienta Interactiva", "interactive-tool", "⚙️"), # Cambiado el icono
            ("Cuestionario", "quiz", "❓")
        ]

        self.nav_buttons = {}
        for text, section_name, icon in buttons_info:
            btn = ttk.Button(nav_frame, text=f"{icon} {text}", style="Nav.TButton",
                             command=lambda s=section_name: self.show_section(s))
            btn.pack(side=tk.LEFT, padx=5)
            self.nav_buttons[section_name] = btn
        
        # --- Contenedor de Secciones ---
        self.sections_container = ttk.Frame(main_frame)
        self.sections_container.pack(expand=True, fill=tk.BOTH, pady=10)

        self.sections = {}
        self.create_standards_section()
        self.create_plan_elements_section()
        self.create_interactive_tool_section()
        self.create_quiz_section()

        # --- Footer ---
        footer = ttk.Label(main_frame, text="© 2025 Guía de Estudio de Izaje Seguro. Todos los derechos reservados.", font=("Helvetica", 8), anchor="center")
        footer.pack(pady=10, side=tk.BOTTOM)

        self.show_section("standards") # Mostrar sección inicial

    def setup_interactive_tool_vars(self):
        self.load_weight_var = tk.DoubleVar(value=10000)
        self.crane_capacity_var = tk.DoubleVar(value=20000)
        self.boom_length_var = tk.DoubleVar(value=30)
        self.radius_var = tk.DoubleVar(value=15)
        self.sling_angle_horizontal_var = tk.DoubleVar(value=60)
        self.num_sling_legs_var = tk.IntVar(value=2)
        self.outrigger_pad_length_var = tk.DoubleVar(value=1)
        self.outrigger_pad_width_var = tk.DoubleVar(value=1)
        self.ground_bearing_capacity_var = tk.DoubleVar(value=200)
        self.crane_weight_var = tk.DoubleVar(value=15000) # Peso de la grúa para cálculo de estabilizadores
        self.safety_factor_var = tk.DoubleVar(value=1.25) # Factor de seguridad de izaje

        # Variables para resultados
        self.crane_capacity_percentage_str = tk.StringVar(value="0.00%")
        self.is_critical_lift_str = tk.StringVar(value="")
        self.sling_leg_tension_str = tk.StringVar(value="0.00 kg")
        self.pressure_per_outrigger_str = tk.StringVar(value="0.00 kPa")
        self.outrigger_capacity_percentage_str = tk.StringVar(value="0.00%")
        self.derated_crane_capacity_str = tk.StringVar(value="0.00 kg")

        # Registrar callbacks para actualización automática
        for var in [self.load_weight_var, self.crane_capacity_var, self.boom_length_var, 
                    self.radius_var, self.sling_angle_horizontal_var, self.num_sling_legs_var,
                    self.outrigger_pad_length_var, self.outrigger_pad_width_var,
                    self.ground_bearing_capacity_var, self.crane_weight_var, self.safety_factor_var]:
            var.trace_add("write", self.update_interactive_calculations)

    def setup_quiz_vars(self):
        self.quiz_started = tk.BooleanVar(value=False)
        self.current_question_index = tk.IntVar(value=0)
        self.quiz_results = {} # Almacenará {index: is_correct}
        self.quiz_score_str = tk.StringVar(value="Puntuación: 0%")
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
        # Variables para mostrar la pregunta y opciones del quiz
        self.quiz_question_label_var = tk.StringVar()
        self.quiz_options_vars = [tk.StringVar() for _ in range(4)] # Asumiendo max 4 opciones
        self.quiz_feedback_vars = [tk.StringVar() for _ in range(4)]
        self.quiz_result_details_var = tk.StringVar()


    def show_section(self, section_name):
        self.active_section_name.set(section_name)
        for name, frame in self.sections.items():
            if name == section_name:
                frame.pack(expand=True, fill=tk.BOTH)
            else:
                frame.pack_forget()
        
        # Actualizar estilo de botones de navegación
        for name, btn in self.nav_buttons.items():
            if name == section_name:
                btn.state(['pressed']) # Estado presionado para el activo
            else:
                btn.state(['!pressed'])

        # Actualizar cálculos si se muestra la herramienta interactiva
        if section_name == "interactive-tool":
            self.update_interactive_calculations()


    def create_standards_section(self):
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
        frame = ttk.Frame(self.sections_container, padding="10")
        self.sections["plan-elements"] = frame
        
        ttk.Label(frame, text="Elementos de un Plan de Izaje Seguro", style="SectionTitle.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Un plan de izaje seguro implica considerar una serie de temas, problemas y factores.", wraplength=800, justify=tk.LEFT, font=("Helvetica", 10)).pack(anchor="w", pady=(0,10))

        # Contenedor para el acordeón con scrollbar
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

        self.accordion_sections = {} # Para guardar las frames de contenido
        for title, content in sections_data:
            btn = ttk.Button(scrollable_frame, text=f"▼ {title}", style="Accordion.TButton", 
                             command=lambda t=title: self.toggle_accordion_section(t, scrollable_frame))
            btn.pack(fill="x", pady=2)
            
            content_frame = ttk.Frame(scrollable_frame, padding=(20, 5, 5, 5)) # Indent content
            ttk.Label(content_frame, text=content, wraplength=700, justify=tk.LEFT, font=("Helvetica", 9)).pack(anchor="w")
            self.accordion_sections[title] = {"button": btn, "frame": content_frame, "open": False}
            # content_frame se mostrará/ocultará en toggle_accordion_section

        # Riesgos Comunes
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
        section = self.accordion_sections[title]
        if section["open"]:
            section["frame"].pack_forget()
            section["button"].config(text=f"▼ {title}")
            section["open"] = False
        else:
            # Cerrar otras secciones abiertas si se desea comportamiento de acordeón exclusivo
            # for sec_title, sec_data in self.accordion_sections.items():
            #     if sec_title != title and sec_data["open"]:
            #         sec_data["frame"].pack_forget()
            #         sec_data["button"].config(text=f"▼ {sec_title}")
            #         sec_data["open"] = False
            section["frame"].pack(fill="x", after=section["button"])
            section["button"].config(text=f"▲ {title}")
            section["open"] = True
        
        # Forzar la actualización del canvas que contiene el scrollable_frame
        # Esto es crucial para que el scrollbar se ajuste correctamente
        parent_frame.master.update_idletasks() 
        parent_frame.master.configure(scrollregion=parent_frame.master.bbox("all"))


    def create_interactive_tool_section(self):
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

        # Canvas y Scrollbar para inputs
        inputs_canvas = tk.Canvas(inputs_frame_container)
        inputs_scrollbar = ttk.Scrollbar(inputs_frame_container, orient="vertical", command=inputs_canvas.yview)
        inputs_scrollable_frame = ttk.Frame(inputs_canvas)
        inputs_scrollable_frame.bind("<Configure>", lambda e: inputs_canvas.configure(scrollregion=inputs_canvas.bbox("all")))
        inputs_canvas.create_window((0, 0), window=inputs_scrollable_frame, anchor="nw")
        inputs_canvas.configure(yscrollcommand=inputs_scrollbar.set)
        
        inputs_canvas.pack(side="left", fill="both", expand=True)
        inputs_scrollbar.pack(side="right", fill="y")

        input_fields = [
            ("Peso de la Carga (kg):", self.load_weight_var),
            ("Capacidad Nominal Grúa (kg):", self.crane_capacity_var),
            ("Factor de Seguridad Izaje:", self.safety_factor_var), # Nuevo campo
            ("Longitud de la Pluma (m):", self.boom_length_var),
            ("Radio de Operación (m):", self.radius_var),
            ("Ángulo Eslinga (horizontal, °):", self.sling_angle_horizontal_var, (10, 89), "scale"), # (min, max) para scale
            ("Número de Patas de Eslinga:", self.num_sling_legs_var, [1, 2, 3, 4], "combobox"), # Opciones para combobox
            ("Peso de la Grúa (kg):", self.crane_weight_var),
            ("Longitud Zapata Estabilizador (m):", self.outrigger_pad_length_var),
            ("Ancho Zapata Estabilizador (m):", self.outrigger_pad_width_var),
            ("Capacidad Portante Terreno (kPa):", self.ground_bearing_capacity_var),
        ]

        for item in input_fields:
            label_text = item[0]
            var = item[1]
            
            row_frame = ttk.Frame(inputs_scrollable_frame)
            row_frame.pack(fill="x", pady=3)
            ttk.Label(row_frame, text=label_text, style="Input.TLabel").pack(side=tk.LEFT, padx=5, anchor="w")

            if len(item) > 3 and item[3] == "scale":
                min_val, max_val = item[2]
                # Frame para agrupar scale y label de valor
                scale_val_frame = ttk.Frame(row_frame)
                scale_val_frame.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
                scale = ttk.Scale(scale_val_frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL, variable=var, length=120) # Ajustar length
                scale.pack(side=tk.LEFT, fill="x", expand=True)
                ttk.Label(scale_val_frame, textvariable=var, width=5).pack(side=tk.LEFT, padx=(5,0)) # Muestra el valor
            elif len(item) > 3 and item[3] == "combobox":
                options = item[2]
                combo = ttk.Combobox(row_frame, textvariable=var, values=options, state="readonly", width=10)
                combo.pack(side=tk.LEFT, padx=5)
            else:
                entry = ttk.Entry(row_frame, textvariable=var, width=15)
                entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        # --- Columna de Resultados y Visualizaciones ---
        results_viz_frame = ttk.Frame(main_paned_window, padding="10")
        main_paned_window.add(results_viz_frame, weight=2)

        # Resultados del Análisis
        results_frame = ttk.Frame(results_viz_frame, padding="10", relief="groove", borderwidth=2)
        results_frame.pack(fill="x", pady=(0,10)) # results_frame se empaqueta en results_viz_frame

        # Usar grid para todos los hijos de results_frame
        results_title_label = ttk.Label(results_frame, text="Resultados del Análisis", style="SubHeader.TLabel")
        results_title_label.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew") # Span y sticky para centrar si es necesario

        ttk.Label(results_frame, text="Capacidad Derateada Grúa:", style="Result.TLabel").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.derated_cap_label = ttk.Label(results_frame, textvariable=self.derated_crane_capacity_str, style="Result.TLabel")
        self.derated_cap_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(results_frame, text="% Capacidad Grúa Utilizada (sobre derateada):", style="Result.TLabel").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.cap_perc_label = ttk.Label(results_frame, textvariable=self.crane_capacity_percentage_str) 
        self.cap_perc_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        self.critical_lift_label = ttk.Label(results_frame, textvariable=self.is_critical_lift_str)
        self.critical_lift_label.grid(row=2, column=2, sticky="w", padx=5, pady=2)

        ttk.Label(results_frame, text="Tensión por Pata de Eslinga:", style="Result.TLabel").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(results_frame, textvariable=self.sling_leg_tension_str, style="Result.TLabel").grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(results_frame, text="Presión por Estabilizador:", style="Result.TLabel").grid(row=4, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(results_frame, textvariable=self.pressure_per_outrigger_str, style="Result.TLabel").grid(row=4, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(results_frame, text="% Capacidad Portante Terreno Utilizada:", style="Result.TLabel").grid(row=5, column=0, sticky="w", padx=5, pady=2)
        self.outrigger_perc_label = ttk.Label(results_frame, textvariable=self.outrigger_capacity_percentage_str) 
        self.outrigger_perc_label.grid(row=5, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(results_frame, text="Nota: Asegúrese de que las eslingas y accesorios tengan un WLL adecuado con su propio factor de seguridad.", font=("Helvetica", 8, "italic")).grid(row=6, column=0, columnspan=3, sticky="w", padx=5, pady=(10,5))

        # Configurar columnconfigure para que la columna 1 (valores) se expanda si hay espacio
        results_frame.columnconfigure(1, weight=1)


        # Visualización de Grúa (Canvas)
        viz_frame = ttk.Frame(results_viz_frame, padding="10", relief="groove", borderwidth=2)
        viz_frame.pack(fill="x", pady=10) # viz_frame se empaqueta en results_viz_frame
        ttk.Label(viz_frame, text="Posición de la Grúa y la Carga (Simplificado)", style="SubHeader.TLabel").pack()
        self.crane_canvas = tk.Canvas(viz_frame, width=380, height=230, bg="white")
        self.crane_canvas.pack(pady=5)
        ttk.Label(viz_frame, text="*El ángulo de pluma se calcula para que la punta esté sobre la carga al radio dado.", font=("Helvetica", 8, "italic")).pack()

        # Gráfico de Tensión de Eslinga (Matplotlib)
        chart_frame = ttk.Frame(results_viz_frame, padding="10", relief="groove", borderwidth=2)
        chart_frame.pack(fill="both", expand=True, pady=10) # chart_frame se empaqueta en results_viz_frame
        ttk.Label(chart_frame, text="Tensión de Eslinga vs. Ángulo", style="SubHeader.TLabel").pack()
        
        self.fig, self.ax = plt.subplots(figsize=(5, 3.5)) 
        self.fig.subplots_adjust(bottom=0.2, left=0.25, right=0.95, top=0.9) # Ajustar márgenes
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

        self.update_interactive_calculations() 

    def update_interactive_calculations(self, *args):
        try:
            load_w = self.load_weight_var.get()
            crane_cap = self.crane_capacity_var.get()
            boom_l = self.boom_length_var.get()
            rad = self.radius_var.get()
            sling_angle_h = self.sling_angle_horizontal_var.get()
            num_legs = self.num_sling_legs_var.get()
            pad_l = self.outrigger_pad_length_var.get()
            pad_w = self.outrigger_pad_width_var.get()
            ground_cap = self.ground_bearing_capacity_var.get()
            crane_w = self.crane_weight_var.get()
            safety_f = self.safety_factor_var.get()

            if safety_f <= 0: safety_f = 1.0 

            derated_crane_capacity = crane_cap / safety_f if crane_cap > 0 and safety_f > 0 else 0
            self.derated_crane_capacity_str.set(f"{derated_crane_capacity:.2f} kg")

            crane_cap_perc = (load_w / derated_crane_capacity) * 100 if derated_crane_capacity > 0 else float('inf')
            self.crane_capacity_percentage_str.set(f"{crane_cap_perc:.2f}%")
            
            is_critical = crane_cap_perc > 75
            self.is_critical_lift_str.set("(¡Izaje Crítico!)" if is_critical else "(Izaje No Crítico)")
            self.cap_perc_label.configure(style="Critical.TLabel" if is_critical else "Safe.TLabel")
            self.critical_lift_label.configure(style="Critical.TLabel" if is_critical else "Safe.TLabel")


            sling_leg_tension = 0
            if num_legs > 0 and 0 < sling_angle_h < 90:
                sling_angle_v = 90 - sling_angle_h 
                cos_val = math.cos(to_radians(sling_angle_v))
                if cos_val != 0: 
                    sling_leg_tension = (load_w / num_legs) / cos_val
            self.sling_leg_tension_str.set(f"{sling_leg_tension:.2f} kg")

            outrigger_pad_area = pad_l * pad_w
            total_outrigger_load_N = (load_w + crane_w) * 9.81 
            pressure_per_outrigger_kPa = (total_outrigger_load_N / 4) / (outrigger_pad_area * 1000) if outrigger_pad_area > 0 else 0
            self.pressure_per_outrigger_str.set(f"{pressure_per_outrigger_kPa:.2f} kPa")

            outrigger_cap_perc = (pressure_per_outrigger_kPa / ground_cap) * 100 if ground_cap > 0 else float('inf')
            self.outrigger_capacity_percentage_str.set(f"{outrigger_cap_perc:.2f}%")
            if outrigger_cap_perc > 100:
                 self.outrigger_perc_label.configure(style="Critical.TLabel")
            elif outrigger_cap_perc > 80: 
                 self.outrigger_perc_label.configure(style="Warning.TLabel")
            else:
                 self.outrigger_perc_label.configure(style="Safe.TLabel")


            self.draw_crane_visualization(boom_l, rad)
            self.update_sling_tension_chart(load_w, num_legs)

        except tk.TclError: # Puede ocurrir si las variables no están listas al inicio
            pass # Los callbacks se ejecutarán de nuevo cuando los valores cambien
        except Exception as e:
            # print(f"Error en cálculos: {e}") 
            pass
            
    def draw_crane_visualization(self, boom_length, radius):
        # Asegurarse que el canvas está listo para dibujar
        self.crane_canvas.update_idletasks() 
        canvas = self.crane_canvas
        canvas.delete("all")
        
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w <=1 or h <=1: 
            self.after(50, lambda: self.draw_crane_visualization(boom_length, radius)) 
            return

        ground_level = h - 20
        crane_base_x = w * 0.25 # Ajustado para más espacio
        crane_base_y = ground_level
        
        canvas.create_line(0, ground_level, w, ground_level, fill="black", width=2)
        canvas.create_rectangle(crane_base_x - 15, ground_level - 20, crane_base_x + 15, ground_level, fill="gray", outline="black")

        if boom_length <= 0 or radius <= 0:
            canvas.create_text(w/2, h/2, text="Longitud de pluma y radio\ndeben ser > 0", fill="red", justify="center", font=("Helvetica", 9))
            return
        if radius > boom_length:
            canvas.create_text(w/2, h/2, text="Radio no puede ser mayor\nque Longitud Pluma", fill="red", justify="center", font=("Helvetica", 9))
            return

        try:
            # Ángulo de la pluma con la vertical (desde el pivote de la grúa)
            angle_boom_vertical_rad = math.acos(radius / boom_length)
        except ValueError: 
             canvas.create_text(w/2, h/2, text="Error cálculo ángulo (Radio > Pluma)", fill="red", justify="center", font=("Helvetica", 9))
             return

        angle_boom_horizontal_rad = math.pi/2 - angle_boom_vertical_rad
        angle_boom_horizontal_deg = math.degrees(angle_boom_horizontal_rad)

        # Escala: hacer que la longitud de la pluma sea una fracción del ancho disponible
        # El ancho disponible para la pluma y el radio es (w - crane_base_x - padding)
        drawing_width_available = w - crane_base_x - 20 # 20 for padding on right
        
        # Si la pluma es muy larga, escalar para que quepa. Si es corta, usar una escala razonable.
        # Queremos que boom_length * cos(angle_boom_horizontal_rad) (proyección horizontal) + radio_offset (si es diferente) quepan
        # La proyección horizontal de la pluma es 'radius' por definición de cómo lo estamos dibujando.
        
        scale_factor = drawing_width_available / (boom_length * 1.2) # Un poco de margen
        if radius * scale_factor > drawing_width_available * 0.8 : # Si el radio se vuelve muy grande
            scale_factor = (drawing_width_available * 0.8) / radius


        boom_viz_length = boom_length * scale_factor
        radius_viz = radius * scale_factor
        
        # Pivote de la pluma un poco más arriba de la base de la grúa
        boom_pivot_x = crane_base_x
        boom_pivot_y = crane_base_y - 10

        boom_end_x = boom_pivot_x + boom_viz_length * math.cos(angle_boom_horizontal_rad)
        boom_end_y = boom_pivot_y - boom_viz_length * math.sin(angle_boom_horizontal_rad)

        canvas.create_line(boom_pivot_x, boom_pivot_y, boom_end_x, boom_end_y, fill="blue", width=5, capstyle=tk.ROUND)

        # Carga (directamente debajo de la punta de la pluma al radio dado)
        load_hook_x = boom_pivot_x + radius_viz # Posición horizontal de la carga
        load_hook_y = boom_end_y # La carga cuelga de la punta de la pluma (verticalmente)
        
        # Asegurar que la línea de carga sea vertical desde la punta de la pluma hasta la carga
        # La punta de la pluma está en (boom_end_x, boom_end_y)
        # La carga está horizontalmente en load_hook_x
        # Para que la línea de carga sea vertical, la carga debe estar en (boom_end_x, alguna_y_debajo)
        # Pero la definición del problema es que la carga está a 'radius' del centro de giro.
        # La punta de la pluma debe estar sobre la carga.
        # Entonces, boom_end_x debe ser igual a load_hook_x.
        
        # Si la pluma se dibuja con su ángulo real, y la carga está en 'radius', la línea de carga será vertical.
        # La visualización actual ya lo hace: boom_end_x es crane_base_x + boom_length * cos(angle_horizontal)
        # Y radius es boom_length * cos(angle_horizontal), así que boom_end_x = crane_base_x + radius_viz.

        canvas.create_line(boom_end_x, boom_end_y, boom_end_x, boom_end_y + 15, fill="black", width=1.5) # Cable corto
        canvas.create_rectangle(boom_end_x - 10, boom_end_y + 15, boom_end_x + 10, boom_end_y + 35, fill="orange", outline="black") # Carga

        # Línea y texto para el Radio
        canvas.create_line(boom_pivot_x, ground_level, boom_end_x, ground_level, fill="red", arrow=tk.BOTH, width=1.5)
        canvas.create_text(boom_pivot_x + (boom_end_x - boom_pivot_x)/2, ground_level - 10, text=f"Radio: {radius:.1f}m", fill="black", font=("Helvetica", 8), anchor="s")
        
        # Texto para Longitud y Ángulo de Pluma
        # Colocar texto cerca del punto medio de la pluma, ligeramente desplazado
        text_boom_x = boom_pivot_x + (boom_viz_length/2) * math.cos(angle_boom_horizontal_rad) + 5 * math.sin(angle_boom_horizontal_rad)
        text_boom_y = boom_pivot_y - (boom_viz_length/2) * math.sin(angle_boom_horizontal_rad) - 5 * math.cos(angle_boom_horizontal_rad)
        canvas.create_text(text_boom_x, text_boom_y, text=f"{boom_length:.1f}m\n{angle_boom_horizontal_deg:.1f}°", fill="blue", font=("Helvetica", 8), anchor="center", justify="center")


    def update_sling_tension_chart(self, load_weight, num_sling_legs):
        angles_h = list(range(10, 90)) 
        tensions = []

        if num_sling_legs <= 0: 
            self.line_tension.set_data([], [])
            self.ax.set_ylim(0, 100 if load_weight == 0 else load_weight * 2) # Ajustar Y si no hay patas
            self.ax.set_title(f"Tensión Eslinga (Carga: {load_weight:.0f}kg, Patas: {num_legs}) - Inválido", fontsize=9)
            self.canvas_mpl.draw_idle() # Usar draw_idle para mejor rendimiento
            return

        for angle_h in angles_h:
            if 0 < angle_h < 90: # Ángulo horizontal válido
                angle_v = 90 - angle_h 
                cos_val = math.cos(to_radians(angle_v))
                if cos_val != 0: 
                    tension = (load_weight / num_legs) / cos_val
                    # Limitar la tensión máxima a mostrar para evitar gráficos extremos con ángulos muy bajos
                    tensions.append(min(tension, load_weight * 10) if math.isfinite(tension) else 0) 
                else:
                    tensions.append(load_weight * 10) # Tensión muy alta si el coseno es cero (ángulo vertical 90)
            else:
                tensions.append(0)
        
        self.line_tension.set_data(angles_h, tensions)
        
        self.ax.relim()
        self.ax.autoscale_view(scalex=False) # Solo autoescala Y
        
        if tensions: 
            max_valid_tension = max(t for t in tensions if t is not None and math.isfinite(t) and t > 0) if any(t > 0 for t in tensions if t is not None and math.isfinite(t)) else load_weight
            min_valid_tension = min(t for t in tensions if t is not None and math.isfinite(t) and t > 0) if any(t > 0 for t in tensions if t is not None and math.isfinite(t)) else 0

            if max_valid_tension > 0 :
                 self.ax.set_ylim(0, max_valid_tension * 1.15) # Un poco más de margen superior
            else: # Si todas las tensiones son 0 o inválidas
                 self.ax.set_ylim(0, load_weight * 1.5 if load_weight > 0 else 100)
        else:
            self.ax.set_ylim(0, load_weight * 1.5 if load_weight > 0 else 100)

        self.ax.set_title(f"Tensión Eslinga (Carga: {load_weight:.0f}kg, Patas: {num_legs})", fontsize=9)
        self.canvas_mpl.draw_idle()


    def create_quiz_section(self):
        self.quiz_main_frame = ttk.Frame(self.sections_container, padding="10")
        self.sections["quiz"] = self.quiz_main_frame
        self.display_quiz_content()


    def display_quiz_content(self):
        for widget in self.quiz_main_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.quiz_main_frame, text="Cuestionario de Seguridad en Izaje", style="SectionTitle.TLabel").pack(anchor="w", pady=10)

        if not self.quiz_started.get():
            start_quiz_frame = ttk.Frame(self.quiz_main_frame)
            start_quiz_frame.pack(pady=20, expand=True)

            ttk.Label(start_quiz_frame, text="Evalúa tus conocimientos", font=("Helvetica", 14, "bold")).pack(pady=10)
            ttk.Label(start_quiz_frame, text="Ponte a prueba con este cuestionario sobre los principios de izaje seguro.", wraplength=400, justify="center").pack(pady=10)
            
            ttk.Button(start_quiz_frame, text="❓ Iniciar Cuestionario", command=self.start_quiz, style="Quiz.TButton").pack(pady=20)

            if self.quiz_results: 
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
            question_frame = ttk.Frame(self.quiz_main_frame)
            question_frame.pack(pady=20, expand=True, fill="x")

            q_idx = self.current_question_index.get()
            question_data = self.quiz_questions[q_idx]

            ttk.Label(question_frame, text=f"Pregunta {q_idx + 1} de {len(self.quiz_questions)}", font=("Helvetica", 10, "italic")).pack()
            self.quiz_question_label_var.set(question_data["question"])
            ttk.Label(question_frame, textvariable=self.quiz_question_label_var, style="QuizQuestion.TLabel").pack(pady=15)

            self.quiz_option_buttons = []
            button_frame = ttk.Frame(question_frame) # Frame para centrar botones
            button_frame.pack()

            for i, option_text in enumerate(question_data["options"]):
                btn = ttk.Button(button_frame, text=option_text, style="Quiz.TButton",
                                 command=lambda opt=option_text: self.handle_quiz_answer(opt))
                btn.pack(pady=3, padx=5, ipadx=10) # Usar pack para botones de opción
                self.quiz_option_buttons.append(btn)
            
            self.quiz_feedback_frame = ttk.Frame(question_frame)
            self.quiz_feedback_frame.pack(pady=10)


    def start_quiz(self):
        self.quiz_started.set(True)
        self.current_question_index.set(0)
        self.quiz_results = {}
        self.quiz_score_str.set("Puntuación: 0%")
        self.quiz_result_details_var.set("")
        self.display_quiz_content()

    def handle_quiz_answer(self, selected_option):
        q_idx = self.current_question_index.get()
        question_data = self.quiz_questions[q_idx]
        is_correct = (selected_option == question_data["answer"])
        self.quiz_results[q_idx] = is_correct

        for btn in self.quiz_option_buttons:
            btn.state(['disabled']) # Deshabilitar todos
            original_text = btn.cget("text")
            if original_text == selected_option: # Opción seleccionada por el usuario
                if is_correct:
                    btn.configure(style="Correct.TButton")
                    btn.config(text=f"✔ {original_text}")
                else:
                    btn.configure(style="Incorrect.TButton")
                    btn.config(text=f"✘ {original_text}")
            elif original_text == question_data["answer"]: # Si esta es la respuesta correcta (y no fue la seleccionada)
                 btn.configure(style="Correct.TButton") # Resaltar la correcta
                 btn.config(text=f"✔ {original_text}")


        for widget in self.quiz_feedback_frame.winfo_children(): 
            widget.destroy()

        if is_correct:
            ttk.Label(self.quiz_feedback_frame, text="¡Correcto!", style="Correct.TLabel").pack()
        else:
            ttk.Label(self.quiz_feedback_frame, text=f"Incorrecto. La respuesta correcta es: {question_data['answer']}", style="Incorrect.TLabel").pack()

        if q_idx < len(self.quiz_questions) - 1:
            ttk.Button(self.quiz_feedback_frame, text="Siguiente Pregunta →", command=self.next_question, style="Nav.TButton").pack(pady=10)
        else:
            ttk.Button(self.quiz_feedback_frame, text="Ver Resultados Finales", command=self.finish_quiz, style="Nav.TButton").pack(pady=10)


    def next_question(self):
        self.current_question_index.set(self.current_question_index.get() + 1)
        self.display_quiz_content()

    def finish_quiz(self):
        self.quiz_started.set(False)
        correct_answers = sum(1 for res in self.quiz_results.values() if res)
        score_percentage = (correct_answers / len(self.quiz_questions)) * 100 if len(self.quiz_questions) > 0 else 0
        self.quiz_score_str.set(f"Puntuación: {score_percentage:.0f}%")
        self.display_quiz_content() 


if __name__ == '__main__':
    app = LiftingPlanApp()
    app.mainloop()