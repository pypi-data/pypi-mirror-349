from typing import List

from asana import StoriesApi

from my_asana.authenticate import get_stories_api, get_tasks_api
from my_asana.users import Users


def tag_user_in_comment(user_id: str) -> str:
    return f'<a data-asana-gid="{user_id}"/>'


def add_comment_to_task(task_id: str, comment: str):
    stories_api: StoriesApi = get_stories_api()

    body = {
        "data": {
            "html_text": comment
        }
    }
    opts = {
        'opt_fields': "html_text"
    }

    stories_api.create_story_for_task(
        task_gid=task_id,
        body=body,
        opts=opts
    )


def add_followers_to_task(task_id: str):
    body = {
        "data": {
            "followers": [user.user_id for user in [Users.ORI, Users.ITAMAR, Users.HILA]]
        }
    }
    opts = {}

    get_tasks_api().add_followers_for_task(body, task_id, opts)


def get_up_for_sale_again_message() -> str:
    users_str: str = "".join([tag_user_in_comment(user.user_id) for user in [Users.ORI, Users.ITAMAR, Users.HILA]])
    main_message: str = 'This property failed in contingency. It is now back on the market! Please review it.'
    html_text: str = f'<body>{users_str}\n{main_message}</body>'
    return html_text


def get_property_sold_message() -> str:
    users_str: str = "".join([tag_user_in_comment(user.user_id) for user in [Users.ORI, Users.ITAMAR, Users.HILA]])
    main_message: str = 'This property is now sold. Moving it to Decline.'
    html_text: str = f'<body>{users_str}\n{main_message}</body>'
    return html_text

def get_off_market_message() -> str:
    main_message: str = 'This property is now off-market. Moving it to Decline.'
    html_text: str = f'<body>{main_message}</body>'
    return html_text