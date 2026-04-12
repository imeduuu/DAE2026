"""
Ventana principal de la aplicación
Gestiona el flujo principal y la navegación entre vistas
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QMessageBox, QStackedWidget,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QDialog, QLineEdit, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon
from gui.login_window import LoginWindow
from utils.constants import ROLE_ADMIN, ORDER_STATUS_PENDING, ORDER_STATUS_CONFIRMED, ORDER_STATUS_SHIPPED, ORDER_STATUS_DELIVERED, ORDER_STATUS_CANCELLED


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""
    
    def __init__(self, mediator):
        super().__init__()
        self.mediator = mediator
        self.current_user = None
        self.setWindowTitle("Gestor de Pedidos")
        self.setGeometry(100, 100, 1000, 700)
        
        # Mostrar login
        self.show_login()
    
    def show_login(self):
        """Muestra la ventana de login"""
        login = LoginWindow(self.mediator, self)
        if login.exec() == QDialog.DialogCode.Accepted:
            self.current_user = login.current_user
            self.setup_main_ui()
        else:
            self.close()
    
    def setup_main_ui(self):
        """Configura la interfaz principal después del login"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Crear vistas PRIMERO (antes del header)
        self.stacked = QStackedWidget()
        self.dashboard_view = self.create_dashboard()
        self.orders_view = self.create_orders_view()
        # Vista de usuarios solo para Admin y Gerente
        from utils.constants import ROLE_ADMIN, ROLE_MANAGER
        self.users_view = self.create_users_view() if self.current_user.role in [ROLE_ADMIN, ROLE_MANAGER] else None
        
        self.stacked.addWidget(self.dashboard_view)
        self.stacked.addWidget(self.orders_view)
        if self.users_view:
            self.stacked.addWidget(self.users_view)
        
        # Barra superior (DESPUÉS de crear las vistas)
        header = self.create_header()
        layout.addWidget(header)
        
        # Contenido principal
        layout.addWidget(self.stacked)
        
        central_widget.setLayout(layout)
        self.show()
    
    def create_header(self):
        """Crea la barra de encabezado"""
        header = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Logo/Título
        title = QLabel("📊 Gestor de Pedidos")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Información del usuario
        user_info = QLabel(f"👤 {self.current_user.username} ({self.current_user.role})")
        layout.addWidget(user_info)
        
        layout.addStretch()
        
        # Botones de navegación
        nav_layout = QHBoxLayout()
        
        dashboard_btn = QPushButton("📈 Panel")
        dashboard_btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.dashboard_view))
        nav_layout.addWidget(dashboard_btn)
        
        orders_btn = QPushButton("📦 Pedidos")
        orders_btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.orders_view))
        nav_layout.addWidget(orders_btn)
        
        if self.users_view:
            users_btn = QPushButton("👥 Usuarios")
            users_btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.users_view))
            nav_layout.addWidget(users_btn)
        
        logout_btn = QPushButton("🚪 Salir")
        logout_btn.setObjectName("dangerBtn")
        logout_btn.clicked.connect(self.do_logout)
        nav_layout.addWidget(logout_btn)
        
        layout.addLayout(nav_layout)
        
        header.setLayout(layout)
        header.setStyleSheet("background-color: #2d2d2d; border-bottom: 1px solid #404040;")
        
        return header
    
    def create_dashboard(self):
        """Crea el panel principal"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Bienvenida
        welcome = QLabel(f"¡Bienvenido {self.current_user.username}!")
        welcome_font = QFont()
        welcome_font.setPointSize(16)
        welcome_font.setBold(True)
        welcome.setFont(welcome_font)
        layout.addWidget(welcome)
        
        layout.addSpacing(20)
        
        # Estadísticas (placeholder)
        stats_layout = QHBoxLayout()
        
        stats = [
            ("📦 Pedidos Totales", "0"),
            ("⏳ Pendientes", "0"),
            ("✅ Completados", "0"),
            ("👥 Usuarios", str(len(self.mediator.user_repository.find_all())))
        ]
        
        for label, value in stats:
            stat_widget = self.create_stat_card(label, value)
            stats_layout.addWidget(stat_widget)
        
        layout.addLayout(stats_layout)
        
        layout.addSpacing(30)
        
        # Acciones rápidas
        actions_label = QLabel("Acciones Rápidas")
        actions_font = QFont()
        actions_font.setPointSize(12)
        actions_font.setBold(True)
        actions_label.setFont(actions_font)
        layout.addWidget(actions_label)
        
        actions_layout = QHBoxLayout()
        
        new_order = QPushButton("➕ Crear Nuevo Pedido")
        new_order.setObjectName("primaryBtn")
        new_order.clicked.connect(self.show_new_order_dialog)
        actions_layout.addWidget(new_order)
        
        view_orders = QPushButton("📋 Ver Mis Pedidos")
        view_orders.clicked.connect(lambda: self.stacked.setCurrentWidget(self.orders_view))
        actions_layout.addWidget(view_orders)
        
        layout.addLayout(actions_layout)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_stat_card(self, label, value):
        """Crea una tarjeta de estadística"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        label_widget = QLabel(label)
        label_font = QFont()
        label_font.setPointSize(11)
        label_widget.setFont(label_font)
        layout.addWidget(label_widget)
        
        value_widget = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_widget.setFont(value_font)
        layout.addWidget(value_widget)
        
        widget.setLayout(layout)
        widget.setStyleSheet("background-color: #2d2d2d; border-radius: 8px; border: 1px solid #404040;")
        
        return widget
    
    def create_orders_view(self):
        """Crea la vista de pedidos"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("📦 Mis Pedidos")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabla de pedidos
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Descripción", "Estado", "Creado", "Acciones"])
        
        header = self.orders_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        self.refresh_orders_table()
        layout.addWidget(self.orders_table)
        
        # Botón para crear
        actions_layout = QHBoxLayout()
        new_btn = QPushButton("➕ Crear Nuevo Pedido")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self.show_new_order_dialog)
        actions_layout.addWidget(new_btn)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_orders_table(self):
        """Actualiza la tabla de pedidos"""
        # Aquí iría la lógica para obtener pedidos del repositorio
        # Por ahora es un placeholder
        self.orders_table.setRowCount(0)
    
    def create_users_view(self):
        """Crea la vista de usuarios (solo para admin)"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("👥 Gestión de Usuarios")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabla de usuarios
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Usuario", "Email", "Rol", "Creado"])
        
        header = self.users_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        self.refresh_users_table()
        layout.addWidget(self.users_table)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.clicked.connect(self.refresh_users_table)
        buttons_layout.addWidget(refresh_btn)
        
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        widget.setLayout(layout)
        return widget
    
    def refresh_users_table(self):
        """Actualiza la tabla de usuarios"""
        users = self.mediator.user_repository.find_all()
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.users_table.setItem(row, 1, QTableWidgetItem(user.username))
            self.users_table.setItem(row, 2, QTableWidgetItem(user.email))
            self.users_table.setItem(row, 3, QTableWidgetItem(user.role))
            self.users_table.setItem(row, 4, QTableWidgetItem(str(user.created_at)[:10] if user.created_at else "-"))
    
    def show_new_order_dialog(self):
        """Muestra el diálogo para crear un nuevo pedido"""
        QMessageBox.information(self, "Información", "Funcionalidad de pedidos próximamente disponible")
    
    def do_logout(self):
        """Realiza el logout"""
        reply = QMessageBox.question(self, "Confirmar", "¿Deseas cerrar sesión?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.setCentralWidget(QWidget())
            self.show_login()
