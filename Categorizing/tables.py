# Declare your table
from flask_table import Table, Col, LinkCol, ButtonCol


class SupportItemTable(Table):
    in_timestamp = Col('Time', attr_list=['input', 'timestamp'])
    in_message = Col('Message', attr_list=['input', 'message'])
    in_user_name = Col('User Name', attr_list=['input', 'user_name'])
    in_contact_details = Col('User Contact', attr_list=[
                             'input', 'contact_details'])
    out_timestamp = Col('Time processed', attr_list=['output', 'timestamp'])
    out_sentiment = Col('Sentiment', attr_list=['output', 'sentiment'])
    out_assignee = Col('Assignee', attr_list=['output', 'assignee'])
    out_answers = Col('Answers', attr_list=['output', 'answers'])

    # actions = LinkCol('View', 'delete_fn')  # , url_kwargs=dict(id='id'))
    action_del = ButtonCol('Delete', 'deleteRequestCallback',
                           url_kwargs=dict(id=['input', 'user_name']))

    # name = Col('Name')
    # topic = Col('Topic')
