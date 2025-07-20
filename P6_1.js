import React, { useState, useEffect, useCallback, createContext, useContext } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from 'firebase/auth';
import { getFirestore, doc, setDoc, getDoc, collection, addDoc, getDocs, query, where, onSnapshot, updateDoc, deleteDoc, writeBatch } from 'firebase/firestore';
import { ChevronDown, ChevronRight, PlusCircle, Edit2, Trash2, Briefcase, Layers, ListChecks, CalendarDays, DollarSign, BarChart3, AlertTriangle, Settings, Eye, ThumbsUp, ThumbsDown, Play, Save, FolderOpen, FileText, Users, GanttChartSquare, TrendingUp, AlertCircle, CheckCircle, Info, ExternalLink } from 'lucide-react';

// Configuración de Firebase
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {
  apiKey: "YOUR_API_KEY", 
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Inicializar Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

const appId = typeof __app_id !== 'undefined' ? __app_id : 'p6-simulator-default-v4'; // Updated appId for Gantt version

// Contexto de la Aplicación
const AppContext = createContext();

// --- Funciones de Ayuda para Fechas ---
const addDaysToDate = (dateString, days) => {
  if (!dateString) return '';
  const date = new Date(dateString + 'T00:00:00Z'); // Usar Z para UTC y evitar problemas de zona horaria
  if (isNaN(date.getTime())) return '';
  date.setUTCDate(date.getUTCDate() + days);
  return date.toISOString().split('T')[0];
};

const dateToEpochDays = (dateString) => {
    if (!dateString) return 0;
    const date = new Date(dateString + 'T00:00:00Z');
    if (isNaN(date.getTime())) return 0;
    return Math.floor(date.getTime() / (1000 * 60 * 60 * 24));
};

const dateDiffInDays = (dateStr1, dateStr2) => {
    if (!dateStr1 || !dateStr2) return 0;
    return Math.abs(dateToEpochDays(dateStr1) - dateToEpochDays(dateStr2));
};

const maxDate = (dates) => {
    const validDates = dates.filter(d => d && !isNaN(new Date(d + 'T00:00:00Z').getTime())).map(d => new Date(d + 'T00:00:00Z'));
    if (validDates.length === 0) return null;
    return new Date(Math.max.apply(null, validDates)).toISOString().split('T')[0];
};

const minDate = (dates) => {
    const validDates = dates.filter(d => d && !isNaN(new Date(d + 'T00:00:00Z').getTime())).map(d => new Date(d + 'T00:00:00Z'));
    if (validDates.length === 0) return null;
    return new Date(Math.min.apply(null, validDates)).toISOString().split('T')[0];
};

const formatCurrency = (value) => {
    const number = Number(value);
    if (isNaN(number)) return '$0.00';
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(number);
};


// Componente Principal App
function App() {
  const [userId, setUserId] = useState(null);
  const [isAuthReady, setIsAuthReady] = useState(false);
  const [currentView, setCurrentView] = useState('home');
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [selectedProject, setSelectedProject] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        setUserId(user.uid);
      } else {
        try {
          if (typeof __initial_auth_token !== 'undefined' && __initial_auth_token) {
            await signInWithCustomToken(auth, __initial_auth_token);
          } else {
            await signInAnonymously(auth);
          }
        } catch (e) { console.error("Error en autenticación:", e); setError("Error de autenticación."); }
      }
      setIsAuthReady(true);
    });
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    if (isAuthReady && userId) {
      setIsLoading(true);
      const projectsColPath = `artifacts/${appId}/users/${userId}/p6_projects`;
      const q = query(collection(db, projectsColPath));
      const unsubscribe = onSnapshot(q, (querySnapshot) => {
        const projectsData = [];
        querySnapshot.forEach((doc) => { projectsData.push({ id: doc.id, ...doc.data() }); });
        setProjects(projectsData.sort((a,b) => new Date(b.createdAt || 0) - new Date(a.createdAt || 0) ));
        setIsLoading(false);
      }, (err) => { console.error("Error cargando proyectos:", err); setError("No se pudieron cargar los proyectos."); setIsLoading(false); });
      return () => unsubscribe();
    }
  }, [isAuthReady, userId]);

  useEffect(() => {
    if (selectedProjectId && userId) {
      setIsLoading(true);
      const projectDocPath = `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`;
      const unsubscribe = onSnapshot(doc(db, projectDocPath), (docSnap) => {
        if (docSnap.exists()) { setSelectedProject({ id: docSnap.id, ...docSnap.data() }); }
        else { setSelectedProject(null); setSelectedProjectId(null); }
        setIsLoading(false);
      }, (err) => { console.error("Error cargando proyecto:", err); setError("No se pudo cargar el proyecto."); setIsLoading(false); });
      return () => unsubscribe();
    } else { setSelectedProject(null); }
  }, [selectedProjectId, userId]);

  const handleCreateNewProject = async (projectName, projectStartDate) => {
    if (!projectName.trim() || !projectStartDate) { setError("Nombre y fecha de inicio son obligatorios."); return; }
    if (!userId) { setError("Usuario no autenticado."); return; }
    setIsLoading(true); setError(null);
    const newProject = {
      name: projectName, startDate: projectStartDate, createdAt: new Date().toISOString(),
      wbs: [{ id: `wbs-root-${crypto.randomUUID()}`, name: projectName, parentId: null, path: '0' }],
      activities: [], resources: [],
      costs: { budgetedTotalCost: 0, actualTotalCost: 0 },
      risks: [], baselines: [], dataDate: projectStartDate,
    };
    try {
      const projectsColPath = `artifacts/${appId}/users/${userId}/p6_projects`;
      const docRef = await addDoc(collection(db, projectsColPath), newProject);
      setSelectedProjectId(docRef.id); setShowNewProjectModal(false); setCurrentView('projectSetup');
    } catch (e) { console.error("Error creando proyecto:", e); setError("Error al crear el proyecto."); }
    finally { setIsLoading(false); }
  };

  const handleSelectProject = (projectId) => { setSelectedProjectId(projectId); setCurrentView('projectSetup'); };
  
  const contextValue = { userId, appId, selectedProjectId, selectedProject, isLoading, setIsLoading, error, setError, db, setCurrentView };

  if (!isAuthReady) return <LoadingSpinner message="Inicializando autenticación..." />;
  if (isLoading && !selectedProject && !projects.length && currentView !== 'home') return <LoadingSpinner message="Cargando datos..." />;

  return (
    <AppContext.Provider value={contextValue}>
      <div className="flex flex-col h-screen font-inter bg-gray-100 text-gray-800">
        <Header />
        <div className="flex flex-1 overflow-hidden">
          <Sidebar currentView={currentView} setCurrentView={setCurrentView} projectSelected={!!selectedProjectId} />
          <main className="flex-1 p-4 md:p-6 overflow-y-auto bg-white shadow-inner m-1 md:m-2 rounded-lg">
            {error && <Notification type="error" message={error} onClose={() => setError(null)} />}
            {currentView === 'home' && <Home projects={projects} onSelectProject={handleSelectProject} onShowNewProjectModal={() => setShowNewProjectModal(true)} isLoading={isLoading && projects.length === 0} />}
            {selectedProjectId && selectedProject && (
              <>
                {currentView === 'projectSetup' && <ProjectSetup />}
                {currentView === 'wbs' && <WBSEditor />}
                {currentView === 'activities' && <ActivityEditor />}
                {currentView === 'schedule' && <SchedulingView />}
                {currentView === 'costs' && <CostsView />} 
                {(['resources', 'baselines', 'progress', 'reports', 'risks', 'layouts'].includes(currentView)) && <PlaceholderView viewName={currentView} />}
              </>
            )}
            {!selectedProjectId && currentView !== 'home' && (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <FolderOpen size={50} className="text-gray-400 mb-4" />
                <p className="text-xl text-gray-600">Por favor, selecciona o crea un proyecto.</p>
                <button onClick={() => setCurrentView('home')} className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Ir a Inicio</button>
              </div>
            )}
          </main>
        </div>
        {showNewProjectModal && <NewProjectModal onClose={() => setShowNewProjectModal(false)} onCreate={handleCreateNewProject} />}
      </div>
    </AppContext.Provider>
  );
}

