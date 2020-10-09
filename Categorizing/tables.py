# Declare your table
from flask_table import Table, Col


class SupportItemTable(Table):
    name = Col('Name')
    topic = Col('Topic')
