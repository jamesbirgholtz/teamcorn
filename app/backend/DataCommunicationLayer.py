import pyodbc
import sqlalchemy
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Ticket:
    def __init__(self, ticket_id, status, assigned_to, priority):
        self.ticket_id = ticket_id
        self.status = status
        self.assigned_to = assigned_to
        self.priority = priority


class User:
    def __init__(self, user_id, username, email, role):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.role = role


class Comments:
    def __init__(self, comment_id):
        self.comment_id = comment_id


class DataCommunicationLayer:

    def __init__(self, logger):
        self._logger = logger
        self._db_engine = None
        self._db_session = None
        self._session = None

        try:
            self._db_engine = sqlalchemy.create_engine(
                'sqlite:////C://Users//Tobec//TicketsDB')  # ensure this is the correct path for the sqlite file.
            self._db_session = sessionmaker(bind=self._db_engine)
            self._session = self._db_session()
            self._db_conn = self._db_engine.connect()

            self._logger.info('Successfully connected to the Database!')
        except Exception as e:
            self._logger.info('Connecting to the Database Failed!')
            self._logger.error(e)
            Exception('Connecting to the Database Failed!')

    def register_user(self, user_id, email, username, role):
        try:
            metadata = MetaData()
            table = Table("Users", metadata, autoload_with=engine)
            insert_statement = insert(table).values(user_id, username, role)
            self._session.execute(insert_statement)
            self._session.commit()
            self._logger.info('Successfully inserted %s into the Database.' % email)
        except Exception as e:
            self._logger.error(e)
            self._session.rollback()
        finally:
            self._session.close()

    def check_user(self, user_id):
        metadata = MetaData()
        table - Table("Users", metadata, autoload_with=engine)
        select_statement = select(table).where(table.user_id == user_id)
        result = self._session.execute(select_statement)
        if result.first() is None:
            return [False, result]
        return [True, result]

    def create_ticket(self, status, assigned_to, priority):
        try:
            metadata = MetaData()
            table = Table("Tickets", metadata, autoload_with=engine)
            if self.check_user(assigned_to)[0]:
                insert_statement = insert(table).values(status, assigned_to, priority)
                self._session.execute(insert_statement)
                self._session.commit()
                self._logger.info('Successfully inserted into the Database.')
            else:
                print("Tried to Assign Ticket To Invalid User")
        except Exception as e:
            self._logger.error(e)
            self._session.rollback()
        finally:
            self._session.close()

    def check_ticket(self, ticket_id):
        metadata = MetaData()
        table = Table("Tickets", metadata, autoload_with=engine)
        select_statement = select(table).where(table.ticket_id == ticket_id)
        result = self._session.execute(select_statement)
        if result.first() is None:
            return [False, result]
        return [True, result]

    def select_ticket(self, ticket_id):
        result = self.check_ticket(ticket_id)
        if result[0]:
            return result[1]
        else:
            return result[1]

    def update_ticket_status(self, ticket_id, new_status):
        metadata = MetaData()
        table = Table("Tickets", metadata, autoload_with=engine)
        try:
            if self.check_ticket(ticket_id)[0]:
                update_statement = table.update().values(status=new_status).where(table.ticket_id == ticket_id)
                self._session.execute(update_statement)
                self._session.commit()
            else:
                print('No ticket exists!')
        except Exception as e:
            self._logger.error(e)
            self._session.rollback()

    def delete_ticket(self, ticket_id):
        metadata = MetaData()
        table = Table("Tickets", metadata, autoload_with=engine)
        try:
            if self.check_ticket(ticket_id)[0]:
                self._session.query(table).filter(table.ticket_id == ticket_id).delete()
                self._session.commit()
            else:
                print('No tickets found')
        except Exception as e:
            self._logger.error(e)
            self._session.rollback()
