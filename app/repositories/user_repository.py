from app.models.user import User
from app.database import get_connection


class UserRepository:
    @staticmethod
    def find_all() -> list[User]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC")
                return [User.from_row(row) for row in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def find_by_id(user_id: int) -> User | None:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
                row = cur.fetchone()
                return User.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def search(query: str) -> list[User]:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                is_numeric = query.isdigit()
                if is_numeric:
                    cur.execute(
                        "SELECT id, name, email, created_at FROM users "
                        "WHERE id = %s OR LOWER(name) LIKE %s OR LOWER(email) LIKE %s "
                        "ORDER BY created_at DESC",
                        (int(query), f"%{query.lower()}%", f"%{query.lower()}%"),
                    )
                else:
                    cur.execute(
                        "SELECT id, name, email, created_at FROM users "
                        "WHERE LOWER(name) LIKE %s OR LOWER(email) LIKE %s "
                        "ORDER BY created_at DESC",
                        (f"%{query.lower()}%", f"%{query.lower()}%"),
                    )
                return [User.from_row(row) for row in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def find_by_email(email: str) -> User | None:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email, created_at FROM users WHERE email = %s", (email,))
                row = cur.fetchone()
                return User.from_row(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def create(name: str, email: str) -> User:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email, created_at",
                    (name, email),
                )
                conn.commit()
                return User.from_row(cur.fetchone())
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def update(user_id: int, name: str, email: str) -> User | None:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE users SET name = %s, email = %s WHERE id = %s RETURNING id, name, email, created_at",
                    (name, email, user_id),
                )
                conn.commit()
                row = cur.fetchone()
                return User.from_row(row) if row else None
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def delete(user_id: int) -> bool:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()
