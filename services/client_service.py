"""Service for managing clients."""

from typing import List, Optional
from models import db, Client

class ClientService:
    @staticmethod
    def create_client(name: str, email: Optional[str] = None, 
                     notes: Optional[str] = None) -> Client:
        """Create a new client.
        
        Args:
            name: Name of the client.
            email: Optional client email.
            notes: Optional notes about the client.
            
        Returns:
            The created client.
            
        Raises:
            ValueError: If client with name already exists.
        """
        if Client.query.filter_by(name=name).first():
            raise ValueError(f"Client '{name}' already exists")
            
        client = Client(name=name, email=email, notes=notes)
        db.session.add(client)
        db.session.commit()
        return client
    
    @staticmethod
    def get_client(client_id: int) -> Client:
        """Get a client by ID."""
        return Client.query.get_or_404(client_id)
    
    @staticmethod
    def list_clients() -> List[Client]:
        """List all clients ordered by name."""
        return Client.query.order_by(Client.name).all()
    
    @staticmethod
    def update_client(client_id: int, name: Optional[str] = None,
                     email: Optional[str] = None, 
                     notes: Optional[str] = None) -> Client:
        """Update a client's details."""
        client = Client.query.get_or_404(client_id)
        
        if name and name != client.name:
            if Client.query.filter_by(name=name).first():
                raise ValueError(f"Client '{name}' already exists")
            client.name = name
            
        if email is not None:
            client.email = email
            
        if notes is not None:
            client.notes = notes
            
        db.session.commit()
        return client
    
    @staticmethod
    def delete_client(client_id: int) -> None:
        """Delete a client.
        
        Note: This will set client_id to NULL for all associated time entries.
        """
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
