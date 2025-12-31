from datetime import datetime
import hashlib
from ldap3 import Server, Connection, ALL, SUBTREE
import streamlit as st


class ValidationError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class User:
    """Represents a user session in SD Automation Hub."""

    def __init__(self, username: str, password: str, display_name: str, hr_code: str,
                 job_title: str, account_type: int = 1, roles=None, last_logon: str = "") -> None:
        # Validate username and display_name
        if not username or not isinstance(username, str):
            raise ValueError("Username must be a non-empty string.")
        if not display_name or not isinstance(display_name, str):
            raise ValueError("Display name must be a non-empty string.")

        # Validate roles
        if not isinstance(roles, list):
            raise TypeError("Roles must be a list.")

        # Validate account_type
        if not isinstance(account_type, int):
            raise TypeError("Account type must be an integer.")

        self.username = username
        self.display_name = display_name
        self.roles = roles
        self.hr_code = hr_code
        self.job_title = job_title
        self.account_type = account_type
        self.last_logon = last_logon
        self.password_hash = self._hash_password(password=password)

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def update_last_logon(self) -> None:
        """Update last logon timestamp in human-readable format."""
        self.last_logon = datetime.now().strftime("%d-%m-%Y %H:%M")

    def get_summary(self) -> str:
        """Return a summary of user information."""
        return (f"User: {self.display_name} ({self.username})\n"
                f"HR Code: {self.hr_code}\n"
                f"Job Title: {self.job_title}\n"
                f"Roles: {', '.join(self.roles)}\n"
                f"Last Logon: {self.last_logon or 'Never'}")

    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return "admin" in [role.lower() for role in self.roles]

    def is_user(self) -> bool:
        """Check if user is a regular user."""
        return "user" in [role.lower() for role in self.roles]


def authenticate_ldap(username: str, password: str) -> dict:
    try:
        server = Server("ldap://vn-ldaps.hcg.homecredit.net", get_info=ALL)
        conn = Connection(
            server,
            f"CN={username},OU=Users,OU=VN,DC=hcg,DC=homecredit,DC=net",
            password,
            auto_bind=True
        )

        if not conn.bound:
            raise AuthenticationError("LDAP bind failed.")

        conn.search(
            search_base="OU=Users,OU=VN,DC=hcg,DC=homecredit,DC=net",
            search_filter=f"(&(samAccountName={username})(memberOf=CN=VN.SD.SD_AUTOMATION_HUB.USER,OU=Groups,OU=VN,DC=hcg,DC=homecredit,DC=net))",
            search_scope=SUBTREE,
            attributes=["displayName", "employeeID", "title"]
        )

        if not conn.entries:
            raise AuthenticationError(
                "User not found or not in required group.")

        entry = conn.entries[0]
        conn.unbind()

        return {
            "displayName": str(entry.displayName),
            "employeeID": str(entry.employeeID),
            "title": str(entry.title),
            "roles": ["user"]  # Static for now
        }

    except Exception as e:
        raise AuthenticationError(f"LDAP authentication failed: {e}")


def login(username: str, password: str) -> User:
    if not username:
        raise ValidationError("Username cannot be empty.")
    if not password:
        raise ValidationError("Password cannot be empty.")

    ldap_data = authenticate_ldap(username, password)

    user = User(
        username=username,
        display_name=ldap_data["displayName"],
        roles=ldap_data["roles"],
        hr_code=ldap_data["employeeID"],
        job_title=ldap_data["title"],
        password=password
    )
    user.update_last_logon()

    st.session_state["user"] = user
    return user
