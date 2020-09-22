from textwrap import dedent

from pytest import mark, raises


def test_login(session):
    res = session.validate()
    assert set(res.keys()) == {
        'groups', 'owned_date', 'site', 'script_direction', 'warning', 
        'sys_user_id', 'is_enabled', 'modified_date', 'owned_by', 
        'cooperator_id', 'modified_by', 'sys_lang_id', 'created_by', 
        'site_id', 'user_name', 'created_date', 'login_token'
    }