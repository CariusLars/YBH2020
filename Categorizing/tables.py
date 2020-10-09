# Declare your table
from flask_table import Table, Col, LinkCol, ButtonCol


class SupportItemTableView(Table):
    in_id = Col('Id', attr_list = ['input', 'id'])
    in_timestamp = Col('Time', attr_list=['input', 'timestamp'])
    in_message = Col('Message', attr_list=['input', 'message'])
    in_user_name = Col('User Name', attr_list=['input', 'user_name'])
    in_contact_details = Col('User Contact', attr_list=[
                             'input', 'contact_details'])
    out_timestamp = Col('Time processed', attr_list=['output', 'timestamp'])
    out_extreme_negative = Col('Extreme Negative', attr_list=['output', 'extreme_negative'])
    out_category = Col('Category', attr_list=['output', 'category'])
    out_category_score = Col('Category Score', attr_list=['output', 'category_score'])
    out_assignee = Col('Assignee', attr_list=['output', 'assignee'])
    out_answers = Col('Answers', attr_list=['output', 'answers'])


class SupportItemTableEdit(Table):
    in_id = Col('Id', attr_list=['input', 'id'])
    in_timestamp = Col('Time', attr_list=['input', 'timestamp'])
    in_message = Col('Message', attr_list=['input', 'message'])
    in_user_name = Col('User Name', attr_list=['input', 'user_name'])
    in_contact_details = Col('User Contact', attr_list=[
        'input', 'contact_details'])
    out_timestamp = Col('Time processed', attr_list=['output', 'timestamp'])
    out_extreme_negative = Col('Extreme Negative', attr_list=['output', 'extreme_negative'])
    out_category = Col('Category', attr_list=['output', 'category'])
    out_category_score = Col('Category Score', attr_list=['output', 'category_score'])
    out_assignee = Col('Assignee', attr_list=['output', 'assignee'])
    out_answers = Col('Answers', attr_list=['output', 'answers'])

    action_del = ButtonCol('Delete', 'deleteRequestCallback',
                           url_kwargs=dict(id=['input', 'user_name']))
    action_reply = ButtonCol('Reply', 'replyRequestCallback',
                             url_kwargs=dict(id=['input', 'user_name']))
