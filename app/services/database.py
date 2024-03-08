from app.services.logger import Logger
from app.db_connection import DbConnection
from app.utilities.utility import GlobalUtility
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker,query
from db_layer.models import Client,Configurations,BillingInformation,FileTypesInfo,Users,Subscriptions,SubscriptionPlan
from sqlalchemy.engine import URL

class DataBaseClass:

    _instance = None


    def __init__(self):
        self.global_utility = GlobalUtility.get_instance()
        self.logger = Logger().get_instance()
        self.db_connection = DbConnection.get_instance()


    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    def insert_data(self,model,model_name, data):         
         model.insert(model_name,data)

    def get_all_configurations(self,server,database):
        try:
            # dns = f'mssql+pyodbc://{server}/{database}?driver=SQL+Server'
            dns = f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
            engine = create_engine(dns)
            Session = sessionmaker(bind=engine)
            session = Session()

            clients_data = session.query(Client).filter_by(ClientId=1).all()
            clients_column_names = clients_data[0].__dict__.keys() if clients_data else []
            clients_array = [{column: getattr(row, column) for column in clients_column_names} for row in clients_data]
            for i, result_array in enumerate(clients_array):
                print(f"Result set {i + 1}:")
                print(result_array)

            confguration_data = session.query(Configurations).filter_by(ClientId=1).all()
            confguration_column_names = confguration_data[0].__dict__.keys() if confguration_data else []
            confguration_array = [{column: getattr(row, column) for column in confguration_column_names} for row in confguration_data]

            filetype_info_data = session.query(FileTypesInfo).filter_by(ClientId=1).all()
            filetype_info_column_names = filetype_info_data[0].__dict__.keys() if filetype_info_data else []
            filetype_info_array = [{column: getattr(row, column) for column in filetype_info_column_names} for row in
                                  filetype_info_data]

            # users_data = session.query(Users).filter_by(ClientId=1).all()
            subscriptions_data = session.query(Subscriptions).filter_by(ClientId=1).all()
            subscriptions_column_names = subscriptions_data[0].__dict__.keys() if subscriptions_data else []
            subscriptions_array = [{column: getattr(row, column) for column in subscriptions_column_names} for row in
                                   subscriptions_data]


            subscription_plan_data = session.query(SubscriptionPlan).filter_by(ClientId=1).all()
            subscription_plan_column_names = subscription_plan_data[0].__dict__.keys() if subscription_plan_data else []
            # subscription_plan_array = [{column: getattr(row, column) for column in subscription_plan_column_names} for row in
            #                        subscription_plan_column_names]
            # self.global_utility.set_client_data(clients_array)
            # self.global_utility.set_configurations_data(confguration_array)
            # self.global_utility.set_file_type_info_data(filetype_info_array)
            # self.global_utility.get_subscription_data(subscriptions_array)
            session.close()
            configurations = {
                'Client':  clients_array,
                'Configurations': confguration_array,
                'FileTypesInfo': filetype_info_array,
                'Subscriptions': subscriptions_array,
                # 'SubscriptionPlan': subscription_plan_array
            }
            return configurations
        except Exception as e:
            session.close()
            self.logger.error("connect_to_database", e)
            raise
        finally:
            session.close()