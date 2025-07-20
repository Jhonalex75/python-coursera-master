# requirements.txt
"""
Flask==2.0.1
Flask-SQLAlchemy==2.5.1
Flask-WTF==0.15.1
Pillow==8.3.1
python-dotenv==0.19.0
"""

# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipment.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Asegurar que existe el directorio de uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'dwg'}

db = SQLAlchemy(app)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(100), nullable=False)
    model_type = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    location = db.Column(db.String(200))
    maintenance_date = db.Column(db.DateTime, nullable=False)
    technician_name = db.Column(db.String(100))
    
    # Campos de la checklist
    visual_inspection = db.Column(db.Text)
    lubrication = db.Column(db.Text)
    electrical_components = db.Column(db.Text)
    mechanical_components = db.Column(db.Text)
    safety_systems = db.Column(db.Text)
    performance_test = db.Column(db.Text)
    
    # Campos del resumen
    issues_identified = db.Column(db.Text)
    actions_taken = db.Column(db.Text)
    parts_replaced = db.Column(db.Text)
    next_maintenance = db.Column(db.DateTime)
    
    # Campos para archivos
    images = db.Column(db.String(500))  # URLs separadas por comas
    documents = db.Column(db.String(500))  # URLs separadas por comas

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    equipments = Equipment.query.all()
    return render_template('index.html', equipments=equipments)

@app.route('/equipment/new', methods=['GET', 'POST'])
def new_equipment():
    if request.method == 'POST':
        equipment = Equipment(
            equipment_name=request.form['equipment_name'],
            model_type=request.form['model_type'],
            serial_number=request.form['serial_number'],
            location=request.form['location'],
            maintenance_date=datetime.strptime(request.form['maintenance_date'], '%Y-%m-%d'),
            technician_name=request.form['technician_name'],
            visual_inspection=request.form['visual_inspection'],
            lubrication=request.form['lubrication'],
            electrical_components=request.form['electrical_components'],
            mechanical_components=request.form['mechanical_components'],
            safety_systems=request.form['safety_systems'],
            performance_test=request.form['performance_test'],
            issues_identified=request.form['issues_identified'],
            actions_taken=request.form['actions_taken'],
            parts_replaced=request.form['parts_replaced'],
            next_maintenance=datetime.strptime(request.form['next_maintenance'], '%Y-%m-%d')
        )

        # Manejo de archivos
        images = []
        documents = []
        
        if 'images' in request.files:
            for file in request.files.getlist('images'):
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    images.append(filename)
        
        if 'documents' in request.files:
            for file in request.files.getlist('documents'):
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    documents.append(filename)
        
        equipment.images = ','.join(images)
        equipment.documents = ','.join(documents)

        db.session.add(equipment)
        db.session.commit()
        flash('Equipo registrado exitosamente')
        return redirect(url_for('index'))
    
    return render_template('new_equipment.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# templates/base.html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Mantenimiento de Equipos</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .form-group { margin-bottom: 1rem; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">Mantenimiento de Equipos</a>
        </div>
    </nav>
    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

# templates/index.html
{% extends "base.html" %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Equipos Registrados</h1>
    <a href="{{ url_for('new_equipment') }}" class="btn btn-primary">Nuevo Equipo</a>
</div>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Equipo</th>
                <th>Modelo</th>
                <th>Serie</th>
                <th>Ubicación</th>
                <th>Última Mantención</th>
                <th>Próxima Mantención</th>
            </tr>
        </thead>
        <tbody>
            {% for equipment in equipments %}
            <tr>
                <td>{{ equipment.equipment_name }}</td>
                <td>{{ equipment.model_type }}</td>
                <td>{{ equipment.serial_number }}</td>
                <td>{{ equipment.location }}</td>
                <td>{{ equipment.maintenance_date.strftime('%Y-%m-%d') }}</td>
                <td>{{ equipment.next_maintenance.strftime('%Y-%m-%d') }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}

# templates/new_equipment.html
{% extends "base.html" %}

{% block content %}
<h1 class="mb-4">Nuevo Registro de Equipo</h1>

<form method="POST" enctype="multipart/form-data">
    <div class="row">
        <div class="col-md-6">
            <h3>Información General</h3>
            <div class="form-group">
                <label>Nombre del Equipo</label>
                <input type="text" name="equipment_name" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Modelo/Tipo</label>
                <input type="text" name="model_type" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Número de Serie</label>
                <input type="text" name="serial_number" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Ubicación</label>
                <input type="text" name="location" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Fecha de Mantenimiento</label>
                <input type="date" name="maintenance_date" class="form-control" required>
            </div>
            <div class="form-group">
                <label>Nombre del Técnico</label>
                <input type="text" name="technician_name" class="form-control" required>
            </div>
        </div>

        <div class="col-md-6">
            <h3>Lista de Verificación</h3>
            <div class="form-group">
                <label>Inspección Visual</label>
                <textarea name="visual_inspection" class="form-control" rows="2"></textarea>
            </div>
            <div class="form-group">
                <label>Lubricación</label>
                <textarea name="lubrication" class="form-control" rows="2"></textarea>
            </div>
            <div class="form-group">
                <label>Componentes Eléctricos</label>
                <textarea name="electrical_components" class="form-control" rows="2"></textarea>
            </div>
            <div class="form-group">
                <label>Componentes Mecánicos</label>
                <textarea name="mechanical_components" class="form-control" rows="2"></textarea>
            </div>
            <div class="form-group">
                <label>Sistemas de Seguridad</label>
                <textarea name="safety_systems" class="form-control" rows="2"></textarea>
            </div>
            <div class="form-group">
                <label>Prueba de Rendimiento</label>
                <textarea name="performance_test" class="form-control" rows="2"></textarea>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <div class="col-md-12">
            <h3>Resumen de Mantenimiento</h3>
            <div class="form-group">
                <label>Problemas Identificados</label>
                <textarea name="issues_identified" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label>Acciones Tomadas</label>
                <textarea name="actions_taken" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label>Partes Reemplazadas</label>
                <textarea name="parts_replaced" class="form-control" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label>Próximo Mantenimiento</label>
                <input type="date" name="next_maintenance" class="form-control" required>
            </div>
        </div>
    </div>

    <div class="row mt-4">
        <div class="col-md-6">
            <h3>Archivos Adjuntos</h3>
            <div class="form-group">
                <label>Imágenes</label>
                <input type="file" name="images" class="form-control" multiple accept="image/*">
            </div>
            <div class="form-group">
                <label>Documentos (PDF, DWG)</label>
                <input type="file" name="documents" class="form-control" multiple accept=".pdf,.dwg">
            </div>
        </div>
    </div>

    <button type="submit" class="btn btn-primary mt-4">Guardar Registro</button>
</form>
{% endblock %}