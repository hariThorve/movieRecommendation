from sqlmodel import Field, Session, SQLModel, create_engine

class Person(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secretName: str
    age: int | None = None

rahulData = Person(name = "Rahul", secretName= "rahulya", age = 21)
hariData = Person(name = "Hariprasad", secretName= "hari", age = 21)
sohamData = Person(name = "Soham", secretName= "somya", age = 21)

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/hari")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(rahulData)
    session.add(hariData)
    session.add(sohamData)
    session.commit()