# Declare your table
from flask_table import Table, Col, LinkCol, ButtonCol


class SupportItemTableView(Table):
    in_id = Col('Request-ID', attr_list = ['input', 'id'])
    in_timestamp = Col('Zeitstempel', attr_list=['input', 'timestamp'])
    in_message = Col('Nachricht', attr_list=['input', 'message'])
    in_user_name = Col('Name', attr_list=['input', 'user_name'])
    #in_contact_details = Col('Kontakt-ID', attr_list=[
    #                         'input', 'contact_details'])
    #out_timestamp = Col('Time processed', attr_list=['output', 'timestamp'])
    out_extreme_negative = Col('Beschwerde - Warnung', attr_list=['output', 'extreme_negative'])
    out_category = Col('Kategorie', attr_list=['output', 'category'])
    out_category_score = Col('Kategorie Score', attr_list=['output', 'category_score'])
    out_assignee = Col('Mitarbeiter', attr_list=['output', 'assignee'])
    #out_answers = Col('Answers', attr_list=['output', 'answers'])


class SupportItemTableEdit(Table):
    in_id = Col('Request-ID', attr_list=['input', 'id'])
    in_timestamp = Col('Zeitstempel', attr_list=['input', 'timestamp'])
    in_message = Col('Nachricht', attr_list=['input', 'message'])
    in_user_name = Col('Name', attr_list=['input', 'user_name'])
    #in_contact_details = Col('Kontakt-ID', attr_list=[
    #    'input', 'contact_details'])
    #out_timestamp = Col('Time processed', attr_list=['output', 'timestamp'])
    out_extreme_negative = Col('Beschwerde - Warnung', attr_list=['output', 'extreme_negative'])
    out_category = Col('Kategorie', attr_list=['output', 'category'])
    out_category_score = Col('Kategorie Score', attr_list=['output', 'category_score'])
    out_assignee = Col('Mitarbeiter', attr_list=['output', 'assignee'])
    #out_answers = Col('Answers', attr_list=['output', 'answers'])

    action_del = ButtonCol('', 'deleteRequestCallback',
                           url_kwargs=dict(id=['input', 'user_name']))
    action_reply = ButtonCol('', 'replyRequestCallback',
                             url_kwargs=dict(id=['input', 'id']))
