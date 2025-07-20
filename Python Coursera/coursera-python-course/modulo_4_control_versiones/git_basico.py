"""
Módulo 4: Control de Versiones con Git
=====================================

Este módulo cubre:
- Conceptos básicos de control de versiones
- Comandos Git fundamentales
- Flujo de trabajo con Git
- Colaboración en proyectos
- Mejores prácticas

Autor: Curso Python Coursera
Versión: 1.0
"""

import os
import subprocess
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class SimuladorGit:
    """
    Simulador de Git para aprender los conceptos básicos
    """
    
    def __init__(self, nombre_repositorio: str = "mi_proyecto"):
        self.nombre_repositorio = nombre_repositorio
        self.archivos = {}
        self.commits = []
        self.rama_actual = "main"
        self.ramas = {"main": []}
        self.staging_area = {}
        self.ultimo_commit = None
    
    def git_init(self) -> str:
        """
        Inicializar un repositorio Git
        
        Returns:
            str: Mensaje de confirmación
        """
        if not self.commits:
            self.commits.append({
                'hash': '0000000',
                'mensaje': 'Initial commit',
                'fecha': datetime.now().isoformat(),
                'archivos': {},
                'rama': 'main'
            })
            self.ultimo_commit = '0000000'
            return f"Repositorio Git inicializado en '{self.nombre_repositorio}'"
        else:
            return "Repositorio ya inicializado"
    
    def crear_archivo(self, nombre: str, contenido: str) -> str:
        """
        Crear un archivo en el directorio de trabajo
        
        Args:
            nombre: Nombre del archivo
            contenido: Contenido del archivo
            
        Returns:
            str: Mensaje de confirmación
        """
        self.archivos[nombre] = contenido
        return f"Archivo '{nombre}' creado"
    
    def git_add(self, archivo: str = None) -> str:
        """
        Agregar archivos al staging area
        
        Args:
            archivo: Nombre del archivo (None para todos)
            
        Returns:
            str: Mensaje de confirmación
        """
        if archivo:
            if archivo in self.archivos:
                self.staging_area[archivo] = self.archivos[archivo]
                return f"Archivo '{archivo}' agregado al staging area"
            else:
                return f"Error: Archivo '{archivo}' no encontrado"
        else:
            # Agregar todos los archivos modificados
            for nombre, contenido in self.archivos.items():
                self.staging_area[nombre] = contenido
            return f"{len(self.archivos)} archivos agregados al staging area"
    
    def git_commit(self, mensaje: str) -> str:
        """
        Hacer commit de los cambios en el staging area
        
        Args:
            mensaje: Mensaje del commit
            
        Returns:
            str: Mensaje de confirmación
        """
        if not self.staging_area:
            return "Error: No hay archivos en el staging area"
        
        # Generar hash simulado
        import hashlib
        contenido_hash = str(self.staging_area) + str(datetime.now())
        hash_commit = hashlib.md5(contenido_hash.encode()).hexdigest()[:7]
        
        # Crear commit
        commit = {
            'hash': hash_commit,
            'mensaje': mensaje,
            'fecha': datetime.now().isoformat(),
            'archivos': self.staging_area.copy(),
            'rama': self.rama_actual
        }
        
        self.commits.append(commit)
        self.ultimo_commit = hash_commit
        self.ramas[self.rama_actual].append(hash_commit)
        
        # Limpiar staging area
        self.staging_area = {}
        
        return f"Commit '{hash_commit}' creado: {mensaje}"
    
    def git_status(self) -> str:
        """
        Mostrar el estado del repositorio
        
        Returns:
            str: Estado del repositorio
        """
        status = f"Rama actual: {self.rama_actual}\n"
        status += f"Último commit: {self.ultimo_commit}\n\n"
        
        # Archivos en staging area
        if self.staging_area:
            status += "Archivos en staging area:\n"
            for archivo in self.staging_area:
                status += f"  {archivo}\n"
            status += "\n"
        
        # Archivos modificados
        archivos_modificados = []
        for archivo in self.archivos:
            if archivo not in self.staging_area:
                archivos_modificados.append(archivo)
        
        if archivos_modificados:
            status += "Archivos modificados (no en staging):\n"
            for archivo in archivos_modificados:
                status += f"  {archivo}\n"
        
        return status
    
    def git_log(self, num_commits: int = 5) -> str:
        """
        Mostrar historial de commits
        
        Args:
            num_commits: Número de commits a mostrar
            
        Returns:
            str: Historial de commits
        """
        if not self.commits:
            return "No hay commits en el repositorio"
        
        log = "Historial de commits:\n"
        log += "=" * 50 + "\n"
        
        for i, commit in enumerate(reversed(self.commits[-num_commits:])):
            fecha = datetime.fromisoformat(commit['fecha']).strftime('%Y-%m-%d %H:%M')
            log += f"Commit: {commit['hash']}\n"
            log += f"Fecha:  {fecha}\n"
            log += f"Rama:   {commit['rama']}\n"
            log += f"Mensaje: {commit['mensaje']}\n"
            log += f"Archivos: {', '.join(commit['archivos'].keys())}\n"
            log += "-" * 30 + "\n"
        
        return log
    
    def git_branch(self, nombre_rama: str = None) -> str:
        """
        Crear nueva rama o listar ramas
        
        Args:
            nombre_rama: Nombre de la nueva rama
            
        Returns:
            str: Mensaje de confirmación
        """
        if nombre_rama:
            if nombre_rama in self.ramas:
                return f"Error: Rama '{nombre_rama}' ya existe"
            else:
                self.ramas[nombre_rama] = self.ramas[self.rama_actual].copy()
                return f"Nueva rama '{nombre_rama}' creada"
        else:
            # Listar ramas
            ramas_info = "Ramas disponibles:\n"
            for rama in self.ramas:
                if rama == self.rama_actual:
                    ramas_info += f"* {rama}\n"
                else:
                    ramas_info += f"  {rama}\n"
            return ramas_info
    
    def git_checkout(self, nombre_rama: str) -> str:
        """
        Cambiar a una rama específica
        
        Args:
            nombre_rama: Nombre de la rama
            
        Returns:
            str: Mensaje de confirmación
        """
        if nombre_rama in self.ramas:
            self.rama_actual = nombre_rama
            if self.ramas[nombre_rama]:
                self.ultimo_commit = self.ramas[nombre_rama][-1]
            return f"Cambiado a rama '{nombre_rama}'"
        else:
            return f"Error: Rama '{nombre_rama}' no existe"


