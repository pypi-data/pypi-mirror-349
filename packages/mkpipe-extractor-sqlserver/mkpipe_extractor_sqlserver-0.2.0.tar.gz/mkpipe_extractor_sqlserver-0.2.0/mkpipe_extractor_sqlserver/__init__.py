from mkpipe.functions_spark import BaseExtractor


class SqlserverExtractor(BaseExtractor):
    def __init__(self, config, settings):
        super().__init__(
            config,
            settings,
            driver_name='sqlserver',
            driver_jdbc='com.microsoft.sqlserver.jdbc.SQLServerDriver',
        )

    def build_jdbc_url(self):
        return f'jdbc:{self.driver_name}://{self.host}:{self.port};databaseName={self.database};user={self.username};password={self.password};encrypt=false;trustServerCertificate=false'

    def build_passord(self):
        return str(self.connection_params['password'])
