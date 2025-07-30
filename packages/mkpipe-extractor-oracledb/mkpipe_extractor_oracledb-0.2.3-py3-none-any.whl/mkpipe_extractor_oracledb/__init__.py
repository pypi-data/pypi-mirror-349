from mkpipe.functions_spark import BaseExtractor


class OracledbExtractor(BaseExtractor):
    def __init__(self, config, settings):
        super().__init__(
            config,
            settings,
            driver_name='oracle:thin',
            driver_jdbc='oracle.jdbc.OracleDriver',
        )

    def build_jdbc_url(self):
        return f'jdbc:{self.driver_name}:{self.username}/{self.password}@//{self.host}:{self.port}/{self.database}?oracle.jdbc.defaultNChar=true'

    def normalize_partitions_column(self, col: str):
        return '"' + col.split(' as ')[0].strip() + '"'
