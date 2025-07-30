import os
from mkpipe.functions_spark import BaseExtractor


class SqliteExtractor(BaseExtractor):
    def __init__(self, config, settings):
        super().__init__(
            config,
            settings,
            driver_name='sqlite',
            driver_jdbc='org.sqlite.JDBC',
        )

    def build_jdbc_url(self):
        self.db_path = os.path.abspath(self.connection_params['db_path'])
        return f'jdbc:sqlite:{self.db_path}'
