"""
Ventana de Login
Gestiona la autenticación del usuario
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class LoginWindow(QDialog):
    """Ventana de Login"""
    
    login_successful = pyqtSignal(object)  # Emite el usuario logueado
    
    def __init__(self, mediator, parent=None):
        super().__init__(parent)
        self.mediator = mediator
        self.current_user = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.setWindowTitle("Login - Gestor de Pedidos")
        self.setGeometry(100, 100, 400, 300)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("Gestor de Pedidos")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Inicia sesión para continuar")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(15)
        
        # Usuario
        username_label = QLabel("Nombre de usuario:")
        layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Ingresa tu usuario")
        layout.addWidget(self.username_input)
        
        # Contraseña
        password_label = QLabel("Contraseña:")
        layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Ingresa tu contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        layout.addSpacing(15)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        login_btn = QPushButton("Iniciar Sesión")
        login_btn.setObjectName("primaryBtn")
        login_btn.clicked.connect(self.do_login)
        buttons_layout.addWidget(login_btn)
        
        register_btn = QPushButton("Registrarse")
        register_btn.clicked.connect(self.show_register)
        buttons_layout.addWidget(register_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def do_login(self):
        """Realiza el login"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Validación", "Por favor completa todos los campos")
            return
        
        success, message, user = self.mediator.auth_service.login(username, password)
        
        if success:
            self.current_user = user
            self.login_successful.emit(user)
            self.accept()
        else:
            QMessageBox.critical(self, "Error de Login", message)
            self.password_input.clear()
    
    def show_register(self):
        """Muestra la ventana de registro"""
        dialog = RegisterDialog(self.mediator, self)
        dialog.exec()


class RegisterDialog(QDialog):
    """Diálogo de Registro"""
    
    def __init__(self, mediator, parent=None):
        super().__init__(parent)
        self.mediator = mediator
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        self.setWindowTitle("Registrarse - Gestor de Pedidos")
        self.setGeometry(100, 100, 450, 400)
        self.setModal(True)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Título
        title = QLabel("Crear Nueva Cuenta")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        # Usuario
        username_label = QLabel("Nombre de usuario:")
        layout.addWidget(username_label)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Elige tu usuario")
        layout.addWidget(self.username_input)
        
        # Email
        email_label = QLabel("Correo electrónico:")
        layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("tu@email.com")
        layout.addWidget(self.email_input)
        
        # Contraseña
        password_label = QLabel("Contraseña:")
        layout.addWidget(password_label)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña segura")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        # Confirmar contraseña
        confirm_label = QLabel("Confirmar contraseña:")
        layout.addWidget(confirm_label)
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Repite tu contraseña")
        self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_input)
        
        # Rol de usuario
        role_label = QLabel("Tipo de usuario:")
        layout.addWidget(role_label)
        self.role_combo = QComboBox()
        from utils.constants import ROLE_CLIENT, ROLE_MANAGER, ROLE_ADMIN, ROLES
        self.role_combo.addItem(ROLES[ROLE_CLIENT], ROLE_CLIENT)
        self.role_combo.addItem(ROLES[ROLE_MANAGER], ROLE_MANAGER)
        self.role_combo.addItem(ROLES[ROLE_ADMIN], ROLE_ADMIN)
        self.role_combo.setCurrentIndex(0)  # Por defecto Cliente
        layout.addWidget(self.role_combo)
        
        # Nota sobre roles
        note = QLabel("Nota: Los roles de Gerente y Admin requieren autorización")
        note_font = QFont()
        note_font.setPointSize(9)
        note_font.setItalic(True)
        note.setFont(note_font)
        note.setStyleSheet("color: #888888;")
        layout.addWidget(note)
        
        layout.addSpacing(10)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        register_btn = QPushButton("Registrarse")
        register_btn.setObjectName("successBtn")
        register_btn.clicked.connect(self.do_register)
        buttons_layout.addWidget(register_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def do_register(self):
        """Realiza el registro"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()
        role = self.role_combo.currentData()  # Obtener rol seleccionado
        
        if not all([username, email, password, confirm]):
            QMessageBox.warning(self, "Validación", "Por favor completa todos los campos")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Validación", "Las contraseñas no coinciden")
            self.password_input.clear()
            self.confirm_input.clear()
            return
        
        # Validar que solo Admin puede crear otros Admin/Gerente
        from utils.constants import ROLE_ADMIN, ROLE_MANAGER
        if role in [ROLE_ADMIN, ROLE_MANAGER]:
            QMessageBox.warning(
                self, 
                "Restricción de Seguridad",
                "Solo administradores existentes pueden crear cuentas de Gerente o Admin.\n\n"
                "Se creará como Cliente por seguridad."
            )
            role = "cliente"
        
        success, message, user = self.mediator.auth_service.register(
            username, email, password, role
        )
        
        if success:
            from utils.constants import ROLES
            QMessageBox.information(
                self, 
                "Éxito", 
                f"¡Cuenta creada! Bienvenido {username}\n"
                f"Rol: {ROLES.get(role, role)}"
            )
            self.accept()
        else:
            QMessageBox.critical(self, "Error de Registro", message)
