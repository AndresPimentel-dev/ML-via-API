
from src.domain.entities import User
from src.domain.interfaces import ILogger, UserRepositoryInterface, SecurityService,TokenService, CacheServiceUsername, PredictionRepositoryInterface, CeleryWorkersService

class UserUseCases:
    def __init__(self, user_repo: UserRepositoryInterface, 
                 pws_sv: SecurityService, tk_sv: TokenService, 
                 cc_us: CacheServiceUsername,
                 logger: ILogger):
        self.user_repo = user_repo
        self.pwd_sv = pws_sv
        self.tk_sv = tk_sv
        self.cc_us = cc_us
        self.logger = logger

    def register_user(self, username:str, email:str, plain_password:str):
        try:
            self.logger.info(message="registro usuario", username=username,
                             email=email)
            existing_username = self.user_repo.get_by_username(username=username)
            existing_email = self.user_repo.get_by_email(email=email)
            if existing_username or existing_email:
                return None
            hashed_password = self.pwd_sv.hash_password(plain_password=plain_password)
            new = self.user_repo.create(username=username, email=email,hashed_password=hashed_password)
            token = self.tk_sv.create_token({"sub": username})
            self.cc_us.set_token_username(token=token, username=username, user_id=new.id)
            return token
        except Exception as e:
            self.logger.error(message="error creando usuario", error=str(e),
                              username=username, email=email)
            raise e
    def login_user(self, username:str, plain_password:str):
        try:
            self.logger.info(message="iniciando secion", username=username)
            user = self.user_repo.get_by_username(username=username)
            print(user)
            if not user:
                print("usuario no encontrado")
                return None
            verify = self.pwd_sv.verify_password(plain_password=plain_password, hashed_password=user.hashed_password)
            if not verify:
                return None
            token = self.tk_sv.create_token({"sub":username})
            self.cc_us.set_token_username(token=token, username=username, user_id=user.id)
            return token
        except Exception as e:
            self.logger.error(message="error iniciando sesion", username=username, error=str(e))