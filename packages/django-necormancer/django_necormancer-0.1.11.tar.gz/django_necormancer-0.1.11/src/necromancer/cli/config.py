from InquirerPy import get_style
from InquirerPy.base.control import Choice
import pathlib


BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

CLI_STYLES = get_style({
    "questionmark": "#8BE9FD",        
    "answermark": "#50FA7B",          
    "answered_question": "#BD93F9",
    "question": "#BD93F9",
    "checkbox": "#8BE9FD",
    "pointer": "#8BE9FD",
})

CLI_SETTINGS = {
    'qmark': '?',
    'amark': '✔',
    'style': CLI_STYLES
}

PACKAGE_MANAGEMENT = [
    'pip-tools',
    Choice(value=None, name='None')
]

ENVIROMENT_SETUP_TOOLS = [
    'Make',
    Choice(value=None, name='None')
]

THIRD_PARTY_BASE_PACKAGES = []

THIRD_PARTY_DEV_PACKAGES = [
    'ipdb',
]

THIRD_PARTY_PROD_PACKAGES = []

THIRD_PARTY_PACKAGES = THIRD_PARTY_BASE_PACKAGES + THIRD_PARTY_DEV_PACKAGES + THIRD_PARTY_PROD_PACKAGES