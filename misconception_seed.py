import json
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# 1. Database Connection Configuration
DB_USER = "pearlmolefe"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "misconception_db"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 2. Schema-Aware Object-Relational Mapping (ORM) Models
class MisconceptionTaxonomy(Base):
    __tablename__ = "misconception_taxonomy"
    __table_args__ = {"schema": "misconception"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    category = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    
    questions = relationship("DiagnosticQuestion", back_populates="misconception")

class DiagnosticQuestion(Base):
    __tablename__ = "diagnostic_questions"
    __table_args__ = {"schema": "misconception"}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    misconception_id = Column(Integer, ForeignKey("misconception.misconception_taxonomy.id", ondelete="SET NULL"), nullable=True)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(String(255), nullable=False)
    incorrect_answer_distractor = Column(String(255), nullable=False)
    
    misconception = relationship("MisconceptionTaxonomy", back_populates="questions")

# 3. Seeding Execution Pipeline
def seed_database():
    session = SessionLocal()
    
    try:
        # Step A: Validate that the custom schema exists
        print("📁 Verifying database schema bounds...")
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS misconception;"))
            conn.commit()
            
        # Build tables inside the schema if they do not exist
        Base.metadata.create_all(bind=engine)
        
        # Clean out old data to avoid duplicate key violations on rerun
        print("🧹 Cleaning database records inside custom taxonomy tables...")
        session.query(DiagnosticQuestion).delete()
        session.query(MisconceptionTaxonomy).delete()
        session.commit()
        
        # Reset SERIAL sequences to 1 inside the 'misconception' schema namespace
        print("🔄 Resetting sequence counters...")
        session.execute(text("ALTER SEQUENCE misconception.misconception_taxonomy_id_seq RESTART WITH 1;"))
        session.execute(text("ALTER SEQUENCE misconception.diagnostic_questions_id_seq RESTART WITH 1;"))
        session.commit()

        # Step B: Read and Ingest the Misconceptions Taxonomy file
        print("📂 Reading table_misconceptions.json...")
        with open("table_misconceptions.json", "r", encoding="utf-8") as f:
            misc_data = json.load(f)
            
        json_id_to_db_id = {}
        
        print("🌱 Seeding misconception_taxonomy table...")
        for item in misc_data:
            db_misc = MisconceptionTaxonomy(
                name=item["name"],
                category=item["category"],
                description=item["description"]
            )
            session.add(db_misc)
            session.flush() # Forces database write to fetch the SERIAL generated identity ID
            
            # Map original static JSON ID to our fresh database auto-increment ID
            json_id_to_db_id[item["id"]] = db_misc.id

        # Step C: Read and Ingest the 20 Diagnostic Questions sets
        print("📂 Reading table_questions.json...")
        with open("table_questions.json", "r", encoding="utf-8") as f:
            question_data = json.load(f)
            
        print("🌱 Seeding 20 diagnostic_questions rows...")
        for q in question_data:
            raw_fk = q.get("misconception_id")
            resolved_fk = json_id_to_db_id.get(raw_fk) if raw_fk else None
            
            db_question = DiagnosticQuestion(
                misconception_id=resolved_fk,
                question_text=q["question_text"],
                correct_answer=q["correct_answer"],
                incorrect_answer_distractor=q["incorrect_answer_distractor"]
            )
            session.add(db_question)

        # Commit everything to the database permanently
        session.commit()
        print("✅ Success! Your 20-set relational schema is fully seeded.")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Critical Error during database seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
