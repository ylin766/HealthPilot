from semantic_kernel.functions.kernel_function_decorator import kernel_function
import chainlit as cl
import sqlite3, os

class UserProfileQueryPlugin:
    def __init__(self):
        self.db_path = "data/memory.db"

    @kernel_function(
        name="get_user_profile_if_exists",
        description="Check if user_profile table exists. If it does, return the current user's profile if found."
    )
    async def get_user_profile_if_exists(self) -> str:
        user_id = cl.user_session.get("user").identifier

        # Check if the database file exists
        if not os.path.exists(self.db_path):
            return "❌ Database file not found."

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Check if the table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='user_profile';
        """)
        table_exists = cursor.fetchone()

        if not table_exists:
            conn.close()
            return "❌ Table 'user_profile' does not exist."

        # Try to fetch the user's profile
        cursor.execute("""
            SELECT name, age, gender, height_cm, weight_kg
            FROM user_profile
            WHERE user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return (
                f"✅ Profile found:\n"
                f"- Name: {row[0]}\n"
                f"- Age: {row[1]}\n"
                f"- Gender: {row[2]}\n"
                f"- Height: {row[3]} cm\n"
                f"- Weight: {row[4]} kg"
            )
        else:
            return "ℹ️ Table exists, but no profile found for this user."
