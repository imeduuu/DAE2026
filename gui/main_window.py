"""
Ventana principal de la aplicación
Gestiona el flujo principal y la navegación entre vistas
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QMessageBox, QStackedWidget,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                             QDialog, QLineEdit, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
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
        
        self.stats_widgets = {}
        
        # Crear vistas PRIMERO (antes del header)
        self.stacked = QStackedWidget()
        self.dashboard_view = self.create_dashboard()
        self.orders_view = self.create_orders_view()
        # Vista de usuarios solo para Admin y Gerente
        from utils.constants import ROLE_ADMIN, ROLE_MANAGER
        self.users_view = self.create_users_view() if self.current_user.role in [ROLE_ADMIN, ROLE_MANAGER] else None
        # Vista de gestión de roles solo para Admin
        self.roles_management_view = self.create_roles_management_view() if self.current_user.role == ROLE_ADMIN else None
        
        self.stacked.addWidget(self.dashboard_view)
        self.stacked.addWidget(self.orders_view)
        if self.users_view:
            self.stacked.addWidget(self.users_view)
        if self.roles_management_view:
            self.stacked.addWidget(self.roles_management_view)
        
        # Barra superior (DESPUÉS de crear las vistas)
        header = self.create_header()
        layout.addWidget(header)
        
        # Contenido principal
        layout.addWidget(self.stacked)
        
        central_widget.setLayout(layout)
        
        # Iniciar timer para transiciones automáticas de pedidos
        self._start_order_transition_timer()
        
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
        
        if self.roles_management_view:
            roles_btn = QPushButton("⚙️ Gestión de Roles")
            roles_btn.clicked.connect(lambda: self.stacked.setCurrentWidget(self.roles_management_view))
            nav_layout.addWidget(roles_btn)
        
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
        
        self.refresh_dashboard_stats()
        
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
        
        self.stats_widgets[label] = value_widget
        
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
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            "ID", "Usuario", "Descripción", "Estado", "Creado", "Actualizado", "Acciones"
        ])
        
        header = self.orders_table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        
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
        orders = self.mediator.order_service.get_user_orders(
            self.current_user.id,
            self.current_user.role
        )
        self.orders_table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(order.id)))
            self.orders_table.setItem(row, 1, QTableWidgetItem(str(order.user_id)))
            self.orders_table.setItem(row, 2, QTableWidgetItem(order.description))
            self.orders_table.setItem(row, 3, QTableWidgetItem(order.status))
            self.orders_table.setItem(row, 4, QTableWidgetItem(str(order.created_at)[:19] if order.created_at else "-"))
            self.orders_table.setItem(row, 5, QTableWidgetItem(str(order.updated_at)[:19] if order.updated_at else "-"))
            
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)
            
            if self.current_user.role in [ROLE_ADMIN] or order.user_id == self.current_user.id:
                update_btn = QPushButton("Actualizar")
                update_btn.setObjectName("secondaryBtn")
                update_btn.clicked.connect(
                    lambda checked, order_id=order.id: self.show_update_status_dialog(order_id)
                )
                action_layout.addWidget(update_btn)
            
            action_layout.addStretch()
            action_widget.setLayout(action_layout)
            self.orders_table.setCellWidget(row, 6, action_widget)
        
        self.refresh_dashboard_stats()
    
    def refresh_dashboard_stats(self):
        """Actualiza los valores del panel de estadísticas"""
        orders = self.mediator.order_service.get_user_orders(
            self.current_user.id,
            self.current_user.role
        )
        total = len(orders)
        pending = sum(1 for order in orders if order.status == ORDER_STATUS_PENDING)
        delivered = sum(1 for order in orders if order.status == ORDER_STATUS_DELIVERED)
        
        if "📦 Pedidos Totales" in self.stats_widgets:
            self.stats_widgets["📦 Pedidos Totales"].setText(str(total))
        if "⏳ Pendientes" in self.stats_widgets:
            self.stats_widgets["⏳ Pendientes"].setText(str(pending))
        if "✅ Completados" in self.stats_widgets:
            self.stats_widgets["✅ Completados"].setText(str(delivered))
    
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

    def create_roles_management_view(self):
        """Crea la vista de gestión de roles (solo para admin)"""
        from utils.constants import ROLE_ADMIN
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("⚙️ Gestión de Roles")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Descripción
        desc = QLabel("Administra los roles y permisos de los usuarios del sistema")
        desc_font = QFont()
        desc_font.setPointSize(9)
        desc_font.setItalic(True)
        desc.setFont(desc_font)
        layout.addWidget(desc)

        layout.addSpacing(10)

        # Barra de búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("🔍 Buscar usuario:")
        search_layout.addWidget(search_label)
        
        self.roles_search_input = QLineEdit()
        self.roles_search_input.setPlaceholderText("Usuario, Email o Rol...")
        self.roles_search_input.textChanged.connect(self.filter_roles_table)
        search_layout.addWidget(self.roles_search_input)
        search_layout.addSpacing(10)

        clear_search_btn = QPushButton("✕ Limpiar")
        clear_search_btn.setMaximumWidth(100)
        clear_search_btn.clicked.connect(lambda: self.roles_search_input.clear())
        search_layout.addWidget(clear_search_btn)

        layout.addLayout(search_layout)
        layout.addSpacing(10)

        # Tabla de roles
        self.roles_table = QTableWidget()
        self.roles_table.setColumnCount(6)
        self.roles_table.setHorizontalHeaderLabels([
            "ID", "Usuario", "Email", "Rol Actual", "Creado", "Acciones"
        ])

        header = self.roles_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        self.refresh_roles_table()
        layout.addWidget(self.roles_table)

        # Botones de acción
        buttons_layout = QHBoxLayout()

        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.clicked.connect(self.refresh_roles_table)
        buttons_layout.addWidget(refresh_btn)

        buttons_layout.addStretch()

        layout.addLayout(buttons_layout)

        widget.setLayout(layout)
        return widget

    def refresh_roles_table(self):
        """Actualiza la tabla de gestión de roles"""
        from utils.constants import ROLES
        
        users = self.mediator.user_repository.find_all()
        self.roles_table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.roles_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
            self.roles_table.setItem(row, 1, QTableWidgetItem(user.username))
            self.roles_table.setItem(row, 2, QTableWidgetItem(user.email))
            self.roles_table.setItem(row, 3, QTableWidgetItem(ROLES.get(user.role, user.role)))
            self.roles_table.setItem(row, 4, QTableWidgetItem(str(user.created_at)[:10] if user.created_at else "-"))

            # Botón de cambiar rol
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(0, 0, 0, 0)

            change_role_btn = QPushButton("Cambiar Rol")
            change_role_btn.setObjectName("secondaryBtn")
            change_role_btn.clicked.connect(
                lambda checked, user_id=user.id: self.show_role_change_dialog(user_id)
            )
            action_layout.addWidget(change_role_btn)
            action_layout.addStretch()

            action_widget.setLayout(action_layout)
            self.roles_table.setCellWidget(row, 5, action_widget)

    def filter_roles_table(self):
        """Filtra la tabla de roles según la búsqueda"""
        search_text = self.roles_search_input.text().lower()

        for row in range(self.roles_table.rowCount()):
            # Obtener datos de la fila
            username = self.roles_table.item(row, 1).text() if self.roles_table.item(row, 1) else ""
            email = self.roles_table.item(row, 2).text() if self.roles_table.item(row, 2) else ""
            role = self.roles_table.item(row, 3).text() if self.roles_table.item(row, 3) else ""

            # Mostrar o ocultar fila según búsqueda
            match = (search_text in username.lower() or 
                    search_text in email.lower() or 
                    search_text in role.lower())
            self.roles_table.setRowHidden(row, not match)

    def show_role_change_dialog(self, user_id: int):
        """Muestra el diálogo para cambiar el rol de un usuario"""
        from utils.constants import ROLE_ADMIN
        
        user = self.mediator.user_repository.find_by_id(user_id)
        if not user:
            QMessageBox.critical(self, "Error", "Usuario no encontrado")
            return

        # Validación de seguridad
        if user_id == self.current_user.id:
            QMessageBox.warning(
                self, 
                "No permitido",
                "No puedes cambiar tu propio rol"
            )
            return

        dialog = RoleChangeDialog(self.mediator, user, self.current_user, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_roles_table()
            # Si el usuario actual perdió permisos, refrescar la sesión
            updated_user = self.mediator.user_repository.find_by_id(self.current_user.id)
            if updated_user:
                self.current_user = updated_user

    def show_new_order_dialog(self):
        """Muestra el diálogo para crear un nuevo pedido"""
        dialog = NewOrderDialog(self.current_user, self.mediator, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_orders_table()
            self.refresh_dashboard_stats()

    def show_update_status_dialog(self, order_id: int):
        """Muestra el diálogo para actualizar el estado de un pedido"""
        order = self.mediator.order_repository.find_by_id(order_id)
        if not order:
            QMessageBox.critical(self, "Error", "Pedido no encontrado")
            return

        dialog = UpdateStatusDialog(self.mediator, order, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_orders_table()
            self.refresh_dashboard_stats()

    def _start_order_transition_timer(self):
        """Inicia el timer para procesar transiciones automáticas de pedidos"""
        self.order_transition_timer = QTimer()
        # Ejecutar cada 30 segundos (30,000 ms)
        self.order_transition_timer.timeout.connect(self._process_order_transitions)
        self.order_transition_timer.start(30000)

    def _process_order_transitions(self):
        """Procesa las transiciones automáticas de pedidos"""
        try:
            transitions = self.mediator.order_service.process_automatic_transitions()
            if transitions > 0:
                # Si hay cambios, actualizar las tablas visibles
                self.refresh_orders_table()
                self.refresh_dashboard_stats()
        except Exception as e:
            print(f"Error procesando transiciones: {e}")

    def do_logout(self):
        """Realiza el logout"""
        reply = QMessageBox.question(self, "Confirmar", "¿Deseas cerrar sesión?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.setCentralWidget(QWidget())
            self.show_login()


class NewOrderDialog(QDialog):
    """Diálogo para crear un nuevo pedido"""

    def __init__(self, current_user, mediator, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.mediator = mediator
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Nuevo Pedido")
        self.setModal(True)
        self.setFixedSize(500, 320)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel("Describe tu pedido:")
        layout.addWidget(label)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Ingresa los detalles del pedido...")
        layout.addWidget(self.description_input)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        create_btn = QPushButton("Crear pedido")
        create_btn.setObjectName("primaryBtn")
        create_btn.clicked.connect(self._create_order)
        buttons_layout.addWidget(create_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def _create_order(self):
        description = self.description_input.toPlainText().strip()
        success, message, order = self.mediator.order_service.create_order(
            self.current_user.id,
            description
        )
        if success:
            QMessageBox.information(self, "Pedido creado", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


class UpdateStatusDialog(QDialog):
    """Diálogo para cambiar el estado de un pedido"""

    def __init__(self, mediator, order, parent=None):
        super().__init__(parent)
        self.mediator = mediator
        self.order = order
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle(f"Actualizar estado - Pedido #{self.order.id}")
        self.setModal(True)
        self.setFixedSize(500, 260)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel(f"Pedido #{self.order.id} - {self.order.description}")
        label.setWordWrap(True)
        layout.addWidget(label)

        status_label = QLabel("Selecciona el nuevo estado:")
        layout.addWidget(status_label)

        self.status_combo = QComboBox()
        self.status_combo.addItem("Pendiente", ORDER_STATUS_PENDING)
        self.status_combo.addItem("Confirmado", ORDER_STATUS_CONFIRMED)
        self.status_combo.addItem("Enviado", ORDER_STATUS_SHIPPED)
        self.status_combo.addItem("Entregado", ORDER_STATUS_DELIVERED)
        self.status_combo.addItem("Cancelado", ORDER_STATUS_CANCELLED)
        self.status_combo.setCurrentText(self.order.status.capitalize())
        layout.addWidget(self.status_combo)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        update_btn = QPushButton("Actualizar estado")
        update_btn.setObjectName("primaryBtn")
        update_btn.clicked.connect(self._update_status)
        buttons_layout.addWidget(update_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def _update_status(self):
        status = self.status_combo.currentData()
        success, message = self.mediator.order_service.update_order_status(self.order.id, status)
        if success:
            QMessageBox.information(self, "Éxito", message)
            self.accept()
        else:
            QMessageBox.warning(self, "Error", message)


class RoleChangeDialog(QDialog):
    """Diálogo para cambiar el rol de un usuario"""

    def __init__(self, mediator, user, current_user, parent=None):
        super().__init__(parent)
        self.mediator = mediator
        self.user = user
        self.current_user = current_user
        self._setup_ui()

    def _setup_ui(self):
        from utils.constants import ROLE_ADMIN, ROLE_MANAGER, ROLE_CLIENT, ROLES
        
        self.setWindowTitle(f"Cambiar rol - {self.user.username}")
        self.setModal(True)
        self.setFixedSize(600, 350)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Información del usuario
        title = QLabel(f"Cambiar rol de: {self.user.username}")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        layout.addSpacing(10)

        # Información actual
        info_layout = QHBoxLayout()
        email_label = QLabel(f"📧 {self.user.email}")
        info_layout.addWidget(email_label)
        role_label = QLabel(f"👤 Rol actual: {ROLES.get(self.user.role, self.user.role)}")
        info_label = QLabel(f"ID: {self.user.id}")
        info_layout.addWidget(role_label)
        info_layout.addWidget(info_label)
        info_layout.addStretch()
        layout.addLayout(info_layout)

        layout.addSpacing(15)

        # Combinador de roles
        role_label = QLabel("Nuevo rol:")
        layout.addWidget(role_label)

        self.role_combo = QComboBox()
        self.role_combo.addItem(ROLES[ROLE_ADMIN], ROLE_ADMIN)
        self.role_combo.addItem(ROLES[ROLE_MANAGER], ROLE_MANAGER)
        self.role_combo.addItem(ROLES[ROLE_CLIENT], ROLE_CLIENT)
        self.role_combo.setCurrentText(ROLES.get(self.user.role, self.user.role))
        layout.addWidget(self.role_combo)

        # Campo de motivo
        layout.addSpacing(10)
        reason_label = QLabel("Motivo del cambio (opcional):")
        layout.addWidget(reason_label)

        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText("Ingresa el motivo del cambio...")
        self.reason_input.setMaximumHeight(80)
        layout.addWidget(self.reason_input)

        # Área de advertencia
        layout.addSpacing(10)
        warning_label = QLabel("⚠️ Esta acción cambiará los permisos del usuario.")
        warning_font = QFont()
        warning_font.setPointSize(9)
        warning_font.setItalic(True)
        warning_label.setFont(warning_font)
        layout.addWidget(warning_label)

        layout.addStretch()

        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        confirm_btn = QPushButton("✓ Confirmar cambio")
        confirm_btn.setObjectName("primaryBtn")
        confirm_btn.clicked.connect(self._confirm_change)
        buttons_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("✗ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def _confirm_change(self):
        from utils.constants import ROLES
        
        new_role = self.role_combo.currentData()
        
        # Si el nuevo rol es el mismo, no hacer nada
        if new_role == self.user.role:
            QMessageBox.information(self, "Sin cambios", "El nuevo rol es igual al actual")
            return

        # Mostrar confirmación
        reply = QMessageBox.question(
            self,
            "Confirmar cambio de rol",
            f"¿Confirmar cambio de {ROLES.get(self.user.role)} a {ROLES.get(new_role)}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            reason = self.reason_input.toPlainText().strip()
            success, message = self.mediator.user_service.change_user_role(
                self.user.id,
                new_role,
                self.current_user.id,
                reason
            )

            if success:
                QMessageBox.information(self, "Éxito", message)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", message)
