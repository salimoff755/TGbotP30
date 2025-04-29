# from select import select
from sqlalchemy import ForeignKey, DECIMAL, insert, select, delete, update, text, TIMESTAMP, func
from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLAEnum

from db import Base
from db.utils import CreatedModel

# engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/tg_bot_p30")
# session = sessionmaker(engine)()
# Base = declarative_base()

class User(CreatedModel):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_name : Mapped[str]
    last_name : Mapped[str] = mapped_column(nullable=True)
    username : Mapped[str] = mapped_column(nullable=True)



class Developer(CreatedModel):
    __tablename__ = "developers"
    chat_id : Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_name : Mapped[str]
    last_name : Mapped[str]
    phone_number : Mapped[str]
    username : Mapped[str]
    occupation : Mapped[str]
    description : Mapped[str]



class Customer(CreatedModel):
    __tablename__ = "customers"
    chat_id : Mapped[int] = mapped_column(BIGINT, primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    username: Mapped[str]



class Project(CreatedModel):
    class StatusType(PyEnum):
        REJECT = "reject"
        ACCEPT = "accept"
    __tablename__ = "projects"
    id : Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name : Mapped[str]
    description : Mapped[str]
    developer_id : Mapped[int] = mapped_column(BIGINT , ForeignKey('developers.chat_id' , ondelete="CASCADE"))
    price : Mapped[float] = mapped_column(DECIMAL(10 , 0))
    customer_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('customers.chat_id', ondelete="CASCADE"))
    deadline : Mapped[str]
    tz_file : Mapped[str]
    status: Mapped[str] = mapped_column(SQLAEnum(StatusType, values_callable=lambda x: [i.value for i in x]),server_default=StatusType.ACCEPT.value)



metadata = Base.metadata
# Base.metadata.create_all(bind=engine)


# query_insert = insert(Customer).values(first_name="Elyor",
#                                        last_name="Salimov",
#                                        phone_number="940404060",
#                                        username="elyor755")
# session.execute(query_insert)
# session.commit()

# query_select = select(Customer).filter(Customer.username.contains("doni"))
# customers = session.execute(query_select).scalars()
# for customer in customers:
#     print(customer.username)


# query_delete = delete(Customer).filter(Customer.chat_id == 6)
# session.execute(query_delete)
# session.commit()

# query_update = update(Customer).filter(Customer.chat_id == 2).values(phone_number=971573350)
# session.execute(query_update)
# session.commit()

# query = text("select * from customers")
# print(list(session.execute(query).fetchall()))