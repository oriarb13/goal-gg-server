# scripts/create_initial_data.py
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.role import Role

def create_roles():
    """Create initial roles in the database"""
    db = SessionLocal()
    
    try:
        # Check if roles already exist
        existing_roles = db.query(Role).count()
        if existing_roles > 0:
            print(f"✅ Roles already exist! Found {existing_roles} roles.")
            
            # Show existing roles
            roles = db.query(Role).all()
            print("\nExisting roles:")
            for role in roles:
                print(f"  - {role.name}: {role.max_clubs} clubs, {role.max_players} players, ${role.cost}")
            return
        
        # Define roles data
        roles_data = [
            {"name": "user", "max_clubs": 0, "max_players": 0, "cost": 0.0},
            {"name": "silver", "max_clubs": 1, "max_players": 25, "cost": 15.0},
            {"name": "gold", "max_clubs": 3, "max_players": 30, "cost": 25.0},
            {"name": "premium", "max_clubs": 5, "max_players": 100, "cost": 40.0},
            {"name": "super_admin", "max_clubs": 1000, "max_players": 1000, "cost": 0.0}
        ]
        
        print("Creating roles...")
        
        # Create role objects
        roles = []
        for role_data in roles_data:
            role = Role(
                name=role_data["name"],
                max_clubs=role_data["max_clubs"], 
                max_players=role_data["max_players"],
                cost=role_data["cost"]
            )
            roles.append(role)
            db.add(role)
            print(f"  ✅ Created role: {role.name}")
        
        # Commit to database
        db.commit()
        
        print(f"\n🎉 Successfully created {len(roles)} roles!")
        print("\nRoles created:")
        for role in roles:
            print(f"  ID: {role.id} | {role.name}: {role.max_clubs} clubs, {role.max_players} players, ${role.cost}")
            
    except Exception as e:
        print(f"❌ Error creating roles: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def show_roles():
    """Display all existing roles"""
    db = SessionLocal()
    try:
        roles = db.query(Role).all()
        
        if not roles:
            print("❌ No roles found in database")
            return
            
        print(f"\n📋 Found {len(roles)} roles:")
        print("=" * 60)
        for role in roles:
            print(f"ID: {role.id:2d} | {role.name:12s} | Clubs: {role.max_clubs:3d} | Players: {role.max_players:3d} | Cost: ${role.cost:5.2f}")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error fetching roles: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting roles creation...")
    create_roles()
    print("\n📊 Current roles in database:")
    show_roles()

# Alternative: Run individual functions
# create_roles()  # Create the roles
# show_roles()    # Just show existing roles