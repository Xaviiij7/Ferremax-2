# FERREMAS 🛠️

### Proyecto Semestral - Integración de Plataformas

---

## Descripción

**FERREMAS** es una ferretería mayorista y minorista que encargó el desarrollo de una plataforma de e-commerce con funcionalidades específicas orientadas a mejorar la experiencia del usuario y optimizar la gestión de productos y pagos en línea.

---

## Funcionalidades

- Diseño intuitivo y accesible para los usuarios  
- API para visualización de productos  
- Integración con API de conversión de divisas  
- Pasarela de pago con Transbank  

---

## Tecnologías Utilizadas

- **Django**
- **Django REST Framework**
- **Transbank SDK**
- **Bootstrap 5**

---

## Instalación

Sigue estos pasos para ejecutar el proyecto correctamente:

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git

2. **Cambia al directorio del proyecto:**
```bash
   cd tu-repositorio
```
3. **Elimina cualquier carpeta env anterior si existe:**
   ```bash
      # En Linux/macOS
      rm -rf env
      
      # En Windows
      rmdir /s env
   
4. **Crea un entorno virtual:**
```bash
   python -m venv env
```
5. **Activa el entorno virtual:**
```bash
   En Linux/macOS:
   source env/bin/activate
   
   En Windows:
   .\env\Scripts\activate

```
6. **Instala las dependencias necesarias:**
```bash
   pip install -r requirements.txt
```
7. **Si el archivo requirements.txt no contiene todas las librerías necesarias, puedes instalarlas manualmente:**
```
   pip install django
   pip install djangorestframework
   pip install requests
   pip install Pillow
```
8. **Ejecuta el servidor:**
```bash
   python manage.py runserver
```

## API
- API de Productos
- API de Cambio de Divisa
- API de Pago Transbank