// --- Componentes de UI y Vistas (Header, Sidebar, Home, Modals, ProjectSetup, WBSEditor sin cambios funcionales mayores) ---
const Header = () => { /* Sin cambios */
  const { userId } = useContext(AppContext);
  return (
    <header className="bg-gray-800 text-white p-3 md:p-4 flex justify-between items-center shadow-md print:hidden">
      <div className="flex items-center space-x-2">
        <GanttChartSquare size={28} className="text-blue-400"/>
        <h1 className="text-xl md:text-2xl font-semibold">Simulador P6 Básico</h1>
      </div>
      {userId && <div className="text-xs bg-gray-700 px-2 py-1 rounded">UID: ...{userId.slice(-6)}</div>}
    </header>
  );
};

const Sidebar = ({ currentView, setCurrentView, projectSelected }) => { /* Sin cambios */
  const navItems = [
    { id: 'home', label: 'Inicio', icon: FolderOpen, requiresProject: false },
    { id: 'projectSetup', label: 'Proyecto', icon: Settings, requiresProject: true },
    { id: 'wbs', label: 'EDT (WBS)', icon: Layers, requiresProject: true },
    { id: 'activities', label: 'Actividades', icon: ListChecks, requiresProject: true },
    { id: 'schedule', label: 'Programación', icon: CalendarDays, requiresProject: true },
    { id: 'costs', label: 'Costos', icon: DollarSign, requiresProject: true },
    { id: 'resources', label: 'Recursos', icon: Users, requiresProject: true, soon: true },
    { id: 'baselines', label: 'Líneas Base', icon: ThumbsUp, requiresProject: true, soon: true },
    { id: 'progress', label: 'Avance', icon: TrendingUp, requiresProject: true, soon: true },
    { id: 'reports', label: 'Informes', icon: BarChart3, requiresProject: true, soon: true },
    { id: 'risks', label: 'Riesgos', icon: AlertTriangle, requiresProject: true, soon: true },
  ];

  return (
    <aside className="w-20 md:w-64 bg-gray-700 text-gray-200 p-2 md:p-4 space-y-1 md:space-y-2 overflow-y-auto print:hidden">
      {navItems.map(item => (
        <button
          key={item.id}
          title={item.label}
          onClick={() => {
            if (!item.requiresProject || projectSelected) {
              setCurrentView(item.id);
            } else {
              alert("Por favor, selecciona o crea un proyecto primero.");
            }
          }}
          disabled={(item.requiresProject && !projectSelected) || item.soon}
          className={`w-full flex items-center space-x-0 md:space-x-3 p-2 md:p-2.5 rounded-md text-left
            ${currentView === item.id ? 'bg-blue-600 text-white shadow-md' : 'hover:bg-gray-600'}
            ${(item.requiresProject && !projectSelected) || item.soon ? 'opacity-50 cursor-not-allowed' : ''}
          `}
        >
          <item.icon size={20} className="flex-shrink-0" />
          <span className="hidden md:inline truncate">{item.label}</span>
          {item.soon && <span className="hidden md:inline ml-auto text-xs bg-yellow-500 text-yellow-900 px-1.5 py-0.5 rounded">Pronto</span>}
        </button>
      ))}
    </aside>
  );
};

