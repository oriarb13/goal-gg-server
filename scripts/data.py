# scripts/create_demo_data.py
import sys
import os
sys.path.append('.')

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.models.club import Club
from app.models.member import Member
from app.models.enums import SportCategoryEnum, ClubStatusEnum
from app.utils.security import hash_password

def create_demo_data():
    """Create comprehensive demo data"""
    db = SessionLocal()
    
    try:
        print("🚀 Starting demo data creation...")
        
        # 1. Create Super Admin - Ori Arbeli
        print("\n1️⃣ Creating Super Admin...")
        super_admin = User(
            first_name="Ori",
            last_name="Arbeli", 
            email="ori@gmail.com",
            password=hash_password("ori13690"),
            phone={"prefix": "+972", "number": "0523080860"},
            year_of_birth=2002,
            city="Rishon Letzion",
            country="Israel",
            sport_category=SportCategoryEnum.FOOTBALL,
            positions=["MIDFIELDER", "STRIKER"],
            cm=175,
            kg=70,
            avg_skill_rating=9.5,
            role_id=5  # super_admin
        )
        db.add(super_admin)
        db.flush()
        print(f"  ✅ Created Super Admin: {super_admin.first_name} {super_admin.last_name} (ID: {super_admin.id})")
        
        # 2. Create Gold User
        print("\n2️⃣ Creating Gold User...")
        gold_user = User(
            first_name="David",
            last_name="Cohen",
            email="david@gmail.com", 
            password=hash_password("password123"),
            phone={"prefix": "+972", "number": "0501234567"},
            year_of_birth=1990,
            city="Tel Aviv",
            country="Israel",
            sport_category=SportCategoryEnum.FOOTBALL,
            positions=["DEFENDER"],
            cm=180,
            kg=75,
            avg_skill_rating=8.2,
            role_id=3  # gold
        )
        db.add(gold_user)
        db.flush()
        print(f"  ✅ Created Gold User: {gold_user.first_name} {gold_user.last_name} (ID: {gold_user.id})")
        
        # 3. Create Silver User
        print("\n3️⃣ Creating Silver User...")
        silver_user = User(
            first_name="Sarah",
            last_name="Levi",
            email="sarah@gmail.com",
            password=hash_password("password123"),
            phone={"prefix": "+972", "number": "0507654321"},
            year_of_birth=1995,
            city="Haifa",
            country="Israel", 
            sport_category=SportCategoryEnum.FOOTBALL,
            positions=["GOALKEEPER"],
            cm=165,
            kg=60,
            avg_skill_rating=7.8,
            role_id=2  # silver
        )
        db.add(silver_user)
        db.flush()
        print(f"  ✅ Created Silver User: {silver_user.first_name} {silver_user.last_name} (ID: {silver_user.id})")
        
        # 4. Create 10 Regular Users
        print("\n4️⃣ Creating 10 Regular Users...")
        regular_users = []
        regular_users_data = [
            {"first_name": "Yoni", "last_name": "Goldberg", "email": "yoni@gmail.com"},
            {"first_name": "Maya", "last_name": "Ben-David", "email": "maya@gmail.com"},
            {"first_name": "Avi", "last_name": "Rosenberg", "email": "avi@gmail.com"},
            {"first_name": "Noa", "last_name": "Friedman", "email": "noa@gmail.com"},
            {"first_name": "Dan", "last_name": "Katz", "email": "dan@gmail.com"},
            {"first_name": "Tal", "last_name": "Shapiro", "email": "tal@gmail.com"},
            {"first_name": "Gal", "last_name": "Weiss", "email": "gal@gmail.com"},
            {"first_name": "Rom", "last_name": "Green", "email": "rom@gmail.com"},
            {"first_name": "Shir", "last_name": "Black", "email": "shir@gmail.com"},
            {"first_name": "Eyal", "last_name": "White", "email": "eyal@gmail.com"}
        ]
        
        for i, user_data in enumerate(regular_users_data):
            regular_user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"],
                password=hash_password("password123"),
                phone={"prefix": "+972", "number": f"050{1000000 + i}"},
                year_of_birth=1985 + i,
                city="Jerusalem",
                country="Israel",
                sport_category=SportCategoryEnum.FOOTBALL,
                positions=["MIDFIELDER"],
                cm=170 + i,
                kg=65 + i,
                avg_skill_rating=6.0 + (i * 0.2),
                role_id=1  # user
            )
            db.add(regular_user)
            regular_users.append(regular_user)
        
        db.flush()
        print(f"  ✅ Created {len(regular_users)} regular users")
        
        # 5. Create Clubs
        print("\n5️⃣ Creating Clubs...")
        
        # Gold user clubs (2 clubs)
        gold_club_1 = Club(
            name="Maccabi Tel Aviv",
            description="Professional football club in Tel Aviv",
            admin_id=gold_user.id,
            sport_category=SportCategoryEnum.FOOTBALL,
            is_private=False,
            max_players=30,  # Gold role max_players
            captains=[gold_user.id],
            location={
                "country": "Israel",
                "city": "Tel Aviv", 
                "address": "Bloomfield Stadium",
                "lat": 32.0853,
                "lng": 34.7818
            }
        )
        db.add(gold_club_1)
        
        gold_club_2 = Club(
            name="Hapoel Tel Aviv",
            description="Historic football club in Tel Aviv",
            admin_id=gold_user.id,
            sport_category=SportCategoryEnum.FOOTBALL,
            is_private=False,
            max_players=30,
            captains=[gold_user.id],
            location={
                "country": "Israel",
                "city": "Tel Aviv",
                "address": "Jaffa Stadium", 
                "lat": 32.0544,
                "lng": 34.7595
            }
        )
        db.add(gold_club_2)
        
        # Silver user club (1 club)
        silver_club = Club(
            name="Maccabi Haifa",
            description="Northern football club",
            admin_id=silver_user.id,
            sport_category=SportCategoryEnum.FOOTBALL,
            is_private=False,
            max_players=25,  # Silver role max_players
            captains=[silver_user.id],
            location={
                "country": "Israel",
                "city": "Haifa",
                "address": "Sammy Ofer Stadium",
                "lat": 32.7940,
                "lng": 34.9896
            }
        )
        db.add(silver_club)
        
        # Super admin club
        super_admin_club = Club(
            name="Goal GG Academy",
            description="Elite football training academy",
            admin_id=super_admin.id,
            sport_category=SportCategoryEnum.FOOTBALL,
            is_private=False,
            max_players=1000,  # Super admin max_players
            captains=[super_admin.id],
            location={
                "country": "Israel",
                "city": "Rishon Letzion",
                "address": "Goal GG Training Center",
                "lat": 31.9730,
                "lng": 34.7925
            }
        )
        db.add(super_admin_club)
        
        db.flush()
        print(f"  ✅ Created 4 clubs")
        
        # 6. Create Memberships
        print("\n6️⃣ Creating Memberships...")
        
        # Admin members for their own clubs (all stats start at 0)
        admin_members = [
            Member(user_id=gold_user.id, club_id=gold_club_1.id, total_goals=0, total_assists=0, total_games=0, skill_rating=gold_user.avg_skill_rating, positions=gold_user.positions),
            Member(user_id=gold_user.id, club_id=gold_club_2.id, total_goals=0, total_assists=0, total_games=0, skill_rating=gold_user.avg_skill_rating, positions=gold_user.positions),
            Member(user_id=silver_user.id, club_id=silver_club.id, total_goals=0, total_assists=0, total_games=0, skill_rating=silver_user.avg_skill_rating, positions=silver_user.positions),
            Member(user_id=super_admin.id, club_id=super_admin_club.id, total_goals=0, total_assists=0, total_games=0, skill_rating=super_admin.avg_skill_rating, positions=super_admin.positions)
        ]
        
        for member in admin_members:
            db.add(member)
        
        # Regular users memberships (all stats start at 0)
        # 2 users to silver club
        for i in range(2):
            member = Member(
                user_id=regular_users[i].id,
                club_id=silver_club.id,
                total_goals=0,
                total_assists=0,
                total_games=0,
                skill_rating=regular_users[i].avg_skill_rating,
                positions=regular_users[i].positions
            )
            db.add(member)
        
        # 3 users to gold club 1
        for i in range(2, 5):
            member = Member(
                user_id=regular_users[i].id,
                club_id=gold_club_1.id,
                total_goals=0,
                total_assists=0,
                total_games=0,
                skill_rating=regular_users[i].avg_skill_rating,
                positions=regular_users[i].positions
            )
            db.add(member)
        
        # 5 users to gold club 2
        for i in range(5, 10):
            member = Member(
                user_id=regular_users[i].id,
                club_id=gold_club_2.id,
                total_goals=0,
                total_assists=0,
                total_games=0,
                skill_rating=regular_users[i].avg_skill_rating,
                positions=regular_users[i].positions
            )
            db.add(member)
        
        # All users to super admin club
        all_users = [super_admin, gold_user, silver_user] + regular_users
        for user in all_users[1:]:  # Skip super admin (already added)
            member = Member(
                user_id=user.id,
                club_id=super_admin_club.id,
                total_goals=0,
                total_assists=0,
                total_games=0,
                skill_rating=user.avg_skill_rating,
                positions=user.positions
            )
            db.add(member)
        
        # Commit all data
        db.commit()
        
        print("\n🎉 Demo data creation completed successfully!")
        print("\n📊 Summary:")
        print(f"  👥 Users created: {len(all_users)}")
        print(f"     - 1 Super Admin (Ori Arbeli)")
        print(f"     - 1 Gold User (David Cohen)")
        print(f"     - 1 Silver User (Sarah Levi)")
        print(f"     - 10 Regular Users")
        print(f"  🏆 Clubs created: 4")
        print(f"     - 2 clubs owned by Gold user")
        print(f"     - 1 club owned by Silver user")
        print(f"     - 1 club owned by Super Admin")
        print(f"  👥 Club memberships:")
        print(f"     - Silver club: 3 members (admin + 2 users)")
        print(f"     - Gold club 1: 4 members (admin + 3 users)")
        print(f"     - Gold club 2: 6 members (admin + 5 users)")
        print(f"     - Super Admin club: 13 members (all users)")
        
        print(f"\n🔑 Login details:")
        print(f"  Super Admin: ori@gmail.com / ori13690")
        print(f"  Gold User: david@gmail.com / password123")
        print(f"  Silver User: sarah@gmail.com / password123")
        print(f"  Regular Users: [name]@gmail.com / password123")
        
    except Exception as e:
        print(f"❌ Error creating demo data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_data()