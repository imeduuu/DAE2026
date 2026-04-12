"""
Repositorio de Usuarios
Capa de acceso a datos para la entidad User
"""
from database.connection import DatabaseConnection
from database.models import User
from typing import Optional, List


class UserRepository:
    """Repositorio para gestionar operaciones con usuarios"""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Inicializa el repositorio
        
        Args:
            db_connection: Instancia de DatabaseConnection
        """
        self.db = db_connection
    
    def create(self, user: User) -> User:
        """
        Crea un nuevo usuario en la base de datos
        
        Args:
            user: Objeto User a crear
            
        Returns:
            User: Usuario creado con ID asignado
            
        Raises:
            ValueError: Si el usuario ya existe (username o email duplicados)
        """
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, role)
                    VALUES (?, ?, ?, ?)
                """, (user.username, user.email, user.password_hash, user.role))
                
                user.id = cursor.lastrowid
                return user
        except Exception as e:
            raise ValueError(f"Error al crear usuario: {str(e)}")
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por ID
        
        Args:
            user_id: ID del usuario
            
        Returns:
            User o None si no existe
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
            return None
    
    def find_by_username(self, username: str) -> Optional[User]:
        """
        Busca un usuario por nombre de usuario
        
        Args:
            username: Nombre de usuario
            
        Returns:
            User o None si no existe
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
            return None
    
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por correo electrónico
        
        Args:
            email: Email del usuario
            
        Returns:
            User o None si no existe
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return self._row_to_user(row)
            return None
    
    def find_all(self) -> List[User]:
        """
        Obtiene todos los usuarios
        
        Returns:
            Lista de usuarios
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            return [self._row_to_user(row) for row in rows]
    
    def update(self, user: User) -> bool:
        """
        Actualiza un usuario existente
        
        Args:
            user: Usuario con datos actualizados
            
        Returns:
            True si se actualizó, False si no existe
        """
        if not user.id:
            raise ValueError("El usuario debe tener un ID para actualizarse")
        
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("""
                    UPDATE users 
                    SET username = ?, email = ?, password_hash = ?, role = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (user.username, user.email, user.password_hash, user.role, user.id))
                
                return cursor.rowcount > 0
        except Exception as e:
            raise ValueError(f"Error al actualizar usuario: {str(e)}")
    
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó, False si no existe
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cursor.rowcount > 0
    
    def _row_to_user(self, row) -> User:
        """Convierte una fila de la BD a objeto User"""
        return User(
            id=row["id"],
            username=row["username"],
            email=row["email"],
            password_hash=row["password_hash"],
            role=row["role"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
