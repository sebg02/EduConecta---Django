# EduConecta - Django

EduConecta es una plataforma web desarrollada con Django, diseñada para conectar profesores y estudiantes. Los usuarios pueden registrarse, gestionar clases, definir horarios de disponibilidad, y realizar solicitudes para agendar clases. El proyecto incluye funcionalidades de autenticación, roles diferenciados (profesor y estudiante), y manejo de datos relacionados con clases y ubicaciones.


## Funcionalidades principales  

### Usuarios y Roles  
- **Usuarios Profesores**  
  - Pueden crear, editar y gestionar clases.  
  - Definen ubicaciones y horarios de disponibilidad para sus clases.  
- **Usuarios Estudiantes**  
  - Pueden buscar clases, agendar solicitudes y administrar intereses relacionados.  

### Gestión de Clases  
- Profesores pueden:  
  - Crear clases con datos como precio, categoría, descripción y ubicación.  
  - Definir disponibilidad mediante formularios.  
  - Editar clases existentes.  

### Solicitudes de Clases  
- Los estudiantes pueden realizar solicitudes para clases disponibles.  
- Los profesores pueden ver el estado de las solicitudes y responderlas.  

### Sistema de Ubicaciones  
- Los profesores pueden compartir ubicaciones con otros.  
- Las clases tienen una ubicación asignada mediante una relación muchos-a-uno.  

### Autenticación y Seguridad  
- Los usuarios inician sesión y se les asigna automáticamente un rol (profesor o estudiante) tras el registro.  
- Acceso restringido para evitar que los usuarios editen o visualicen datos que no les pertenecen.  


## Tecnologías utilizadas  

- **Backend**: Django 5.1.1  
- **Frontend**: Bootstrap 5  
- **Base de datos**: SQLite
- **Autenticación**: Sistema de usuarios y grupos integrado de Django  