class ComandosGitReales:
    """
    Clase para ejecutar comandos Git reales (si Git está instalado)
    """
    
    @staticmethod
    def ejecutar_comando(comando: str) -> Tuple[bool, str]:
        """
        Ejecutar un comando Git real
        
        Args:
            comando: Comando a ejecutar
            
        Returns:
            Tuple[bool, str]: (éxito, salida)
        """
        try:
            resultado = subprocess.run(
                comando.split(),
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            return resultado.returncode == 0, resultado.stdout + resultado.stderr
        except Exception as e:
            return False, f"Error ejecutando comando: {str(e)}"
    
    @staticmethod
    def verificar_git_instalado() -> bool:
        """
        Verificar si Git está instalado
        
        Returns:
            bool: True si Git está disponible
        """
        exito, _ = ComandosGitReales.ejecutar_comando("git --version")
        return exito
    
    @staticmethod
    def comandos_basicos() -> Dict[str, str]:
        """
        Obtener lista de comandos Git básicos
        
        Returns:
            Dict[str, str]: Comandos y sus descripciones
        """
        return {
            "git init": "Inicializar un repositorio Git",
            "git add .": "Agregar todos los archivos al staging area",
            "git add <archivo>": "Agregar archivo específico al staging area",
            "git commit -m 'mensaje'": "Hacer commit con mensaje",
            "git status": "Ver estado del repositorio",
            "git log": "Ver historial de commits",
            "git log --oneline": "Ver historial simplificado",
            "git branch": "Listar ramas",
            "git branch <nombre>": "Crear nueva rama",
            "git checkout <rama>": "Cambiar a rama específica",
            "git checkout -b <rama>": "Crear y cambiar a nueva rama",
            "git merge <rama>": "Fusionar rama actual con otra",
            "git remote add origin <url>": "Agregar repositorio remoto",
            "git push origin <rama>": "Enviar cambios al repositorio remoto",
            "git pull origin <rama>": "Obtener cambios del repositorio remoto",
            "git clone <url>": "Clonar repositorio remoto",
            "git diff": "Ver diferencias en archivos",
            "git reset <archivo>": "Quitar archivo del staging area",
            "git revert <commit>": "Revertir commit específico"
        }


def ejemplo_flujo_trabajo_basico():
    """
    Ejemplo de flujo de trabajo básico con Git
    """
    print("=== Flujo de Trabajo Básico con Git ===\n")
    
    # Crear simulador
    git = SimuladorGit("proyecto_python")
    
    print("1. Inicializar repositorio:")
    print(git.git_init())
    print()
    
    print("2. Crear archivos:")
    print(git.crear_archivo("main.py", "print('Hola Mundo')"))
    print(git.crear_archivo("README.md", "# Mi Proyecto Python\n\nDescripción del proyecto."))
    print()
    
    print("3. Ver estado inicial:")
    print(git.git_status())
    print()
    
    print("4. Agregar archivos al staging:")
    print(git.git_add())
    print()
    
    print("5. Hacer primer commit:")
    print(git.git_commit("Agregar archivos iniciales"))
    print()
    
    print("6. Modificar archivo:")
    print(git.crear_archivo("main.py", "print('Hola Mundo')\nprint('Segunda línea')"))
    print()
    
    print("7. Ver estado después de modificación:")
    print(git.git_status())
    print()
    
    print("8. Agregar y commitear cambios:")
    print(git.git_add("main.py"))
    print(git.git_commit("Agregar segunda línea al programa"))
    print()
    
    print("9. Ver historial:")
    print(git.git_log())


def ejemplo_trabajo_con_ramas():
    """
    Ejemplo de trabajo con ramas
    """
    print("\n=== Trabajo con Ramas ===\n")
    
    # Crear simulador
    git = SimuladorGit("proyecto_ramas")
    
    # Inicializar y hacer commit inicial
    git.git_init()
    git.crear_archivo("app.py", "def main():\n    print('Aplicación principal')")
    git.git_add()
    git.git_commit("Commit inicial")
    
    print("1. Estado inicial:")
    print(git.git_branch())
    print()
    
    print("2. Crear rama de desarrollo:")
    print(git.git_branch("desarrollo"))
    print()
    
    print("3. Cambiar a rama de desarrollo:")
    print(git.git_checkout("desarrollo"))
    print()
    
    print("4. Hacer cambios en rama de desarrollo:")
    print(git.crear_archivo("app.py", "def main():\n    print('Aplicación principal')\n    print('Nueva funcionalidad')"))
    print(git.git_add())
    print(git.git_commit("Agregar nueva funcionalidad"))
    print()
    
    print("5. Ver historial en rama desarrollo:")
    print(git.git_log())
    print()
    
    print("6. Volver a rama main:")
    print(git.git_checkout("main"))
    print()
    
    print("7. Ver ramas disponibles:")
    print(git.git_branch())


def mejores_practicas_git():
    """
    Mostrar mejores prácticas de Git
    """
    print("\n=== Mejores Prácticas de Git ===\n")
    
    practicas = {
        "Mensajes de Commit": [
            "Usar mensajes descriptivos y claros",
            "Empezar con verbo en imperativo (Add, Fix, Update, etc.)",
            "Mantener primera línea bajo 50 caracteres",
            "Usar cuerpo del mensaje para explicar el 'por qué'"
        ],
        "Frecuencia de Commits": [
            "Hacer commits pequeños y frecuentes",
            "Cada commit debe representar un cambio lógico",
            "Evitar commits que mezclen múltiples funcionalidades"
        ],
        "Nomenclatura de Ramas": [
            "main/master: código de producción",
            "develop: rama de desarrollo principal",
            "feature/nombre-funcionalidad: nuevas características",
            "bugfix/nombre-error: correcciones de errores",
            "hotfix/nombre-urgente: correcciones urgentes"
        ],
        "Flujo de Trabajo": [
            "Siempre hacer pull antes de push",
            "Usar pull requests para revisión de código",
            "Mantener ramas actualizadas con la rama principal",
            "Eliminar ramas después de merge"
        ],
        "Archivos a Ignorar": [
            "Archivos temporales (.tmp, .log)",
            "Archivos de configuración local (.env)",
            "Dependencias (node_modules/, __pycache__/)",
            "Archivos de IDE (.vscode/, .idea/)",
            "Archivos de sistema (.DS_Store, Thumbs.db)"
        ]
    }
    
    for categoria, items in practicas.items():
        print(f"{categoria}:")
        for item in items:
            print(f"  • {item}")
        print()


def ejercicios_git():
    """
    Ejercicios prácticos de Git
    """
    print("\n=== Ejercicios Prácticos de Git ===\n")
    
    print("Ejercicio 1: Flujo de trabajo completo")
    print("Simula el siguiente flujo:")
    print("1. Crear repositorio para proyecto de calculadora")
    print("2. Agregar archivo principal con función básica")
    print("3. Hacer commit inicial")
    print("4. Crear rama 'feature-suma'")
    print("5. Implementar función de suma")
    print("6. Hacer commit en la rama")
    print("7. Volver a main y crear rama 'feature-resta'")
    print("8. Implementar función de resta")
    print("9. Hacer commit en la rama")
    print("10. Fusionar ambas ramas a main")
    print()
    
    print("Ejercicio 2: Resolución de conflictos")
    print("Simula un conflicto de merge:")
    print("1. Dos desarrolladores modifican la misma línea")
    print("2. Intentar fusionar las ramas")
    print("3. Resolver el conflicto manualmente")
    print("4. Completar el merge")
    print()
    
    print("Ejercicio 3: Git log y debugging")
    print("Práctica con comandos de historial:")
    print("• git log --oneline")
    print("• git log --graph")
    print("• git show <commit-hash>")
    print("• git diff HEAD~1")
    print()


def verificar_instalacion_git():
    """
    Verificar si Git está instalado y mostrar información
    """
    print("\n=== Verificación de Instalación Git ===\n")
    
    if ComandosGitReales.verificar_git_instalado():
        print("✓ Git está instalado correctamente")
        exito, version = ComandosGitReales.ejecutar_comando("git --version")
        if exito:
            print(f"Versión: {version.strip()}")
    else:
        print("✗ Git no está instalado o no está en el PATH")
        print("Para instalar Git:")
        print("• Windows: Descargar desde https://git-scm.com/")
        print("• macOS: brew install git")
        print("• Linux: sudo apt-get install git")
    
    print("\nComandos Git básicos disponibles:")
    comandos = ComandosGitReales.comandos_basicos()
    for comando, descripcion in list(comandos.items())[:10]:  # Mostrar solo los primeros 10
        print(f"  {comando:<25} - {descripcion}")


def main():
    """
    Función principal del módulo 4
    """
    print("MÓDULO 4: CONTROL DE VERSIONES CON GIT")
    print("=" * 50)
    
    # Verificar instalación
    verificar_instalacion_git()
    
    # Ejemplo básico
    ejemplo_flujo_trabajo_basico()
    
    # Trabajo con ramas
    ejemplo_trabajo_con_ramas()
    
    # Mejores prácticas
    mejores_practicas_git()
    
    # Ejercicios
    ejercicios_git()
    
    print("\n" + "=" * 50)
    print("¡Módulo 4 completado exitosamente!")
    print("\nPróximos pasos:")
    print("1. Instalar Git si no está instalado")
    print("2. Crear cuenta en GitHub/GitLab")
    print("3. Practicar con repositorios reales")
    print("4. Aprender sobre pull requests y colaboración")


if __name__ == "__main__":
    main() 