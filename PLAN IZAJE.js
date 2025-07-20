import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ChevronDownIcon, ChevronUpIcon, BookOpenIcon, CalculatorIcon, QuestionMarkCircleIcon, AcademicCapIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

// Helper function to convert degrees to radians
const toRadians = (angle) => angle * (Math.PI / 180);

const App = () => {
  const [activeSection, setActiveSection] = useState('standards'); // 'standards', 'plan-elements', 'interactive-tool', 'quiz'
  const [quizStarted, setQuizStarted] = useState(false);
  const [quizResults, setQuizResults] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  // State for Interactive Tool
  const [loadWeight, setLoadWeight] = useState(10000); // kg
  const [craneCapacity, setCraneCapacity] = useState(20000); // kg
  const [boomLength, setBoomLength] = useState(30); // meters
  const [radius, setRadius] = useState(15); // meters
  const [slingAngleHorizontal, setSlingAngleHorizontal] = useState(60); // degrees from horizontal
  const [numSlingLegs, setNumSlingLegs] = useState(2); // Number of sling legs
  const [outriggerPadLength, setOutriggerPadLength] = useState(1); // meters
  const [outriggerPadWidth, setOutriggerPadWidth] = useState(1); // meters
  const [groundBearingCapacity, setGroundBearingCapacity] = useState(200); // kPa (kN/m^2)
  const [craneWeight, setCraneWeight] = useState(15000); // kg (assumed for outrigger calc)

  // Calculations for Interactive Tool
  const craneCapacityPercentage = ((loadWeight / craneCapacity) * 100).toFixed(2);
  const isCriticalLift = parseFloat(craneCapacityPercentage) > 75;

  let slingLegTension = 0;
  let slingAngleVertical = 0;
  if (numSlingLegs > 0 && slingAngleHorizontal > 0 && slingAngleHorizontal < 90) {
    slingAngleVertical = 90 - slingAngleHorizontal; // Angle with vertical
    slingLegTension = (loadWeight / numSlingLegs) / Math.cos(toRadians(slingAngleVertical));
  }

  const outriggerPadArea = outriggerPadLength * outriggerPadWidth; // m^2
  // Assuming total load on outriggers is loadWeight + craneWeight, distributed evenly among 4 outriggers
  const totalOutriggerLoad = (loadWeight + craneWeight) * 9.81; // Convert kg to Newtons (approx)
  const pressurePerOutrigger = outriggerPadArea > 0 ? (totalOutriggerLoad / 4) / (outriggerPadArea * 1000) : 0; // kPa

  const outriggerCapacityPercentage = groundBearingCapacity > 0 ? (pressurePerOutrigger / groundBearingCapacity) * 100 : 0;


  // Data for Sling Tension Chart
  const slingTensionChartData = Array.from({ length: 80 }, (_, i) => {
    const angle = i + 10; // Angles from 10 to 89 degrees
    const angleVertical = 90 - angle;
    const tension = (loadWeight / numSlingLegs) / Math.cos(toRadians(angleVertical));
    return { angle, tension: isFinite(tension) ? tension : 0 };
  });

  // Quiz Questions
  const quizQuestions = [
    {
      question: "¿Qué norma ASME B30 cubre las Grúas Móviles y Locomotoras?",
      options: ["ASME B30.9", "ASME B30.5", "ASME B30.10", "ASME B30.26"],
      answer: "ASME B30.5"
    },
    {
      question: "¿Cuál es el factor clave para determinar si un izaje es 'crítico' según la capacidad de la grúa?",
      options: ["Más del 50% de la capacidad", "Más del 75% de la capacidad", "Más del 90% de la capacidad", "Cualquier izaje con más de 10 toneladas"],
      answer: "Más del 75% de la capacidad"
    },
    {
      question: "¿Qué tipo de inspección de eslingas debe realizarse 'antes de cada turno/uso intensivo'?",
      options: ["Inicial", "Periódica", "Frecuente", "Anual"],
      answer: "Frecuente"
    },
    {
      question: "¿Cuál es la velocidad máxima de viento generalmente aceptable para las operaciones de grúa?",
      options: ["20 km/hr", "30 km/hr", "40 km/hr", "50 km/hr"],
      answer: "40 km/hr"
    },
    {
      question: "Si una eslinga tiene un ángulo de estrangulación menor a 120 grados, ¿cómo afecta esto su capacidad nominal?",
      options: ["Aumenta la capacidad", "No tiene efecto", "Reduce la capacidad", "Depende del material de la eslinga"],
      answer: "Reduce la capacidad"
    }
  ];

  const handleQuizStart = () => {
    setQuizStarted(true);
    setQuizResults(null);
    setCurrentQuestionIndex(0);
  };

  const handleAnswer = (selectedOption) => {
    const currentQuestion = quizQuestions[currentQuestionIndex];
    const isCorrect = selectedOption === currentQuestion.answer;

    setQuizResults(prev => ({
      ...prev,
      [currentQuestionIndex]: isCorrect
    }));

    if (currentQuestionIndex < quizQuestions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      // Quiz finished
      setQuizStarted(false);
    }
  };

  const scoreQuiz = () => {
    if (!quizResults) return 0;
    const correctAnswers = Object.values(quizResults).filter(Boolean).length;
    return (correctAnswers / quizQuestions.length) * 100;
  };

  const QuizDisplay = () => {
    if (!quizStarted) {
      return (
        <div className="text-center p-6 bg-gray-100 rounded-lg shadow-inner">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4">Evalúa tus conocimientos</h3>
          <p className="text-gray-700 mb-6">Ponte a prueba con este cuestionario sobre los principios de izaje seguro.</p>
          <button
            onClick={handleQuizStart}
            className="px-6 py-3 bg-blue-600 text-white font-bold rounded-lg shadow-md hover:bg-blue-700 transition duration-300 ease-in-out flex items-center justify-center mx-auto"
          >
            <QuestionMarkCircleIcon className="h-5 w-5 mr-2" /> Iniciar Cuestionario
          </button>
          {quizResults && (
            <div className="mt-8 p-4 bg-white rounded-lg shadow-md">
              <h4 className="text-xl font-semibold text-gray-800 mb-2">Resultados del Cuestionario:</h4>
              <p className="text-lg text-gray-700">Puntuación: <span className="font-bold text-blue-600">{scoreQuiz().toFixed(0)}%</span></p>
              <ul className="mt-4 text-left">
                {quizQuestions.map((q, i) => (
                  <li key={i} className="mb-2">
                    <span className="font-medium">{i + 1}. {q.question}</span>
                    <br />
                    Tu respuesta: <span className={`${quizResults[i] ? 'text-green-600' : 'text-red-600'} font-bold`}>
                      {quizResults[i] ? 'Correcta' : `Incorrecta (Respuesta correcta: ${q.answer})`}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      );
    }

    const currentQuestion = quizQuestions[currentQuestionIndex];
    const hasAnswered = quizResults && quizResults.hasOwnProperty(currentQuestionIndex);

    return (
      <div className="p-6 bg-white rounded-lg shadow-lg">
        <h3 className="text-2xl font-semibold text-gray-800 mb-6">Pregunta {currentQuestionIndex + 1} de {quizQuestions.length}</h3>
        <p className="text-xl text-gray-700 mb-8">{currentQuestion.question}</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {currentQuestion.options.map((option, index) => (
            <button
              key={index}
              onClick={() => handleAnswer(option)}
              disabled={hasAnswered}
              className={`
                p-4 border rounded-lg text-lg font-medium transition duration-300 ease-in-out
                ${hasAnswered
                  ? (option === currentQuestion.answer
                    ? 'bg-green-100 border-green-500 text-green-800'
                    : (option === (quizResults[currentQuestionIndex] ? currentQuestion.answer : '')) // If answered incorrectly, highlight selected if it was wrong
                      ? 'bg-red-100 border-red-500 text-red-800'
                      : 'bg-gray-50 border-gray-300 text-gray-600 cursor-not-allowed')
                  : 'bg-blue-50 hover:bg-blue-100 border-blue-300 text-blue-700 hover:border-blue-500'
                }
                ${hasAnswered && option === currentQuestion.answer ? 'font-bold' : ''}
              `}
            >
              {option}
              {hasAnswered && option === currentQuestion.answer && <CheckCircleIcon className="h-5 w-5 inline-block ml-2 text-green-600" />}
              {hasAnswered && !quizResults[currentQuestionIndex] && option === currentQuestion.options[currentQuestion.options.indexOf(quizResults[currentQuestionIndex])] && <XCircleIcon className="h-5 w-5 inline-block ml-2 text-red-600" />}
            </button>
          ))}
        </div>
        {hasAnswered && currentQuestionIndex < quizQuestions.length - 1 && (
          <div className="mt-8 text-center">
            <button
              onClick={() => setCurrentQuestionIndex(prev => prev + 1)}
              className="px-6 py-3 bg-blue-600 text-white font-bold rounded-lg shadow-md hover:bg-blue-700 transition duration-300 ease-in-out"
            >
              Siguiente Pregunta
            </button>
          </div>
        )}
        {hasAnswered && currentQuestionIndex === quizQuestions.length - 1 && (
          <div className="mt-8 text-center">
            <button
              onClick={() => setQuizStarted(false)}
              className="px-6 py-3 bg-green-600 text-white font-bold rounded-lg shadow-md hover:bg-green-700 transition duration-300 ease-in-out"
            >
              Ver Resultados Finales
            </button>
          </div>
        )}
      </div>
    );
  };


  const StandardsSection = () => (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold text-gray-900 mb-6">Estándares Clave de Izaje</h2>
      <p className="text-gray-700 mb-8">
        Las normas de la serie ASME B30 y las regulaciones de OSHA son fundamentales para la seguridad en las operaciones de izaje. Aunque voluntarias, son guías desarrolladas por expertos para prevenir lesiones y asegurar un entorno de trabajo seguro.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-blue-50 p-5 rounded-lg border border-blue-200">
          <h3 className="text-xl font-semibold text-blue-800 mb-3">Normas ASME B30</h3>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li><span className="font-medium">ASME B30.5:</span> Grúas Móviles y Locomotoras</li>
            <li><span className="font-medium">ASME B30.9:</span> Eslingas</li>
            <li><span className="font-medium">ASME B30.10:</span> Ganchos</li>
            <li><span className="font-medium">ASME B30.26:</span> Herrajes de Aparejo</li>
            <li><span className="font-medium">ASME B30.23:</span> Sistemas de Elevación de Personal (en casos excepcionales)</li>
          </ul>
          <p className="text-sm text-blue-700 mt-4">
            Estas normas son revisadas y modificadas periódicamente para mantenerse actualizadas con las mejores prácticas.
          </p>
        </div>

        <div className="bg-green-50 p-5 rounded-lg border border-green-200">
          <h3 className="text-xl font-semibold text-green-800 mb-3">Regulaciones OSHA</h3>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li><span className="font-medium">29 CFR 1910.184:</span> Eslingas</li>
            <li><span className="font-medium">29 CFR 1926.550:</span> Grúas, Torres, Enganches, Elevadores y Transportadores</li>
          </ul>
          <p className="text-sm text-green-700 mt-4">
            Las regulaciones de OSHA son obligatorias y establecen requisitos mínimos de seguridad para proteger a los trabajadores.
          </p>
        </div>
      </div>

      <div className="mt-8 p-6 bg-yellow-50 rounded-lg border border-yellow-200">
        <h3 className="text-xl font-semibold text-yellow-800 mb-3">Importancia de las Normas</h3>
        <p className="text-gray-700">
          Estas normas son cruciales para prevenir o minimizar lesiones al guiar a fabricantes, propietarios, empleadores y operarios en la implementación de prácticas seguras. Aseguran que el equipo sea diseñado, fabricado, operado y mantenido de manera que se garantice la seguridad pública y en el lugar de trabajo.
        </p>
      </div>
    </div>
  );

  const PlanElementsSection = () => {
    const [openSection, setOpenSection] = useState(null);

    const toggleSection = (section) => {
      setOpenSection(openSection === section ? null : section);
    };

    const sections = [
      {
        id: 'load-assessment',
        title: '1. Evaluación de la Carga',
        content: (
          <>
            <p>Determinar el peso y el centro de gravedad (CG) de la carga es el primer paso crítico. Un cálculo preciso de la masa es fundamental para seleccionar el equipo adecuado y evitar sobrecargas.</p>
            <h4 className="font-semibold mt-4 mb-2">Ejemplo de Cálculo de Masa:</h4>
            <p>Para objetos con forma regular, la masa se puede calcular multiplicando el volumen por la densidad del material. Para objetos irregulares, puede ser necesario consultar planos o usar básculas.</p>
          </>
        )
      },
      {
        id: 'equipment-selection',
        title: '2. Selección del Equipo',
        content: (
          <>
            <p>Elegir la grúa y los accesorios de izaje adecuados es vital. Se debe considerar el tipo, tamaño y peso de la carga, el tipo de enganche y el entorno de operación. El equipo debe tener la capacidad para izar la carga más pesada en el radio requerido.</p>
            <h4 className="font-semibold mt-4 mb-2">Factores a Considerar:</h4>
            <ul className="list-disc list-inside ml-4">
              <li>Capacidad nominal de la grúa.</li>
              <li>Longitud y ángulo de la pluma.</li>
              <li>Tipo y capacidad de las eslingas (cadena, cable, sintéticas).</li>
              <li>Tipo y capacidad de los grilletes, ganchos y otros herrajes de aparejo.</li>
              <li>Condiciones del terreno y espacio disponible.</li>
            </ul>
          </>
        )
      },
      {
        id: 'equipment-inspection',
        title: '3. Inspección de Equipos y Accesorios',
        content: (
          <>
            <p>Las inspecciones regulares son esenciales para garantizar la seguridad del equipo y los accesorios de izaje.</p>
            <h4 className="font-semibold mt-4 mb-2">Tipos de Inspección:</h4>
            <ul className="list-disc list-inside ml-4">
              <li><span className="font-medium">Inicial:</span> A la recepción del equipo o accesorio.</li>
              <li><span className="font-medium">Frecuente:</span> Antes de cada turno o uso intensivo.</li>
              <li><span className="font-medium">Periódica:</span> Realizada por una persona designada y calificada, con una frecuencia establecida (ej. anualmente).</li>
            </ul>
            <h4 className="font-semibold mt-4 mb-2">Puntos de Inspección Comunes:</h4>
            <ul className="list-disc list-inside ml-4">
              <li><span className="font-medium">Grúas:</span> Controles, sistema hidráulico, frenos, pluma, cables, ganchos, estabilizadores, dispositivos de seguridad.</li>
              <li><span className="font-medium">Eslingas:</span> Etiqueta ilegible, cortes, nudos, quemaduras, daños por aplastamiento o corrosión.</li>
              <li><span className="font-medium">Grilletes y Otros Accesorios:</span> Deformaciones, grietas, desgaste excesivo, pasadores doblados o dañados.</li>
            </ul>
          </>
        )
      },
      {
        id: 'work-area-conditions',
        title: '4. Condiciones del Área de Trabajo',
        content: (
          <>
            <p>El entorno de trabajo juega un papel crucial en la seguridad del izaje.</p>
            <h4 className="font-semibold mt-4 mb-2">Factores a Evaluar:</h4>
            <ul className="list-disc list-inside ml-4">
              <li><span className="font-medium">Estabilidad del Terreno:</span> Asegurar que el suelo pueda soportar el peso de la grúa y la carga, especialmente la presión portante en los estabilizadores.</li>
              <li><span className="font-medium">Condiciones Ambientales:</span> Monitorear la velocidad del viento (generalmente no debe superar los 40 km/hr para grúas), lluvia, hielo, visibilidad.</li>
              <li><span className="font-medium">Delimitación y Señalización:</span> Asegurar que el área de izaje esté claramente delimitada y señalizada para evitar el acceso de personal no autorizado.</li>
              <li><span className="font-medium">Obstáculos:</span> Identificar y eliminar cualquier obstáculo aéreo o terrestre (líneas eléctricas, tuberías, edificios).</li>
            </ul>
            <h4 className="font-semibold mt-4 mb-2">Cálculo de Presión Portante en Estabilizadores:</h4>
            <p>La presión sobre el terreno se calcula dividiendo la carga total sobre el estabilizador por el área de la zapata del estabilizador. Esto debe ser menor que la capacidad portante del suelo.</p>
          </>
        )
      },
      {
        id: 'lifting-configuration',
        title: '5. Configuración del Izaje',
        content: (
          <>
            <p>La planificación de la posición de la grúa y la carga es esencial para un izaje seguro y eficiente.</p>
            <h4 className="font-semibold mt-4 mb-2">Aspectos Clave:</h4>
            <ul className="list-disc list-inside ml-4">
              <li><span className="font-medium">Posición Inicial y Final:</span> Definir dónde comenzará y terminará la carga.</li>
              <li><span className="font-medium">Radio de Operación:</span> La distancia horizontal desde el centro de rotación de la grúa hasta el centro de la carga.</li>
              <li><span className="font-medium">Ángulo de la Pluma:</span> El ángulo de la pluma con respecto a la horizontal.</li>
              <li><span className="font-medium">Longitud de la Pluma:</span> La extensión total de la pluma.</li>
              <li><span className="font-medium">Tablas de Carga:</span> Consultar las tablas de carga de la grúa para asegurar que la capacidad nominal no se exceda en ninguna configuración.</li>
            </ul>
          </>
        )
      },
      {
        id: 'critical-calculations',
        title: '6. Cálculos Críticos',
        content: (
          <>
            <p>Los cálculos matemáticos son una parte integral de la planificación segura del izaje.</p>
            <h4 className="font-semibold mt-4 mb-2">Ejemplos de Cálculos:</h4>
            <ul className="list-disc list-inside ml-4">
              <li><span className="font-medium">Carga en las Patas de la Eslinga:</span> La tensión en cada pata de una eslinga aumenta a medida que el ángulo de la eslinga con la vertical se hace más grande (o el ángulo con la horizontal se hace más pequeño). Se usa trigonometría (coseno) para calcular esto.</li>
              <li><span className="font-medium">Reducción de Capacidad en Estrangulación:</span> La capacidad nominal de una eslinga se reduce cuando se utiliza en un enganche de estrangulación con un ángulo menor a 120 grados.</li>
              <li><span className="font-medium">Teorema de Pitágoras y Trigonometría:</span> Fundamentales para determinar distancias, alturas y ángulos en la configuración del izaje.</li>
            </ul>
          </>
        )
      },
      {
        id: 'communication-signals',
        title: '7. Comunicación y Señales',
        content: (
          <>
            <p>Una comunicación clara y efectiva es vital para la seguridad de la operación.</p>
            <h4 className="font-semibold mt-4 mb-2">Aspectos Clave:</h4>
            <ul className="list-disc list-inside ml-4">
              <li><span className="font-medium">Señales Manuales Estandarizadas:</span> Utilizar las señales manuales de grúa según ASME B30.5.</li>
              <li><span className="font-medium">Comunicación Radial:</span> Si la distancia o visibilidad lo requieren, usar radios para la comunicación entre el operador, el rigger y el personal involucrado.</li>
              <li><span className="font-medium">Un Único Señalero:</span> Designar a una sola persona como señalero principal para evitar confusiones.</li>
            </ul>
          </>
        )
      },
      {
        id: 'qualified-personnel',
        title: '8. Personal Calificado',
        content: (
          <>
            <p>Todo el personal involucrado en las operaciones de izaje debe estar debidamente capacitado y certificado.</p>
            <h4 className="font-semibold mt-4 mb-2">Roles Clave:</h4>
            <ul className="list-disc list-inside ml-4">
              <li><span className="font-medium">Operador de Grúa:</span> Responsable de la operación segura de la grúa.</li>
              <li><span className="font-medium">Rigger/Aparejador:</span> Responsable de la selección, inspección y enganche adecuado de la carga.</li>
              <li><span className="font-medium">Señalero:</span> Responsable de guiar al operador de la grúa de forma segura.</li>
            </ul>
            <h4 className="font-semibold mt-4 mb-2">Contenidos de Capacitación:</h4>
            <p>Funcionamiento de grúas, elementos de izaje, señales, tablas de carga, riesgos, y procedimientos de emergencia.</p>
            <p className="mt-2 text-sm text-blue-700">
              Es importante diferenciar entre "certificación" (otorgada por un organismo reconocido) y "licencia" (permiso legal para operar).
            </p>
          </>
        )
      },
    ];

    return (
      <div className="p-6 bg-white rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">Elementos de un Plan de Izaje Seguro</h2>
        <p className="text-gray-700 mb-8">
          Un plan de izaje seguro implica considerar una serie de temas, problemas y factores para garantizar la seguridad de la operación.
        </p>

        <div className="space-y-4">
          {sections.map((section) => (
            <div key={section.id} className="border border-gray-200 rounded-lg overflow-hidden">
              <button
                className="w-full flex justify-between items-center p-4 bg-gray-50 hover:bg-gray-100 transition duration-200 ease-in-out text-left text-xl font-semibold text-gray-800"
                onClick={() => toggleSection(section.id)}
              >
                {section.title}
                {openSection === section.id ? <ChevronUpIcon className="h-6 w-6 text-blue-600" /> : <ChevronDownIcon className="h-6 w-6 text-blue-600" />}
              </button>
              {openSection === section.id && (
                <div className="p-4 bg-white text-gray-700 border-t border-gray-200">
                  {section.content}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-8 p-6 bg-red-50 rounded-lg border border-red-200">
          <h3 className="text-xl font-semibold text-red-800 mb-3">Riesgos Comunes a Evitar (Casos de Estudio)</h3>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>Uso de equipo no estándar o defectuoso.</li>
            <li>Sobrecarga de la grúa o los accesorios.</li>
            <li>Terreno inestable o preparación inadecuada del sitio.</li>
            <li>Falta de delimitación y señalización del área de trabajo.</li>
            <li>Comunicación deficiente o falta de señaleros/riggers calificados.</li>
            <li>Accesorios de izaje defectuosos o dañados.</li>
            <li>Falta de capacitación en cálculos de izaje y lectura de tablas de carga.</li>
          </ul>
          <p className="text-sm text-red-700 mt-4">
            Un plan de izaje seguro aborda proactivamente estos riesgos para garantizar una operación exitosa.
          </p>
        </div>
      </div>
    );
  };

  const InteractiveToolSection = () => (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-3xl font-bold text-gray-900 mb-6">Análisis Interactivo de Plan de Izaje</h2>
      <p className="text-gray-700 mb-8">
        Ingresa los parámetros del izaje para visualizar los cálculos críticos y el impacto en la seguridad.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Parameters */}
        <div className="bg-gray-50 p-6 rounded-lg shadow-inner">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">Parámetros del Izaje</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="loadWeight">
                Peso de la Carga (kg)
              </label>
              <input
                type="number"
                id="loadWeight"
                value={loadWeight}
                onChange={(e) => setLoadWeight(parseFloat(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="craneCapacity">
                Capacidad Nominal de la Grúa (kg)
              </label>
              <input
                type="number"
                id="craneCapacity"
                value={craneCapacity}
                onChange={(e) => setCraneCapacity(parseFloat(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="boomLength">
                Longitud de la Pluma (metros)
              </label>
              <input
                type="number"
                id="boomLength"
                value={boomLength}
                onChange={(e) => setBoomLength(parseFloat(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="radius">
                Radio de Operación (metros)
              </label>
              <input
                type="number"
                id="radius"
                value={radius}
                onChange={(e) => setRadius(parseFloat(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="slingAngleHorizontal">
                Ángulo de Eslinga (con la horizontal, grados)
              </label>
              <input
                type="range"
                id="slingAngleHorizontal"
                min="10"
                max="89"
                value={slingAngleHorizontal}
                onChange={(e) => setSlingAngleHorizontal(parseFloat(e.target.value))}
                className="w-full h-2 bg-blue-100 rounded-lg appearance-none cursor-pointer"
              />
              <span className="text-sm text-gray-600">{slingAngleHorizontal}°</span>
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="numSlingLegs">
                Número de Patas de Eslinga
              </label>
              <select
                id="numSlingLegs"
                value={numSlingLegs}
                onChange={(e) => setNumSlingLegs(parseInt(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value={1}>1 (Vertical)</option>
                <option value={2}>2</option>
                <option value={3}>3</option>
                <option value={4}>4</option>
              </select>
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="outriggerPadLength">
                Longitud Zapata Estabilizador (metros)
              </label>
              <input
                type="number"
                id="outriggerPadLength"
                value={outriggerPadLength}
                onChange={(e) => setOutriggerPadLength(parseFloat(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="outriggerPadWidth">
                Ancho Zapata Estabilizador (metros)
              </label>
              <input
                type="number"
                id="outriggerPadWidth"
                value={outriggerPadWidth}
                onChange={(e) => setOutriggerPadWidth(parseFloat(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="groundBearingCapacity">
                Capacidad Portante del Terreno (kPa)
              </label>
              <input
                type="number"
                id="groundBearingCapacity"
                value={groundBearingCapacity}
                onChange={(e) => setGroundBearingCapacity(parseFloat(e.target.value))}
                className="shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Results and Visualizations */}
        <div className="space-y-8">
          <div className="bg-blue-50 p-6 rounded-lg shadow-inner border border-blue-200">
            <h3 className="text-xl font-semibold text-blue-800 mb-4">Resultados del Análisis</h3>
            <p className="text-lg text-gray-700 mb-2">
              Porcentaje de Capacidad de Grúa Utilizada: <span className={`font-bold ${isCriticalLift ? 'text-red-600' : 'text-green-600'}`}>{craneCapacityPercentage}%</span>
              {isCriticalLift && <span className="ml-2 text-red-600 font-semibold">(¡Izaje Crítico!)</span>}
            </p>
            <p className="text-lg text-gray-700 mb-2">
              Tensión por Pata de Eslinga: <span className="font-bold text-blue-600">{slingLegTension.toFixed(2)} kg</span>
            </p>
            <p className="text-lg text-gray-700 mb-2">
              Presión por Estabilizador: <span className="font-bold text-blue-600">{pressurePerOutrigger.toFixed(2)} kPa</span>
            </p>
            <p className="text-lg text-gray-700">
              Porcentaje de Capacidad Portante del Terreno Utilizada: <span className={`font-bold ${outriggerCapacityPercentage > 90 ? 'text-red-600' : outriggerCapacityPercentage > 70 ? 'text-orange-600' : 'text-green-600'}`}>{outriggerCapacityPercentage.toFixed(2)}%</span>
              {outriggerCapacityPercentage > 90 && <span className="ml-2 text-red-600 font-semibold">(¡Excede capacidad!)</span>}
            </p>
          </div>

          {/* Crane Position Visualization */}
          <div className="bg-purple-50 p-6 rounded-lg shadow-inner border border-purple-200">
            <h3 className="text-xl font-semibold text-purple-800 mb-4">Posición de la Grúa y la Carga</h3>
            <div className="relative w-full h-64 bg-white rounded-lg overflow-hidden flex items-end justify-center">
              <svg width="100%" height="100%" viewBox="0 0 400 250" preserveAspectRatio="xMidYMax meet">
                {/* Ground */}
                <line x1="0" y1="240" x2="400" y2="240" stroke="#333" strokeWidth="2" />
                {/* Crane Base */}
                <rect x="180" y="220" width="40" height="20" fill="#666" rx="5" ry="5" />
                {/* Outriggers (simplified) */}
                <rect x="160" y="235" width="10" height="10" fill="#999" rx="2" ry="2" />
                <rect x="230" y="235" width="10" height="10" fill="#999" rx="2" ry="2" />

                {/* Boom */}
                {/* Calculate boom end coordinates */}
                {(() => {
                  const boomStartX = 200;
                  const boomStartY = 220;
                  const boomEndAngle = 90 - (Math.acos(radius / boomLength) * 180 / Math.PI); // Calculate boom angle from horizontal based on radius and length
                  const actualBoomAngle = isNaN(boomEndAngle) || boomEndAngle < 0 ? 0 : boomEndAngle; // Ensure valid angle

                  const boomEndX = boomStartX + boomLength * 5 * Math.cos(toRadians(actualBoomAngle)); // Scale for visualization
                  const boomEndY = boomStartY - boomLength * 5 * Math.sin(toRadians(actualBoomAngle)); // Scale for visualization

                  // Clamp boomEndX to stay within bounds if radius is too large for boomLength
                  const clampedBoomEndX = Math.min(Math.max(boomStartX - radius * 5, 0), 400);
                  const clampedBoomEndY = Math.min(Math.max(boomStartY - boomLength * 5, 0), 240);


                  return (
                    <>
                      <line
                        x1={boomStartX}
                        y1={boomStartY}
                        x2={boomStartX + radius * 5} // Simple horizontal representation of radius
                        y2={boomStartY - (boomLength * 5 * Math.sin(toRadians(actualBoomAngle)))} // Vertical height
                        stroke="#007bff"
                        strokeWidth="4"
                        strokeLinecap="round"
                        transform={`rotate(${-actualBoomAngle} ${boomStartX} ${boomStartY})`} // Rotate around boom base
                      />
                       <line
                        x1={boomStartX}
                        y1={boomStartY}
                        x2={boomStartX + boomLength * 5 * Math.cos(toRadians(actualBoomAngle))}
                        y2={boomStartY - boomLength * 5 * Math.sin(toRadians(actualBoomAngle))}
                        stroke="#007bff"
                        strokeWidth="4"
                        strokeLinecap="round"
                      />
                      {/* Load */}
                      <rect
                        x={boomStartX + radius * 5 - 15} // Position load at end of radius
                        y={boomStartY - (boomLength * 5 * Math.sin(toRadians(actualBoomAngle))) + 10} // Position load below boom end
                        width="30"
                        height="30"
                        fill="#ffc107"
                        stroke="#e0a800"
                        strokeWidth="2"
                        rx="5" ry="5"
                      />
                       {/* Text for Radius and Boom Angle */}
                      <text x={boomStartX + radius * 2.5} y={boomStartY - 5} fontSize="12" fill="#333" textAnchor="middle">
                        Radio: {radius}m
                      </text>
                      <text x={boomStartX + boomLength * 2.5 * Math.cos(toRadians(actualBoomAngle))} y={boomStartY - boomLength * 2.5 * Math.sin(toRadians(actualBoomAngle)) - 10} fontSize="12" fill="#333" textAnchor="middle">
                        Pluma: {boomLength}m ({actualBoomAngle.toFixed(1)}°)
                      </text>
                    </>
                  );
                })()}
              </svg>
            </div>
            <p className="text-sm text-gray-600 mt-4">
              *Visualización simplificada. El ángulo de la pluma se calcula en base al radio y la longitud de la pluma.
            </p>
          </div>

          {/* Sling Tension Chart */}
          <div className="bg-yellow-50 p-6 rounded-lg shadow-inner border border-yellow-200">
            <h3 className="text-xl font-semibold text-yellow-800 mb-4">Tensión de Eslinga vs. Ángulo</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={slingTensionChartData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="angle" label={{ value: 'Ángulo (horizontal, grados)', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Tensión por Pata (kg)', angle: -90, position: 'insideLeft' }} />
                <Tooltip formatter={(value) => `${value.toFixed(2)} kg`} labelFormatter={(label) => `Ángulo: ${label}°`} />
                <Legend />
                <Line type="monotone" dataKey="tension" stroke="#8884d8" name="Tensión de Eslinga" dot={false} />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-sm text-gray-600 mt-4">
              Este gráfico muestra cómo la tensión en cada pata de la eslinga aumenta a medida que el ángulo con la horizontal disminuye (se vuelve más "plano"). Un ángulo más bajo significa mayor tensión.
            </p>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 font-sans text-gray-900 p-4 sm:p-8">
      <header className="text-center mb-10">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-blue-800 leading-tight">
          Guía de Estudio: Plan de Izaje Seguro
        </h1>
        <p className="text-xl text-blue-600 mt-3">
          Aprende y analiza los principios de las operaciones de izaje industrial.
        </p>
      </header>

      <nav className="mb-8 bg-white p-3 rounded-lg shadow-md flex flex-wrap justify-center gap-3">
        <button
          onClick={() => setActiveSection('standards')}
          className={`px-5 py-2 rounded-lg font-medium text-lg transition duration-300 ease-in-out flex items-center
            ${activeSection === 'standards' ? 'bg-blue-600 text-white shadow-lg' : 'bg-gray-200 text-gray-700 hover:bg-blue-100 hover:text-blue-700'}`}
        >
          <BookOpenIcon className="h-5 w-5 mr-2" /> Estándares
        </button>
        <button
          onClick={() => setActiveSection('plan-elements')}
          className={`px-5 py-2 rounded-lg font-medium text-lg transition duration-300 ease-in-out flex items-center
            ${activeSection === 'plan-elements' ? 'bg-blue-600 text-white shadow-lg' : 'bg-gray-200 text-gray-700 hover:bg-blue-100 hover:text-blue-700'}`}
        >
          <AcademicCapIcon className="h-5 w-5 mr-2" /> Elementos del Plan
        </button>
        <button
          onClick={() => setActiveSection('interactive-tool')}
          className={`px-5 py-2 rounded-lg font-medium text-lg transition duration-300 ease-in-out flex items-center
            ${activeSection === 'interactive-tool' ? 'bg-blue-600 text-white shadow-lg' : 'bg-gray-200 text-gray-700 hover:bg-blue-100 hover:text-blue-700'}`}
        >
          <CalculatorIcon className="h-5 w-5 mr-2" /> Herramienta Interactiva
        </button>
        <button
          onClick={() => setActiveSection('quiz')}
          className={`px-5 py-2 rounded-lg font-medium text-lg transition duration-300 ease-in-out flex items-center
            ${activeSection === 'quiz' ? 'bg-blue-600 text-white shadow-lg' : 'bg-gray-200 text-gray-700 hover:bg-blue-100 hover:text-blue-700'}`}
        >
          <QuestionMarkCircleIcon className="h-5 w-5 mr-2" /> Cuestionario
        </button>
      </nav>

      <main className="max-w-6xl mx-auto">
        {activeSection === 'standards' && <StandardsSection />}
        {activeSection === 'plan-elements' && <PlanElementsSection />}
        {activeSection === 'interactive-tool' && <InteractiveToolSection />}
        {activeSection === 'quiz' && <QuizDisplay />}
      </main>

      <footer className="text-center text-gray-600 mt-12 text-sm">
        <p>&copy; 2025 Guía de Estudio de Izaje Seguro. Todos los derechos reservados.</p>
      </footer>
    </div>
  );
};

export default App;
