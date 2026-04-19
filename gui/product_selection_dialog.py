"""
Diálogo para seleccionar y configurar productos en un pedido
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QSpinBox, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QMessageBox, QHeaderView, QWidget, QAbstractItemView
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QColor, QFont
from typing import Dict, List, Tuple


class ProductSelectionDialog(QDialog):
    """Diálogo para seleccionar productos y cantidades para un pedido"""
    
    def __init__(self, products_tree: Dict, parent=None):
        """
        Inicializa el diálogo
        
        Args:
            products_tree: Diccionario con categorías y productos
            parent: Widget padre
        """
        super().__init__(parent)
        self.products_tree = products_tree
        self.selected_products = {}  # {product_id: {"name": "", "price": 0, "quantity": 0}}
        
        self.setWindowTitle("📦 Seleccionar Productos")
        self.setGeometry(100, 100, 1000, 600)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QHBoxLayout()
        
        # Lado izquierdo: Árbol de categorías/productos
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("📂 Categorías y Productos:"))
        
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("Producto | Modelo | Precio | Stock")
        self.tree_widget.itemSelectionChanged.connect(self.on_product_selected)
        self._populate_tree()
        left_layout.addWidget(self.tree_widget)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        layout.addWidget(left_widget, 2)
        
        # Lado derecho: Cantidad seleccionada
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("🛒 Carrito de Compra:"))
        
        # Tabla de productos seleccionados
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(6)
        self.cart_table.setHorizontalHeaderLabels(
            ["Categoría", "Producto", "Modelo", "Precio", "Cantidad", "Acción"]
        )
        self.cart_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.cart_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        right_layout.addWidget(self.cart_table, 1)
        
        # Controles
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Cantidad:"))
        
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setMinimum(1)
        self.quantity_spinbox.setMaximum(999)
        self.quantity_spinbox.setValue(1)
        controls_layout.addWidget(self.quantity_spinbox)
        
        self.add_button = QPushButton("➕ Agregar al Carrito")
        self.add_button.clicked.connect(self.add_to_cart)
        self.add_button.setEnabled(False)
        controls_layout.addWidget(self.add_button)
        
        right_layout.addLayout(controls_layout)
        
        # Total
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("💰 Total:"))
        self.total_label = QLabel("$0.00")
        font = self.total_label.font()
        font.setPointSize(12)
        font.setBold(True)
        self.total_label.setFont(font)
        self.total_label.setStyleSheet("color: #00ff00; font-weight: bold;")
        total_layout.addWidget(self.total_label)
        total_layout.addStretch()
        right_layout.addLayout(total_layout)
        
        # Botones finales
        buttons_layout = QHBoxLayout()
        
        self.confirm_button = QPushButton("✅ Confirmar Pedido")
        self.confirm_button.clicked.connect(self.accept)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
        """)
        
        self.cancel_button = QPushButton("❌ Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.confirm_button)
        buttons_layout.addWidget(self.cancel_button)
        right_layout.addLayout(buttons_layout)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        layout.addWidget(right_widget, 1)
        
        self.setLayout(layout)
    
    def _populate_tree(self):
        """Llena el árbol con categorías y productos"""
        for category_name, products in self.products_tree.items():
            category_item = QTreeWidgetItem(self.tree_widget)
            category_item.setText(0, f"📂 {category_name}")
            category_item.setFont(0, self._get_bold_font())
            category_item.setForeground(0, QColor("#0099ff"))
            category_item.setExpanded(True)
            
            for product in products:
                product_item = QTreeWidgetItem(category_item)
                # Formato: "Producto | Modelo | $Precio | Stock: X"
                text = (f"💻 {product['name']} | {product['model']} | "
                       f"${product['price']:.2f} | Stock: {product['stock']}")
                product_item.setText(0, text)
                product_item.setData(0, Qt.ItemDataRole.UserRole, product['id'])
                product_item.setData(0, Qt.ItemDataRole.UserRole + 1, product)
                
                if product['stock'] <= 0:
                    product_item.setForeground(0, QColor("#ff0000"))
                    product_item.setDisabled(True)
    
    def _get_bold_font(self) -> QFont:
        """Retorna una fuente en negrita"""
        font = QFont()
        font.setBold(True)
        return font
    
    def on_product_selected(self):
        """Se ejecuta cuando se selecciona un producto"""
        current_item = self.tree_widget.currentItem()
        
        if not current_item or not current_item.parent():  # Si es categoría o nada
            self.add_button.setEnabled(False)
            return
        
        # Verificar que tiene datos de producto
        product_id = current_item.data(0, Qt.ItemDataRole.UserRole)
        
        if product_id is None:
            self.add_button.setEnabled(False)
            return
        
        self.add_button.setEnabled(True)
    
    def add_to_cart(self):
        """Agrega el producto seleccionado al carrito"""
        current_item = self.tree_widget.currentItem()
        
        if not current_item or not current_item.parent():
            QMessageBox.warning(self, "Selección Inválida", "Por favor, selecciona un producto.")
            return
        
        product_id = current_item.data(0, Qt.ItemDataRole.UserRole)
        product_data = current_item.data(0, Qt.ItemDataRole.UserRole + 1)
        quantity = self.quantity_spinbox.value()
        
        if product_data['stock'] < quantity:
            QMessageBox.warning(
                self,
                "Stock Insuficiente",
                f"Solo hay {product_data['stock']} unidades disponibles."
            )
            return
        
        if product_id in self.selected_products:
            # Actualizar cantidad
            self.selected_products[product_id]['quantity'] += quantity
        else:
            # Agregar nuevo producto
            self.selected_products[product_id] = {
                'name': product_data['name'],
                'model': product_data['model'],
                'price': product_data['price'],
                'quantity': quantity,
                'category': self._get_category_for_product(product_id)
            }
        
        self._refresh_cart_table()
        self.quantity_spinbox.setValue(1)
    
    def _get_category_for_product(self, product_id: int) -> str:
        """Obtiene la categoría de un producto"""
        for category, products in self.products_tree.items():
            for product in products:
                if product['id'] == product_id:
                    return category
        return "Desconocido"
    
    def _refresh_cart_table(self):
        """Actualiza la tabla del carrito"""
        self.cart_table.setRowCount(0)
        total = 0
        
        for idx, (product_id, product_info) in enumerate(self.selected_products.items()):
            self.cart_table.insertRow(idx)
            
            # Categoría
            cat_item = QTableWidgetItem(product_info['category'])
            self.cart_table.setItem(idx, 0, cat_item)
            
            # Producto
            prod_item = QTableWidgetItem(product_info['name'])
            self.cart_table.setItem(idx, 1, prod_item)
            
            # Modelo
            model_item = QTableWidgetItem(product_info['model'])
            self.cart_table.setItem(idx, 2, model_item)
            
            # Precio
            price_item = QTableWidgetItem(f"${product_info['price']:.2f}")
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.cart_table.setItem(idx, 3, price_item)
            
            # Cantidad
            qty_item = QTableWidgetItem(str(product_info['quantity']))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.cart_table.setItem(idx, 4, qty_item)
            
            # Botón eliminar
            delete_btn = QPushButton("🗑️")
            delete_btn.setMaximumWidth(40)
            delete_btn.clicked.connect(lambda checked, pid=product_id: self.remove_from_cart(pid))
            self.cart_table.setCellWidget(idx, 5, delete_btn)
            
            # Calcular total
            total += product_info['price'] * product_info['quantity']
        
        self.total_label.setText(f"${total:.2f}")
    
    def remove_from_cart(self, product_id: int):
        """Elimina un producto del carrito"""
        if product_id in self.selected_products:
            del self.selected_products[product_id]
            self._refresh_cart_table()
    
    def get_selected_products(self) -> Dict:
        """Retorna los productos seleccionados"""
        return self.selected_products
