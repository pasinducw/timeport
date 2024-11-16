"""Service for managing projects."""

from typing import List, Optional
from models import db, Project

class ProjectService:
    @staticmethod
    def create_project(name: str, description: Optional[str] = None) -> Project:
        """Create a new project.
        
        Args:
            name: Name of the project.
            description: Optional project description.
            
        Returns:
            The created project.
            
        Raises:
            ValueError: If project with name already exists.
        """
        if Project.query.filter_by(name=name).first():
            raise ValueError(f"Project '{name}' already exists")
            
        project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()
        return project
    
    @staticmethod
    def get_project(project_id: int) -> Project:
        """Get a project by ID."""
        return Project.query.get_or_404(project_id)
    
    @staticmethod
    def list_projects() -> List[Project]:
        """List all projects ordered by name."""
        return Project.query.order_by(Project.name).all()
    
    @staticmethod
    def update_project(project_id: int, name: Optional[str] = None, 
                      description: Optional[str] = None) -> Project:
        """Update a project's details."""
        project = Project.query.get_or_404(project_id)
        
        if name and name != project.name:
            if Project.query.filter_by(name=name).first():
                raise ValueError(f"Project '{name}' already exists")
            project.name = name
            
        if description is not None:
            project.description = description
            
        db.session.commit()
        return project
    
    @staticmethod
    def delete_project(project_id: int) -> None:
        """Delete a project.
        
        Note: This will set project_id to NULL for all associated time entries.
        """
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
