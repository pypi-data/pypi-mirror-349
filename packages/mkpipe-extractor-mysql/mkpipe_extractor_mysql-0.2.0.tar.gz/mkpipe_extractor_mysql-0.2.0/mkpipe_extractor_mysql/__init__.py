from mkpipe.functions_spark import BaseExtractor


class MysqlExtractor(BaseExtractor):
    def __init__(self, config, settings):
        super().__init__(
            config,
            settings,
            driver_name='mysql',
            driver_jdbc='com.mysql.cj.jdbc.Driver',
        )
