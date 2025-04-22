# import psycopg2.extras
#
# from envirement.utils import Env
# from dotenv import load_dotenv
#
#
# load_dotenv()
#
# class DB:
#     DB_NAME = Env().db.DB_NAME
#     DB_USER = Env().db.DB_USER
#     DB_PASSWORD = Env().db.DB_PASSWORD
#     DB_PORT = Env().db.DB_PORT
#     DB_HOST = Env().db.DB_HOST
#     connect = psycopg2.connect(dbname=DB_NAME ,
#                                user=DB_USER ,
#                                port=DB_PORT ,
#                                host=DB_HOST ,
#                                password=DB_PASSWORD)
#     cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)
#
#
# class Manager(DB):
#     def save(self) -> object:
#         table_name = self.__class__.__name__.lower() + "s"
#         cols = [col for col, val in self.__dict__.items() if not val == None]
#         values = [val for col, val in self.__dict__.items() if not val == None]
#         col_format = " , ".join(cols)
#         value_format = " , ".join(["%s"]*len(cols))
#         query = f"""
#             insert into {table_name} ({col_format}) values ({value_format}) returning *
#         """
#         self.cursor.execute(query , values)
#         self.connect.commit()
#         data: list = self.cursor.fetchall()
#         dict_data = self.get_dict_resultset(data)[0]
#         return self.__class__(**dict_data)
#
#     def __get_dict_resultset(self , data):
#         dict_result = []
#         for row in data:
#             dict_result.append(dict(row))
#         return dict_result
#
#     def delete(self) -> list[object]:
#         table_name = self.__class__.__name__.lower() + "s"
#         cols = [col for col, val in self.__dict__.items() if not val == None]
#         values = [val for col, val in self.__dict__.items() if not val == None]
#         condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
#         query = f"""
#             delete from {table_name} {condition_format} returning *
#         """
#         self.cursor.execute(query , values)
#         self.connect.commit()
#         data = self.cursor.fetchall()
#         datas: list = self.__get_dict_resultset(data)
#         return_list = []
#         if datas:
#             for i in datas:
#                 return_list.append(self.__class__(**i))
#             return return_list
#         else:
#             return []
#
#     def update(self, **kwargs) -> object:
#         table_name = self.__class__.__name__.lower() + "s"
#         cols = [col for col, val in self.__dict__.items() if not val == None]
#         values = [val for col, val in self.__dict__.items() if not val == None]
#         set_cols = kwargs.keys()
#         set_values = kwargs.values()
#         condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
#         set_format = " = %s , ".join(set_cols) + " = %s "
#         query = f"""
#             update {table_name} set {set_format} {condition_format} returning *
#         """
#         self.cursor.execute(query , list(set_values) + values)
#         self.connect.commit()
#         data = self.cursor.fetchall()
#         datas: list = self.__get_dict_resultset(data)
#         return_list = []
#         if datas:
#             for i in datas:
#                 return_list.append(self.__class__(**i))
#             return return_list
#         else:
#             return []
#
#     def first(self , *args) -> object:
#         cols_format = "*" if not args else " , ".join(args)
#         table_name = self.__class__.__name__.lower() + "s"
#         cols = [col for col, val in self.__dict__.items() if not val == None]
#         values = [val for col, val in self.__dict__.items() if not val == None]
#         condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
#         query = f"""
#             select {cols_format} from {table_name} {condition_format}
#         """
#         self.cursor.execute(query , values)
#         data = self.cursor.fetchall()
#         dict_data = self.__get_dict_resultset(data)
#         if dict_data:
#             dict_data = dict_data[0]
#             return self.__class__(**dict_data)
#
#     def objects(self , *args) -> list[object]:
#         cols_format = "*" if not args else " , ".join(args)
#         table_name = self.__class__.__name__.lower() + "s"
#         cols = [col for col, val in self.__dict__.items() if not val == None]
#         values = [val for col, val in self.__dict__.items() if not val == None]
#         condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
#         query = f"""
#                     select {cols_format} from {table_name} {condition_format}
#                 """
#         self.cursor.execute(query, values)
#         data = self.cursor.fetchall()
#         datas : list = self.__get_dict_resultset(data)
#         return_list = []
#         if datas:
#             for i in datas:
#                 return_list.append(self.__class__(**i))
#             return return_list
#
#     def get_all(self , *args) -> list[dict]:
#         cols_format = "*" if not args else " , ".join(args)
#         table_name = self.__class__.__name__.lower() + "s"
#         cols = [col for col, val in self.__dict__.items() if not val == None]
#         values = [val for col, val in self.__dict__.items() if not val == None]
#         condition_format = "" if not cols else "where " + " = %s and ".join(cols) + " = %s"
#         query = f"""
#                             select {cols_format} from {table_name} {condition_format}
#                         """
#         self.cursor.execute(query, values)
#         data = self.cursor.fetchall()
#         datas: list = self.__get_dict_resultset(data)
#         return datas
from select import select

from sqlalchemy import create_engine, ForeignKey, DECIMAL, insert, select, delete, update, text
from sqlalchemy import BIGINT
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker
from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLAEnum

engine = create_engine("postgresql+psycopg2://postgres:1@localhost:5432/tg_bot_p30")
session = sessionmaker(engine)()
Base = declarative_base()


class Developer(Base):
    __tablename__ = "developers"
    chat_id : Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name : Mapped[str]
    last_name : Mapped[str]
    phone_number : Mapped[str]
    username : Mapped[str]
    occupation : Mapped[str]
    description : Mapped[str]

class Customer(Base):
    __tablename__ = "customers"
    chat_id : Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    username: Mapped[str]

class Project(Base):
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



Base.metadata.create_all(bind=engine)

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

