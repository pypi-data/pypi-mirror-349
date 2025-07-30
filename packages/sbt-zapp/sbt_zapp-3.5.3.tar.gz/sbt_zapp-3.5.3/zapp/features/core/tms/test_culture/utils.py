import re
from enum import Enum
from requests.cookies import cookiejar_from_dict

from behave.model import Scenario, ScenarioOutline, Table
from behave.runner import Context

from zapp.features.core.tms.test_culture import TEST_CULTURE_LABEL_NAME

TQL_LABEL_TEMPLATE = 'space = "{space}" AND suit = "test_case" AND label IN ("{label}")'
# TQL_UNIT_TEMPLATE = 'space = "{space}" AND suit = "test_case" AND (unit = "{code}" OR old_jira_key ~ "{code}")'
TQL_UNIT_TEMPLATE = 'space = "{space}" AND suit = "test_case" AND unit = "{code}"'
TQL_OLD_JIRA_KEY_TEMPLATE = (
    'space = "{space}" AND suit = "test_case" AND old_jira_key ~ "{code}"'
)

TAG_SERACH_PATTERN = r"%s:.+"
FONT_SIZE = 12

AC21_API_COOKIES = cookiejar_from_dict({"api_swtr_as21": "true"})

allure_priority_mapping = {
    "blocker": "blocker",
    "critical": "critical",
    "normal": "major",
    "minor": "minor",
    "trivial": "trivial",
}


class ScenarioTag(Enum):
    TMS = "allure.link.tms"
    ISSUE = "allure.issue"
    OWNER = "allure.label.owner"
    LABEL = TEST_CULTURE_LABEL_NAME

    def find(self, tags) -> str | None:
        for tag in tags:
            if re.match(TAG_SERACH_PATTERN % self.value, tag):
                return tag.split(":")[-1]


def get_priority(tags) -> str:
    priorities = list(allure_priority_mapping.keys())
    for tag in tags:
        if tag in priorities:
            return allure_priority_mapping[tag]
    return allure_priority_mapping["normal"]  # Значение по умолчанию


def get_scenario(context: Context) -> Scenario | ScenarioOutline:
    if context.active_outline:
        for scenario in context.feature.scenarios:
            if scenario.tags == context.scenario.tags:
                return scenario
    else:
        return context.scenario


def get_column_widths(table: Table) -> list[int]:
    """Подсчет максимальной длины столбца таблицы"""
    rows = [table.headings] + [row.cells for row in table.rows]
    widths = [[len(str(cell)) for cell in row] for row in rows]
    return [max(column) * FONT_SIZE for column in zip(*widths)]