const Home = ({ projects, onSelectProject, onShowNewProjectModal, isLoading }) => { /* Sin cambios */
 return (
  <div className="p-2">
    <div className="flex justify-between items-center mb-4">
      <h2 className="text-xl md:text-2xl font-semibold text-gray-700">Mis Proyectos</h2>
      <button
        onClick={onShowNewProjectModal}
        className="px-3 py-1.5 md:px-4 md:py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors flex items-center space-x-2 text-sm md:text-base"
      >
        <PlusCircle size={18} />
        <span>Nuevo Proyecto</span>
      </button>
    </div>
    {isLoading && <LoadingSpinner message="Cargando proyectos..." />}
    {!isLoading && projects.length === 0 && (
      <div className="text-center py-10">
        <Briefcase size={48} className="mx-auto text-gray-400 mb-3" />
        <p className="text-gray-500">No hay proyectos aún. ¡Crea uno para comenzar!</p>
      </div>
    )}
    {!isLoading && projects.length > 0 && (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map(project => (
          <div key={project.id} 
              className="p-4 bg-white border border-gray-200 rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer flex flex-col justify-between"
              onClick={() => onSelectProject(project.id)}>
            <div>
              <h3 className="text-md font-medium text-blue-600 truncate" title={project.name}>{project.name}</h3>
              <p className="text-xs text-gray-500 mt-1">Inicio: {new Date(project.startDate + 'T00:00:00Z').toLocaleDateString()}</p>
              <p className="text-xs text-gray-400">ID: ...{project.id.slice(-6)}</p>
            </div>
            <div className="mt-3 text-right">
                <ExternalLink size={16} className="text-blue-500 inline-block"/>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);
};

const NewProjectModal = ({ onClose, onCreate }) => { /* Sin cambios */
  const [projectName, setProjectName] = useState('');
  const [projectStartDate, setProjectStartDate] = useState(new Date().toISOString().split('T')[0]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onCreate(projectName, projectStartDate);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50 print:hidden">
      <div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 className="text-lg md:text-xl font-semibold mb-4 text-gray-800">Crear Nuevo Proyecto</h3>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label htmlFor="projectName" className="block text-sm font-medium text-gray-700 mb-1">Nombre del Proyecto</label>
            <input type="text" id="projectName" value={projectName} onChange={(e) => setProjectName(e.target.value)} className="w-full input-style" required />
          </div>
          <div className="mb-5">
            <label htmlFor="projectStartDate" className="block text-sm font-medium text-gray-700 mb-1">Fecha de Inicio</label>
            <input type="date" id="projectStartDate" value={projectStartDate} onChange={(e) => setProjectStartDate(e.target.value)} className="w-full input-style" required />
          </div>
          <div className="flex justify-end space-x-3">
            <button type="button" onClick={onClose} className="px-4 py-2 btn-secondary text-sm">Cancelar</button>
            <button type="submit" className="px-4 py-2 btn-primary text-sm">Crear Proyecto</button>
          </div>
        </form>
      </div>
    </div>
  );
};

const ProjectSetup = () => { /* Sin cambios */
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setError, setCurrentView } = useContext(AppContext);
  const [projectName, setProjectName] = useState('');
  const [projectStartDate, setProjectStartDate] = useState('');
  const [dataDate, setDataDate] = useState('');

  useEffect(() => {
    if (selectedProject) {
      setProjectName(selectedProject.name || '');
      setProjectStartDate(selectedProject.startDate ? selectedProject.startDate.split('T')[0] : '');
      setDataDate(selectedProject.dataDate ? selectedProject.dataDate.split('T')[0] : (selectedProject.startDate ? selectedProject.startDate.split('T')[0] : ''));
    }
  }, [selectedProject]);

  const handleSaveChanges = async () => {
    if (!selectedProjectId || !userId) { setError("Error: Proyecto/Usuario no válido."); return; }
    if (!projectName.trim() || !projectStartDate || !dataDate) { setError("Nombre, Fecha de Inicio y Data Date son obligatorios."); return; }
    setIsLoading(true);
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    try {
      await updateDoc(projectDocRef, { name: projectName, startDate: projectStartDate, dataDate: dataDate });
      setError(null); alert("Cambios guardados.");
    } catch (e) { console.error("Error guardando proyecto:", e); setError("Error al guardar cambios."); }
    finally { setIsLoading(false); }
  };

  const handleDeleteProject = async () => {
    if (!selectedProjectId || !userId) { setError("No hay proyecto para eliminar."); return; }
    if (!window.confirm(`¿Eliminar "${selectedProject?.name}" permanentemente?`)) return;
    setIsLoading(true);
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    try {
      await deleteDoc(projectDocRef); setError(null); alert("Proyecto eliminado."); setCurrentView('home');
    } catch (e) { console.error("Error eliminando proyecto:", e); setError("Error al eliminar proyecto."); }
    finally { setIsLoading(false); }
  };
  
  if (!selectedProject) return <LoadingSpinner message="Cargando config. proyecto..." />;

  return (
    <div className="p-1 md:p-4">
      <h2 className="text-xl md:text-2xl font-semibold mb-5 text-gray-800 border-b pb-2">Configuración: {selectedProject.name}</h2>
      <div className="space-y-4 max-w-md">
        <div><label htmlFor="setupProjectName" className="lbl">Nombre Proyecto</label><input type="text" id="setupProjectName" value={projectName} onChange={(e) => setProjectName(e.target.value)} className="w-full input-style"/></div>
        <div><label htmlFor="setupProjectStartDate" className="lbl">Fecha Inicio</label><input type="date" id="setupProjectStartDate" value={projectStartDate} onChange={(e) => setProjectStartDate(e.target.value)} className="w-full input-style"/></div>
        <div><label htmlFor="setupDataDate" className="lbl">Data Date</label><input type="date" id="setupDataDate" value={dataDate} onChange={(e) => setDataDate(e.target.value)} className="w-full input-style"/></div>
        <button onClick={handleSaveChanges} className="btn-primary px-4 py-2 text-sm flex items-center space-x-2"><Save size={18} /> <span>Guardar</span></button>
        <div className="mt-8 pt-4 border-t">
            <h3 className="text-md font-semibold text-red-600 mb-2">Zona de Peligro</h3>
            <button onClick={handleDeleteProject} className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm flex items-center space-x-2"><Trash2 size={18} /> <span>Eliminar Proyecto</span></button>
            <p className="text-xs text-gray-500 mt-1">Esta acción es irreversible.</p>
        </div>
      </div>
    </div>
  );
};

const WBSEditor = () => { /* Sin cambios */
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setError } = useContext(AppContext);
  const [wbsItems, setWbsItems] = useState([]);
  const [showAddWBSModal, setShowAddWBSModal] = useState(false);
  const [editingWBS, setEditingWBS] = useState(null);
  const [newWBSName, setNewWBSName] = useState('');
  const [selectedParentWBS, setSelectedParentWBS] = useState(null);

  useEffect(() => {
    if (selectedProject && selectedProject.wbs) {
      const sortedWBS = [...selectedProject.wbs].sort((a, b) => (a.path && b.path) ? a.path.localeCompare(b.path, undefined, { numeric: true, sensitivity: 'base' }) : 0);
      setWbsItems(sortedWBS);
    } else { setWbsItems([]); }
  }, [selectedProject]);

  const getWBSPath = (parentId, currentWbsItems) => {
    if (!parentId) { const rootItems = currentWbsItems.filter(w => !w.parentId); return String(rootItems.length); }
    const parent = currentWbsItems.find(w => w.id === parentId);
    if (!parent || typeof parent.path === 'undefined') { console.warn("Parent WBS path not found:", parentId); const siblings = currentWbsItems.filter(w => w.parentId === parentId); return `errPath.${siblings.length}`; }
    const siblings = currentWbsItems.filter(w => w.parentId === parentId); return `${parent.path}.${siblings.length}`;
  };

  const handleAddOrUpdateWBS = async () => {
    if (!newWBSName.trim()) { setError("Nombre EDT obligatorio."); return; }
    if (!selectedProjectId || !userId) { setError("Error: Proyecto/Usuario no válido."); return; }
    setIsLoading(true);
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    let updatedWBSItems = editingWBS ? wbsItems.map(w => w.id === editingWBS.id ? { ...w, name: newWBSName } : w)
      : [...wbsItems, { id: `wbs-${crypto.randomUUID()}`, name: newWBSName, parentId: selectedParentWBS, path: getWBSPath(selectedParentWBS, wbsItems) }];
    updatedWBSItems.sort((a, b) => (a.path && b.path) ? a.path.localeCompare(b.path, undefined, { numeric: true, sensitivity: 'base' }) : 0);
    try {
      await updateDoc(projectDocRef, { wbs: updatedWBSItems });
      setShowAddWBSModal(false); setNewWBSName(''); setEditingWBS(null); setSelectedParentWBS(null); setError(null);
    } catch (e) { console.error("Error WBS:", e); setError("Error al guardar EDT."); } finally { setIsLoading(false); }
  };

  const handleDeleteWBS = async (wbsIdToDelete) => {
    if (!window.confirm("¿Eliminar EDT, descendientes y actividades asociadas?")) return;
    if (!selectedProjectId || !userId) { setError("Error: Proyecto/Usuario no válido."); return; }
    setIsLoading(true);
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    const getDescendantIds = (parentId, allWbs) => { let ids = []; const children = allWbs.filter(w => w.parentId === parentId); for (const child of children) { ids.push(child.id); ids = ids.concat(getDescendantIds(child.id, allWbs));} return ids; };
    const idsToDelete = [wbsIdToDelete, ...getDescendantIds(wbsIdToDelete, wbsItems)];
    const remainingWBSItems = wbsItems.filter(w => !idsToDelete.includes(w.id));
    const remainingActivities = (selectedProject.activities || []).filter(act => !idsToDelete.includes(act.wbsId));
    try {
      await updateDoc(projectDocRef, { wbs: remainingWBSItems, activities: remainingActivities }); setError(null);
    } catch (e) { console.error("Error eliminando WBS:", e); setError("Error al eliminar EDT."); } finally { setIsLoading(false); }
  };

  const openAddModal = (parentId = null) => { setEditingWBS(null); setNewWBSName(''); setSelectedParentWBS(parentId); setShowAddWBSModal(true); };
  const openEditModal = (wbsItem) => { setEditingWBS(wbsItem); setNewWBSName(wbsItem.name); setSelectedParentWBS(wbsItem.parentId); setShowAddWBSModal(true); };

  const renderWBSNode = (parentId = null, level = 0) => wbsItems.filter(item => item.parentId === parentId).map(item => (
    <div key={item.id} style={{ marginLeft: `${level * 20}px` }} className="my-1.5">
      <div className="flex items-center justify-between p-2.5 bg-gray-50 border rounded-md hover:bg-gray-100">
        <span className="text-sm text-gray-700 flex items-center">{level > 0 && <ChevronRight size={14} className="mr-1 text-gray-400"/>}{item.name} <span className="ml-2 text-xs text-gray-400">(...{item.id.slice(-4)})</span></span>
        <div className="space-x-1.5">
          <button onClick={() => openAddModal(item.id)} title="Añadir Hijo" className="p-1 text-green-600 hover:text-green-800"><PlusCircle size={17}/></button>
          <button onClick={() => openEditModal(item)} title="Editar" className="p-1 text-blue-600 hover:text-blue-800"><Edit2 size={17}/></button>
          <button onClick={() => handleDeleteWBS(item.id)} title="Eliminar" className="p-1 text-red-600 hover:text-red-800"><Trash2 size={17}/></button>
        </div>
      </div>
      {renderWBSNode(item.id, level + 1)}
    </div>
  ));

  if (!selectedProject) return <LoadingSpinner message="Cargando EDT..." />;
  return (
    <div className="p-1 md:p-4">
      <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
        <h2 className="text-xl md:text-2xl font-semibold text-gray-800">EDT / WBS: {selectedProject.name}</h2>
        <button onClick={() => openAddModal(wbsItems.find(w => !w.parentId)?.id || null)} className="btn-primary px-3 py-1.5 md:px-4 md:py-2 text-sm flex items-center space-x-2"><PlusCircle size={18} /> <span>Añadir Elemento</span></button>
      </div>
      {wbsItems.length === 0 && <Notification type="info" message="No hay elementos EDT." />}
      <div>{renderWBSNode(null)}</div>
      {showAddWBSModal && <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50"><div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-md">
        <h3 className="text-lg md:text-xl font-semibold mb-4">{editingWBS ? 'Editar' : 'Añadir'} Elemento EDT</h3>
        <form onSubmit={(e) => { e.preventDefault(); handleAddOrUpdateWBS(); }}>
          <div className="mb-4"><label htmlFor="wbsName" className="lbl">Nombre</label><input type="text" id="wbsName" value={newWBSName} onChange={(e) => setNewWBSName(e.target.value)} className="w-full input-style" required /></div>
          {!editingWBS && selectedParentWBS && <p className="text-xs text-gray-600 mb-4">Padre: {wbsItems.find(w => w.id === selectedParentWBS)?.name || 'Raíz'}</p>}
          <div className="flex justify-end space-x-3"><button type="button" onClick={() => { setShowAddWBSModal(false); setEditingWBS(null); setSelectedParentWBS(null); }} className="btn-secondary px-4 py-2 text-sm">Cancelar</button><button type="submit" className="btn-primary px-4 py-2 text-sm">{editingWBS ? 'Guardar' : 'Añadir'}</button></div>
        </form></div></div>}
    </div>
  );
};

const ActivityEditor = () => { /* Sin cambios funcionales mayores, solo ajustes de costos */
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setError } = useContext(AppContext);
  const [activities, setActivities] = useState([]);
  const [wbsOptions, setWbsOptions] = useState([]);
  const [allActivitiesOptions, setAllActivitiesOptions] = useState([]);
  const [showActivityModal, setShowActivityModal] = useState(false);
  const [currentActivity, setCurrentActivity] = useState(null);
  const initialFormState = {
    id: '', name: '', wbsId: '', duration: 1, predecessors: [], resources: [], percentComplete: 0,
    budgetedLaborCost: 0, budgetedMaterialCost: 0, budgetedExpenseCost: 0, budgetedTotalCost: 0,
    actualLaborCost: 0, actualMaterialCost: 0, actualExpenseCost: 0, actualTotalCost: 0,
    es: '', ef: '', ls: '', lf: '', float: null, isCritical: false,
  };
  const [activityFormData, setActivityFormData] = useState(initialFormState);

  useEffect(() => {
    if (selectedProject) {
      const projectActivities = (selectedProject.activities || []).map(act => ({
        ...act, budgetedLaborCost: act.budgetedLaborCost || 0, budgetedMaterialCost: act.budgetedMaterialCost || 0, budgetedExpenseCost: act.budgetedExpenseCost || 0,
        budgetedTotalCost: (act.budgetedLaborCost || 0) + (act.budgetedMaterialCost || 0) + (act.budgetedExpenseCost || 0),
        actualLaborCost: act.actualLaborCost || 0, actualMaterialCost: act.actualMaterialCost || 0, actualExpenseCost: act.actualExpenseCost || 0,
        actualTotalCost: (act.actualLaborCost || 0) + (act.actualMaterialCost || 0) + (act.actualExpenseCost || 0),
      }));
      setActivities(projectActivities.sort((a, b) => (a.id > b.id ? 1 : -1)));
      const options = (selectedProject.wbs || []).map(w => ({ value: w.id, label: w.name, path: w.path })).sort((a,b) => (a.path && b.path) ? a.path.localeCompare(b.path, undefined, { numeric: true, sensitivity: 'base' }) : 0);
      setWbsOptions(options);
      setAllActivitiesOptions(projectActivities.map(act => ({ value: act.id, label: `${act.id.slice(0,8)}... - ${act.name}` })));
      if (options.length > 0 && !activityFormData.wbsId) setActivityFormData(prev => ({ ...prev, wbsId: options[0].value }));
    }
  }, [selectedProject]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    let parsedValue = name.toLowerCase().includes('cost') || name === 'duration' || name === 'percentComplete' ? parseFloat(value) || 0 : value;
    setActivityFormData(prev => {
      const updatedForm = { ...prev, [name]: parsedValue };
      if (['budgetedLaborCost', 'budgetedMaterialCost', 'budgetedExpenseCost'].includes(name)) updatedForm.budgetedTotalCost = (updatedForm.budgetedLaborCost || 0) + (updatedForm.budgetedMaterialCost || 0) + (updatedForm.budgetedExpenseCost || 0);
      if (['actualLaborCost', 'actualMaterialCost', 'actualExpenseCost'].includes(name)) updatedForm.actualTotalCost = (updatedForm.actualLaborCost || 0) + (updatedForm.actualMaterialCost || 0) + (updatedForm.actualExpenseCost || 0);
      return updatedForm;
    });
  };

  const handlePredecessorChange = (selectedOptions) => setActivityFormData(prev => ({ ...prev, predecessors: Array.from(selectedOptions).map(option => option.value) }));

  const handleOpenModal = (activity = null) => {
    setCurrentActivity(activity);
    if (activity) setActivityFormData({ ...initialFormState, ...activity, budgetedTotalCost: (activity.budgetedLaborCost || 0) + (activity.budgetedMaterialCost || 0) + (activity.budgetedExpenseCost || 0), actualTotalCost: (activity.actualLaborCost || 0) + (activity.actualMaterialCost || 0) + (activity.actualExpenseCost || 0) });
    else setActivityFormData({ ...initialFormState, id: `act-${crypto.randomUUID()}`, wbsId: wbsOptions.length > 0 ? wbsOptions[0].value : '' });
    setShowActivityModal(true);
  };

  const handleSaveActivity = async () => {
    if (!activityFormData.name.trim() || !activityFormData.wbsId) { setError("Nombre y EDT obligatorios."); return; }
    if (!selectedProjectId || !userId) { setError("Error: Proyecto/Usuario no válido."); return; }
    setIsLoading(true);
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    const { es, ef, ls, lf, float, isCritical, ...dataToSave } = activityFormData; // Excluir campos calculados puro
    const activityToPersist = { ...dataToSave, es: currentActivity?.es || '', ef: currentActivity?.ef || '', ls: currentActivity?.ls || '', lf: currentActivity?.lf || '', float: currentActivity?.float !== undefined ? currentActivity.float : null, isCritical: currentActivity?.isCritical || false };

    let updatedActivities = currentActivity ? activities.map(act => act.id === currentActivity.id ? activityToPersist : act) : [...activities, activityToPersist];
    try {
      await updateDoc(projectDocRef, { activities: updatedActivities });
      setShowActivityModal(false); setCurrentActivity(null); setError(null);
    } catch (e) { console.error("Error guardando actividad:", e); setError("Error al guardar actividad."); } finally { setIsLoading(false); }
  };

  const handleDeleteActivity = async (activityIdToDelete) => { 
    if (!window.confirm("¿Eliminar esta actividad?")) return;
    if (!selectedProjectId || !userId) { setError("Error: Proyecto/Usuario no válido."); return; }
    setIsLoading(true);
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    const remainingActivities = activities.filter(act => act.id !== activityIdToDelete).map(act => ({ ...act, predecessors: (act.predecessors || []).filter(pId => pId !== activityIdToDelete) }));
    try { await updateDoc(projectDocRef, { activities: remainingActivities }); setError(null); }
    catch (e) { console.error("Error eliminando actividad:", e); setError("Error al eliminar actividad."); } finally { setIsLoading(false); }
  };
  
  const getWBSName = (wbsId) => wbsOptions.find(w => w.value === wbsId)?.label || 'N/A';

  if (!selectedProject) return <LoadingSpinner message="Cargando actividades..." />;
  return (
    <div className="p-1 md:p-4">
      <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
        <h2 className="text-xl md:text-2xl font-semibold">Actividades: {selectedProject.name}</h2>
        <button onClick={() => handleOpenModal()} className="btn-primary px-3 py-1.5 md:px-4 md:py-2 text-sm flex items-center space-x-2" disabled={wbsOptions.length === 0}><PlusCircle size={18} /> <span>Añadir Actividad</span></button>
      </div>
      {wbsOptions.length === 0 && <Notification type="info" message="Crea elementos EDT para añadir actividades." />}
      {activities.length === 0 && wbsOptions.length > 0 && <p className="text-gray-500">No hay actividades.</p>}
      {activities.length > 0 && <div className="overflow-x-auto shadow-md rounded-lg"><table className="min-w-full bg-white border text-sm">
        <thead className="bg-gray-50"><tr>{['ID', 'Nombre', 'EDT', 'Dur. (d)', 'Costo Presup. Total', '% Comp.', 'Acciones'].map(h => <th key={h} className="th-style">{h}</th>)}</tr></thead>
        <tbody className="divide-y divide-gray-200">{activities.map(act => <tr key={act.id} className="hover:bg-gray-50">
          <td className="td-style font-mono text-xs" title={act.id}>{act.id.slice(0,8)}...</td><td className="td-style">{act.name}</td>
          <td className="td-style">{getWBSName(act.wbsId)}</td><td className="td-style text-center">{act.duration}</td>
          <td className="td-style text-right">{formatCurrency(act.budgetedTotalCost)}</td><td className="td-style text-center">{act.percentComplete || 0}%</td>
          <td className="td-style space-x-1.5"><button onClick={() => handleOpenModal(act)} title="Editar" className="btn-icon text-blue-600"><Edit2 size={17}/></button><button onClick={() => handleDeleteActivity(act.id)} title="Eliminar" className="btn-icon text-red-600"><Trash2 size={17}/></button></td>
        </tr>)}</tbody></table></div>}
      {showActivityModal && <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center p-4 z-50 overflow-y-auto"><div className="bg-white p-5 md:p-6 rounded-lg shadow-xl w-full max-w-2xl my-8">
        <h3 className="text-lg md:text-xl font-semibold mb-4">{currentActivity ? 'Editar' : 'Añadir'} Actividad (ID: {activityFormData.id.slice(0,8)}...)</h3>
        <form onSubmit={(e) => { e.preventDefault(); handleSaveActivity(); }}><div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-4 mb-4">
          <div><label htmlFor="activityName" className="lbl">Nombre</label><input type="text" name="name" id="activityName" value={activityFormData.name} onChange={handleInputChange} className="w-full input-style" required /></div>
          <div><label htmlFor="activityWbsId" className="lbl">Elemento EDT</label><select name="wbsId" id="activityWbsId" value={activityFormData.wbsId} onChange={handleInputChange} className="w-full input-style" required>{wbsOptions.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select></div>
          <div><label htmlFor="activityDuration" className="lbl">Duración (días)</label><input type="number" name="duration" id="activityDuration" value={activityFormData.duration} onChange={handleInputChange} min="0" className="w-full input-style" required /></div>
          <div><label htmlFor="activityPercentComplete" className="lbl">% Completado</label><input type="number" name="percentComplete" id="activityPercentComplete" value={activityFormData.percentComplete} onChange={handleInputChange} min="0" max="100" step="1" className="w-full input-style" /></div>
          <div className="md:col-span-2 mt-2 pt-3 border-t"><h4 className="text-md font-semibold text-gray-700 mb-2">Costos Presupuestados</h4></div>
          <div><label htmlFor="budgetedLaborCost" className="lbl">Mano de Obra ($)</label><input type="number" name="budgetedLaborCost" value={activityFormData.budgetedLaborCost} onChange={handleInputChange} min="0" step="any" className="w-full input-style" /></div>
          <div><label htmlFor="budgetedMaterialCost" className="lbl">Materiales ($)</label><input type="number" name="budgetedMaterialCost" value={activityFormData.budgetedMaterialCost} onChange={handleInputChange} min="0" step="any" className="w-full input-style" /></div>
          <div><label htmlFor="budgetedExpenseCost" className="lbl">Gastos ($)</label><input type="number" name="budgetedExpenseCost" value={activityFormData.budgetedExpenseCost} onChange={handleInputChange} min="0" step="any" className="w-full input-style" /></div>
          <div><label htmlFor="budgetedTotalCost" className="lbl">Total Presup. ($)</label><input type="number" name="budgetedTotalCost" value={activityFormData.budgetedTotalCost} className="w-full input-style bg-gray-100" readOnly /></div>
          <div className="md:col-span-2 mt-2 pt-3 border-t"><label htmlFor="activityPredecessors" className="lbl">Predecesoras (FS)</label><select multiple name="predecessors" value={activityFormData.predecessors} onChange={(e) => handlePredecessorChange(e.target.selectedOptions)} className="w-full input-style h-24">{allActivitiesOptions.filter(opt => opt.value !== activityFormData.id).map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select><p className="text-xs text-gray-500 mt-1">Ctrl/Cmd para múltiples.</p></div>
          {currentActivity && <div className="md:col-span-2 mt-2 pt-3 border-t"><h4 className="text-md font-semibold text-gray-700 mb-2">Datos Programación (Calculados)</h4><div className="grid grid-cols-2 md:grid-cols-4 gap-x-6 gap-y-2">
            <div><label className="lbl-xs">ES</label><input type="text" value={activityFormData.es||'-'} className="input-xs-ro" readOnly/></div><div><label className="lbl-xs">EF</label><input type="text" value={activityFormData.ef||'-'} className="input-xs-ro" readOnly/></div>
            <div><label className="lbl-xs">LS</label><input type="text" value={activityFormData.ls||'-'} className="input-xs-ro" readOnly/></div><div><label className="lbl-xs">LF</label><input type="text" value={activityFormData.lf||'-'} className="input-xs-ro" readOnly/></div>
            <div><label className="lbl-xs">Holgura</label><input type="text" value={activityFormData.float !== null ? activityFormData.float : '-'} className="input-xs-ro" readOnly/></div><div><label className="lbl-xs">Crítica</label><input type="text" value={activityFormData.isCritical ? 'Sí':'No'} className="input-xs-ro" readOnly/></div>
          </div></div>}
        </div><div className="flex justify-end space-x-3 mt-5"><button type="button" onClick={() => setShowActivityModal(false)} className="btn-secondary px-4 py-2 text-sm">Cancelar</button><button type="submit" className="btn-primary px-4 py-2 text-sm">{currentActivity ? 'Guardar' : 'Añadir'}</button></div></form></div></div>}
    </div>
  );
};

// --- Componente Carta Gantt Básico ---
const BasicGanttChart = ({ activities, projectStartDate }) => {
  if (!activities || activities.length === 0 || !projectStartDate) {
    return <div className="p-4 text-center text-gray-500">No hay datos suficientes para mostrar la Carta Gantt. Asegúrate de tener actividades programadas y una fecha de inicio del proyecto.</div>;
  }

  const BAR_HEIGHT = 20;
  const ROW_GAP = 10;
  const LABEL_WIDTH = 150; // Ancho para etiquetas de actividad
  const SIDE_PADDING = 20;
  const TOP_PADDING = 50; // Espacio para la escala de tiempo
  const DAY_WIDTH = 20; // Ancho de cada día en píxeles
  const TICK_HEIGHT = 5;

  const chartActivities = activities.filter(act => act.es && act.ef && act.duration > 0);
  if (chartActivities.length === 0) {
    return <div className="p-4 text-center text-gray-500">No hay actividades con fechas de inicio/fin calculadas para mostrar en la Gantt.</div>;
  }
  
  const overallStartDate = minDate([projectStartDate, ...chartActivities.map(act => act.es)]);
  const overallEndDate = maxDate([...chartActivities.map(act => act.ef)]);

  if (!overallStartDate || !overallEndDate) {
      return <div className="p-4 text-center text-gray-500">No se pudieron determinar las fechas de inicio/fin del gráfico.</div>;
  }

  const totalDays = dateDiffInDays(overallStartDate, overallEndDate) + 1;
  const chartWidth = totalDays * DAY_WIDTH;
  const svgWidth = LABEL_WIDTH + chartWidth + SIDE_PADDING * 2;
  const svgHeight = TOP_PADDING + chartActivities.length * (BAR_HEIGHT + ROW_GAP) + SIDE_PADDING;

  const dateToX = (dateStr) => {
    if (!dateStr) return 0;
    const diff = dateDiffInDays(overallStartDate, dateStr);
    return diff * DAY_WIDTH;
  };

  // Generar marcas de tiempo (ticks)
  const timelineTicks = [];
  let currentDate = new Date(overallStartDate + 'T00:00:00Z');
  const endDateObj = new Date(overallEndDate + 'T00:00:00Z');
  
  let monthTracker = -1;

  for (let i = 0; i <= totalDays; i++) {
    const xPos = i * DAY_WIDTH;
    const day = currentDate.getUTCDate();
    const month = currentDate.getUTCMonth();
    
    // Marcas diarias y mensuales
    if (day === 1 || i === 0) { // Inicio de mes o primer día del gráfico
        timelineTicks.push({
            x: xPos,
            label: currentDate.toLocaleDateString('es-ES', { month: 'short', timeZone: 'UTC' }),
            isMonth: true,
        });
        monthTracker = month;
    } else if (totalDays <= 60 && (day % 5 === 0 || day === 1)) { // Marcas cada 5 días si el total es corto
         timelineTicks.push({ x: xPos, label: String(day), isMonth: false });
    } else if (totalDays > 60 && (day % 7 === 0 || day === 1 )) { // Marcas semanales aprox.
         timelineTicks.push({ x: xPos, label: String(day), isMonth: false });
    }
    currentDate.setUTCDate(currentDate.getUTCDate() + 1);
    if (currentDate > endDateObj && i < totalDays) { // Asegurar que el último día se incluya si es necesario
        if (timelineTicks[timelineTicks.length-1].label !== String(endDateObj.getUTCDate())) {
             timelineTicks.push({ x: (i+1) * DAY_WIDTH, label: String(endDateObj.getUTCDate()), isMonth: false });
        }
    }
     if (i >= totalDays && currentDate <= endDateObj) { // Asegurar que el último tick del mes final
        if (monthTracker !== endDateObj.getUTCMonth()) {
             timelineTicks.push({ x: (i+1) * DAY_WIDTH, label: endDateObj.toLocaleDateString('es-ES', { month: 'short', timeZone: 'UTC' }), isMonth: true });
        }
    }
  }


  return (
    <div className="overflow-x-auto bg-white p-2 rounded shadow-lg mt-4 border">
      <svg width={svgWidth} height={svgHeight} className="font-sans text-xs">
        {/* Definiciones de patrones o gradientes si se necesitan */}
        <defs>
            <pattern id="gridPattern" width={DAY_WIDTH} height={BAR_HEIGHT + ROW_GAP} patternUnits="userSpaceOnUse">
                <path d={`M ${DAY_WIDTH} 0 L ${DAY_WIDTH} ${BAR_HEIGHT + ROW_GAP} M 0 ${BAR_HEIGHT + ROW_GAP} L ${DAY_WIDTH} ${BAR_HEIGHT + ROW_GAP}`} fill="none" stroke="rgba(200,200,200,0.3)" strokeWidth="0.5"/>
            </pattern>
        </defs>

        {/* Fondo con patrón de rejilla (opcional) */}
        {/* <rect x={LABEL_WIDTH} y={TOP_PADDING} width={chartWidth} height={chartActivities.length * (BAR_HEIGHT + ROW_GAP)} fill="url(#gridPattern)" /> */}

        {/* Timeline */}
        <g transform={`translate(${LABEL_WIDTH + SIDE_PADDING}, ${TOP_PADDING})`}>
          <line x1="0" y1="-5" x2={chartWidth} y2="-5" stroke="#ccc" strokeWidth="1"/>
          {timelineTicks.map((tick, index) => (
            <g key={`tick-${index}`} transform={`translate(${tick.x}, 0)`}>
              <line y1="-5" y2={tick.isMonth ? -TICK_HEIGHT -5 : -TICK_HEIGHT} stroke="#888" strokeWidth="0.5" />
              <text y={tick.isMonth ? -18 : -10} x="3" textAnchor="start" fontSize="0.65rem" fill="#555" className={tick.isMonth ? 'font-semibold': ''}>
                {tick.label}
              </text>
            </g>
          ))}
        </g>

        {/* Activity Bars and Labels */}
        <g transform={`translate(${SIDE_PADDING}, ${TOP_PADDING})`}>
          {chartActivities.map((act, index) => {
            const yPos = index * (BAR_HEIGHT + ROW_GAP);
            const barX = LABEL_WIDTH + dateToX(act.es);
            // Duración en días, pero la barra debe tener al menos 1 DAY_WIDTH si la duración es 1.
            // Si es 0 días (hito), dibujar un diamante o círculo.
            let barWidth = (Math.max(1, act.duration)) * DAY_WIDTH; 
            if (act.duration === 0) barWidth = DAY_WIDTH / 2; // Hito

            return (
              <g key={act.id} transform={`translate(0, ${yPos})`}>
                {/* Activity Label */}
                <text x={LABEL_WIDTH - 5} y={BAR_HEIGHT / 2 + 4} textAnchor="end" fontSize="0.7rem" fill="#333" className="truncate">
                  {act.name.length > 25 ? act.name.substring(0,22) + "..." : act.name}
                </text>
                
                {/* Activity Bar */}
                <rect
                  x={barX}
                  y="0"
                  width={barWidth -1 } // Pequeño ajuste para que no se solapen los bordes
                  height={BAR_HEIGHT}
                  fill={act.isCritical ? "rgba(239, 68, 68, 0.7)" : "rgba(59, 130, 246, 0.7)"} // Rojo para críticas, Azul para no críticas
                  stroke={act.isCritical ? "rgba(185, 28, 28, 0.9)" : "rgba(37, 99, 235, 0.9)"}
                  strokeWidth="1"
                  rx="3" // Bordes redondeados
                  ry="3"
                >
                  <title>{`${act.name}\nInicio: ${act.es}\nFin: ${act.ef}\nDuración: ${act.duration}d`}</title>
                </rect>
                 {/* Texto dentro de la barra (opcional, si hay espacio) */}
                {barWidth > 50 && (
                    <text x={barX + 5} y={BAR_HEIGHT / 2 + 4} fontSize="0.6rem" fill={act.isCritical ? "#fff" : "#fff"} className="pointer-events-none">
                        {act.id.slice(0,5)}...
                    </text>
                )}
              </g>
            );
          })}
        </g>
      </svg>
    </div>
  );
};


// --- Vista de Programación (Scheduling) ---
const SchedulingView = () => {
  const { selectedProject, selectedProjectId, userId, appId, db, setIsLoading, setError } = useContext(AppContext);
  const [scheduledActivities, setScheduledActivities] = useState([]);
  const [isCalculating, setIsCalculating] = useState(false);

  useEffect(() => {
    if (selectedProject && selectedProject.activities) {
      setScheduledActivities(selectedProject.activities.sort((a,b) => (a.es && b.es) ? (dateToEpochDays(a.es) - dateToEpochDays(b.es)) : (a.id > b.id ? 1 : -1) ));
    }
  }, [selectedProject]);

  const handleCalculateSchedule = async () => {
    if (!selectedProject || !selectedProject.activities || !selectedProject.startDate) { setError("Datos del proyecto incompletos."); return; }
    setIsCalculating(true); setIsLoading(true); setError(null);
    let activities = JSON.parse(JSON.stringify(selectedProject.activities || [])); 
    const projectStartDate = selectedProject.dataDate || selectedProject.startDate;

    activities.forEach(act => {
      act.es = null; act.ef = null; act.ls = null; act.lf = null; act.float = null; act.isCritical = false;
      act.duration = Number(act.duration) || 0; if (act.duration < 0) act.duration = 0; 
      act.predecessors = act.predecessors || [];
    });

    let changedInIteration, iterations = 0, MAX_ITERATIONS = activities.length * 2; 
    do { // Forward Pass
        changedInIteration = false; iterations++;
        activities.forEach(act => {
            let newES = act.predecessors.length === 0 ? projectStartDate : maxDate(act.predecessors.map(pId => activities.find(p=>p.id===pId)?.ef).filter(Boolean).map(ef => addDaysToDate(ef,1)));
            if (act.predecessors.length > 0 && !newES) newES = act.es; // Keep if preds not ready
            if (newES && newES !== act.es) { act.es = newES; changedInIteration = true; }
            if (act.es) { const newEF = addDaysToDate(act.es, Math.max(0, act.duration -1)); if (newEF !== act.ef) { act.ef = newEF; changedInIteration = true; } }
        });
    } while (changedInIteration && iterations < MAX_ITERATIONS);
    if (iterations >= MAX_ITERATIONS) console.warn("Max iterations en Pase Adelante.");
    
    const projectFinishDate = maxDate(activities.map(act => act.ef).filter(Boolean)) || projectStartDate;
    iterations = 0; 
    do { // Backward Pass
        changedInIteration = false; iterations++;
        [...activities].reverse().forEach(act => {
            const successors = activities.filter(succ => succ.predecessors.includes(act.id));
            let newLF = successors.length === 0 ? (act.ef || projectFinishDate) : minDate(successors.map(s => s.ls).filter(Boolean).map(ls => addDaysToDate(ls, -1)));
            if (successors.length > 0 && !newLF) newLF = act.lf; // Keep if succs not ready
            if (newLF && newLF !== act.lf) { act.lf = newLF; changedInIteration = true; }
            if (act.lf) { const newLS = addDaysToDate(act.lf, -(Math.max(0, act.duration - 1))); if (newLS !== act.ls) { act.ls = newLS; changedInIteration = true; } }
        });
    } while (changedInIteration && iterations < MAX_ITERATIONS);
    if (iterations >= MAX_ITERATIONS) console.warn("Max iterations en Pase Atrás.");

    let minFloat = Infinity;
    activities.forEach(act => {
      if (act.ls && act.es) { act.float = dateDiffInDays(act.es, act.ls); if (act.float < minFloat) minFloat = act.float; } 
      else act.float = null; 
    });
    activities.forEach(act => { act.isCritical = act.float !== null && act.float <= (minFloat + 0.01); });
    
    const projectDocRef = doc(db, `artifacts/${appId}/users/${userId}/p6_projects/${selectedProjectId}`);
    try {
      await updateDoc(projectDocRef, { activities: activities });
      setScheduledActivities(activities.sort((a,b) => (a.es && b.es) ? (dateToEpochDays(a.es) - dateToEpochDays(b.es)) : (a.id > b.id ? 1 : -1)));
      alert("Cronograma calculado y guardado.");
    } catch (e) { console.error("Error guardando cronograma:", e); setError("Error al guardar cronograma."); }
    finally { setIsCalculating(false); setIsLoading(false); }
  };

  const getPredecessorDetails = (predIds) => { /* Sin cambios */
    if (!predIds || predIds.length === 0) return 'Ninguna';
    return predIds.map(id => {
        const predAct = selectedProject?.activities?.find(act => act.id === id);
        return predAct ? `${predAct.id.slice(0,6)}... (${predAct.name.slice(0,10)}...)` : 'ID desc.';
    }).join(', ');
  };

  if (!selectedProject) return <LoadingSpinner message="Cargando programación..." />;
  return (
    <div className="p-1 md:p-4">
      <div className="flex flex-col md:flex-row justify-between md:items-center mb-5 pb-2 border-b">
        <h2 className="text-xl md:text-2xl font-semibold">Programación: {selectedProject.name}</h2>
        <button onClick={handleCalculateSchedule} disabled={isCalculating || !(selectedProject?.activities?.length > 0)}
          className="btn-primary px-3 py-1.5 md:px-4 md:py-2 text-sm flex items-center space-x-2 disabled:opacity-50">
          <Play size={18} /> <span>Calcular Cronograma</span>
        </button>
      </div>
      {isCalculating && <LoadingSpinner message="Calculando cronograma..." />}
      {!isCalculating && scheduledActivities.length === 0 && <Notification type="info" message="No hay actividades para programar." />}
      {!isCalculating && scheduledActivities.length > 0 && (
        <>
          <div className="overflow-x-auto shadow-md rounded-lg mb-6">
            <table className="min-w-full bg-white border text-xs">
              <thead className="bg-gray-100"><tr>{['ID', 'Nombre', 'Dur.', 'Predec.', 'ES', 'EF', 'LS', 'LF', 'Holgura', 'Crítica'].map(h => <th key={h} className="th-style-xs whitespace-nowrap">{h}</th>)}</tr></thead>
              <tbody className="divide-y divide-gray-200">{scheduledActivities.map(act => <tr key={act.id} className={`hover:bg-gray-50 ${act.isCritical ? 'bg-red-50' : ''}`}>
                <td className="td-style-xs font-mono" title={act.id}>{act.id.slice(0,6)}...</td><td className="td-style-xs">{act.name}</td>
                <td className="td-style-xs text-center">{act.duration}</td><td className="td-style-xs" title={getPredecessorDetails(act.predecessors)}>{(act.predecessors || []).length > 0 ? `${(act.predecessors || []).map(p => p.slice(0,6)+"...").join(', ')}` : '-'}</td>
                <td className="td-style-xs text-blue-700">{act.es||'-'}</td><td className="td-style-xs text-blue-700">{act.ef||'-'}</td>
                <td className="td-style-xs text-green-700">{act.ls||'-'}</td><td className="td-style-xs text-green-700">{act.lf||'-'}</td>
                <td className={`td-style-xs text-center font-medium ${act.float !== null && act.float <= 0 ? 'text-red-600':'text-gray-600'}`}>{act.float !== null ? act.float : '-'}</td>
                <td className={`td-style-xs text-center font-semibold ${act.isCritical ? 'text-red-600':'text-gray-500'}`}>{act.isCritical?'Sí':'No'}</td>
              </tr>)}</tbody>
            </table>
          </div>
          <BasicGanttChart activities={scheduledActivities} projectStartDate={selectedProject.dataDate || selectedProject.startDate} />
        </>
      )}
       <div className="mt-6 p-3 bg-gray-50 rounded-lg text-xs text-gray-700 print:hidden">
        <h4 className="font-semibold mb-1">Notas sobre la Programación:</h4>
        <ul className="list-disc list-inside space-y-0.5">
            <li>Duraciones en días calendario. Relaciones FS con 0 lag.</li>
            <li>ES: Inicio Temprano, EF: Fin Temprano, LS: Inicio Tardío, LF: Fin Tardío.</li>
            <li>Holgura: LS - ES. Críticas tienen menor holgura (usualmente {'<='} 0).</li>
            <li>Cálculo basado en CPM simplificado. Data Date (ver Config.) es inicio para actividades sin predecesoras.</li>
        </ul>
      </div>
    </div>
  );
};

const CostsView = () => { /* Sin cambios */
    const { selectedProject, isLoading } = useContext(AppContext);
    if (isLoading) return <LoadingSpinner message="Cargando costos..." />;
    if (!selectedProject) return <Notification type="info" message="Selecciona un proyecto." />;
    const projectActivities = selectedProject.activities || [];
    const totalBudgetedProjectCost = projectActivities.reduce((sum, act) => sum + (act.budgetedTotalCost || 0), 0);
    return (
        <div className="p-1 md:p-4">
            <h2 className="text-xl md:text-2xl font-semibold mb-5 text-gray-800 border-b pb-2">Costos: {selectedProject.name}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg shadow"><h3 className="text-lg font-medium text-blue-700 mb-1">Costo Total Presupuestado</h3><p className="text-2xl font-bold text-blue-800">{formatCurrency(totalBudgetedProjectCost)}</p></div>
            </div>
            <h3 className="text-lg font-semibold text-gray-700 mb-3">Desglose Costos Presupuestados por Actividad</h3>
            {projectActivities.length === 0 && <Notification type="info" message="No hay actividades con costos." />}
            {projectActivities.length > 0 && <div className="overflow-x-auto shadow-md rounded-lg"><table className="min-w-full bg-white border text-sm">
                <thead className="bg-gray-50"><tr>{['ID Act.', 'Nombre Act.', 'M. Obra ($)', 'Materiales ($)', 'Gastos ($)', 'Total Presup. ($)'].map(h=><th key={h} className="th-style">{h}</th>)}</tr></thead>
                <tbody className="divide-y divide-gray-200">{projectActivities.map(act => <tr key={act.id} className="hover:bg-gray-50">
                    <td className="td-style font-mono text-xs" title={act.id}>{act.id.slice(0,8)}...</td><td className="td-style">{act.name}</td>
                    <td className="td-style text-right">{formatCurrency(act.budgetedLaborCost)}</td><td className="td-style text-right">{formatCurrency(act.budgetedMaterialCost)}</td>
                    <td className="td-style text-right">{formatCurrency(act.budgetedExpenseCost)}</td><td className="td-style font-semibold text-right">{formatCurrency(act.budgetedTotalCost)}</td>
                </tr>)}</tbody>
                <tfoot className="bg-gray-100"><tr><td colSpan="5" className="px-3 py-2 text-right font-bold">TOTAL PROYECTO:</td><td className="px-3 py-2 text-right font-bold">{formatCurrency(totalBudgetedProjectCost)}</td></tr></tfoot>
            </table></div>}
            <div className="mt-6 p-3 bg-yellow-50 border-l-4 border-yellow-400 rounded-lg text-xs text-yellow-800 print:hidden">
                <h4 className="font-semibold mb-1">Funcionalidad Futura:</h4>
                <ul className="list-disc list-inside space-y-0.5"><li>Costos reales, Comparación Presupuesto vs. Real, EVM, Curvas S.</li></ul>
            </div>
        </div>
    );
};

// --- Componentes Auxiliares ---
const LoadingSpinner = ({ message = "Cargando..." }) => ( /* Sin cambios */
  <div className="flex flex-col items-center justify-center h-full p-4 text-center">
    <svg className="animate-spin h-8 w-8 text-blue-500 mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
    <p className="text-sm text-gray-600">{message}</p>
  </div>
);
const Notification = ({ type, message, onClose }) => { /* Sin cambios */
  const typeClasses = { error: { bg: 'bg-red-100', border: 'border-red-400', text: 'text-red-700', iconColor: 'text-red-500', Icon: AlertCircle }, success: { bg: 'bg-green-100', border: 'border-green-400', text: 'text-green-700', iconColor: 'text-green-500', Icon: CheckCircle }, info: { bg: 'bg-blue-100', border: 'border-blue-400', text: 'text-blue-700', iconColor: 'text-blue-500', Icon: Info }};
  const currentType = typeClasses[type] || typeClasses.info;
  return (<div className={`border-l-4 ${currentType.border} ${currentType.bg} p-3 my-3 rounded-md shadow print:hidden`} role="alert"><div className="flex"><div className="py-1"><currentType.Icon size={20} className={`${currentType.iconColor} mr-2`} /></div><div><p className={`text-sm ${currentType.text}`}>{message}</p></div>{onClose && <button onClick={onClose} className="ml-auto -mx-1.5 -my-1.5 bg-transparent rounded-lg focus:ring-2 focus:ring-gray-400 p-1.5 hover:bg-gray-200 inline-flex h-8 w-8"><span className="sr-only">Cerrar</span><svg className="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14"><path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/></svg></button>}</div></div>);
};
const PlaceholderView = ({ viewName }) => { /* Sin cambios */
    const {selectedProject} = useContext(AppContext);
    const viewLabels = { resources: "Recursos", baselines: "Líneas Base", progress: "Avance", reports: "Informes", risks: "Riesgos", layouts: "Layouts" };
    return (<div className="p-1 md:p-4 text-center"><h2 className="text-xl md:text-2xl font-semibold mb-4">{viewLabels[viewName] || viewName}</h2><div className="flex flex-col items-center justify-center bg-gray-50 p-8 rounded-lg shadow min-h-[300px]"><Briefcase size={60} className="text-gray-300 mb-6" /><p className="text-lg text-gray-500">Funcionalidad de "{viewLabels[viewName] || viewName}" próximamente.</p><p className="text-sm text-gray-400 mt-2">Gracias por tu paciencia.</p>{selectedProject && <p className="mt-4 text-xs text-gray-400">Proyecto: {selectedProject.name}</p>}</div></div>);
};

const GlobalStylesInjector = () => { /* Actualizado para incluir estilos de tabla y etiquetas */
  useEffect(() => {
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = `
      .input-style { padding: 0.5rem 0.75rem; border: 1px solid #D1D5DB; border-radius: 0.375rem; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out; font-size: 0.875rem; }
      .input-style:focus { outline: none; border-color: #3B82F6; box-shadow: 0 0 0 0.2rem rgba(59, 130, 246, 0.25); }
      .input-style-xs, .input-xs-ro { padding: 0.25rem 0.5rem; border: 1px solid #D1D5DB; border-radius: 0.25rem; font-size: 0.75rem; }
      .input-xs-ro { background-color: #F3F4F6; } /* bg-gray-100 */
      .btn-primary { background-color: #2563EB; color: white; font-weight: 500; border-radius: 0.375rem; transition: background-color 0.15s ease-in-out; }
      .btn-primary:hover { background-color: #1D4ED8; } .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
      .btn-secondary { background-color: #E5E7EB; color: #374151; font-weight: 500; border-radius: 0.375rem; border: 1px solid #D1D5DB; transition: background-color 0.15s ease-in-out; }
      .btn-secondary:hover { background-color: #D1D5DB; }
      .btn-icon { padding: 0.25rem; border-radius: 0.25rem; } .btn-icon:hover { background-color: rgba(0,0,0,0.05); }
      .font-inter { font-family: 'Inter', sans-serif; }
      .lbl { display: block; font-size: 0.875rem; font-weight: 500; color: #374151; margin-bottom: 0.25rem; } /* Estilo para labels */
      .lbl-xs { display: block; font-size: 0.75rem; font-weight: 500; color: #4B5563; } /* Estilo para labels pequeños */
      .th-style { padding: 0.75rem; text-align: left; font-size: 0.75rem; font-weight: 500; color: #4B5563; text-transform: uppercase; letter-spacing: 0.05em; }
      .td-style { padding: 0.75rem; white-space: nowrap; color: #374151; }
      .th-style-xs { padding: 0.5rem 0.75rem; text-align: left; font-size: 0.65rem; font-weight: 500; color: #4B5563; text-transform: uppercase; letter-spacing: 0.05em; }
      .td-style-xs { padding: 0.5rem 0.75rem; white-space: nowrap; color: #374151; }
      @media print { .print\\:hidden { display: none; } }
    `;
    document.head.appendChild(styleSheet);
    const interFontLink = document.createElement('link');
    interFontLink.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap';
    interFontLink.rel = 'stylesheet';
    document.head.appendChild(interFontLink);
    return () => { document.head.removeChild(styleSheet); document.head.removeChild(interFontLink); };
  }, []);
  return null;
};

export default function MainApp() {
  return ( <> <GlobalStylesInjector /> <App /> </> );
}

