import logging
import traceback
from typing import Optional
from test_culture_client.client import TestCultureClient
from test_culture_client.models.tql import TqlRequest

from behave.model import Scenario, ScenarioOutline

from zapp.features.core.sessions.keycloak import KeyCloakFrontSession
from zapp.features.core.tms.test_culture import (
    TEST_CULTURE_DEFAULT_FOLDER_CODE,
    TEST_CULTURE_INTEGRATION_ENABLED,
    TEST_CULTURE_UPDATE_TEST_CASE,
    TEST_CULTURE_PASSWORD,
    TEST_CULTURE_SPACE,
    TEST_CULTURE_TOKEN,
    TEST_CULTURE_URL,
    TEST_CULTURE_USERNAME,
)
from zapp.features.core.tms.test_culture.context import TestCaseContext, TestDataContext
from zapp.features.core.tms.test_culture.utils import (
    TQL_LABEL_TEMPLATE,
    TQL_UNIT_TEMPLATE,
    TQL_OLD_JIRA_KEY_TEMPLATE,
    ScenarioTag,
)

log = logging.getLogger(__name__)


class TooManyTestCasesException(Exception):
    pass


class TestCultureReporter:
    client: TestCultureClient
    space: str
    default_folder: str
    already_reported: list[str]  # Для корректной работы с ScenarioOutline
    update_test_case: bool

    def __init__(
        self,
        client: TestCultureClient,
        space: str,
        default_folder: str,
        update_test_case: bool,
    ):
        self.client = client
        self.space = space
        self.default_folder = default_folder
        self.already_reported = []
        self.update_test_case = update_test_case
        log.info("Включена интеграция с TestCulture")
        log.info(f"Обновлять тест-кейсы: {update_test_case}")

    def before_scenario(self, context, scenario):
        if self.update_test_case:
            try:
                tms_code, label, owner = self._find_attributes(scenario)
                if tms_code is None and label is None:
                    return

                code, folder = self._find(tms_code, label)
                code = (
                    self._create(context, label, owner)
                    if code is None
                    else self._update(context, code, folder, owner)
                )
                self.already_reported.append(code)
            except Exception as ex:
                log.error(
                    f"Произошла ошибка при актуализации сценария '{scenario.name}':\n{ex}"
                )
                traceback.print_exception(ex)

    def _find_attributes(
        self, scenario: Scenario | ScenarioOutline
    ) -> tuple[str, str, str]:
        tms_code = ScenarioTag.TMS.find(scenario.effective_tags)
        label = ScenarioTag.LABEL.find(scenario.effective_tags)
        owner = ScenarioTag.OWNER.find(scenario.effective_tags)

        if tms_code is None and label is None:
            log.error(
                f"Сценарий '{scenario.name}' не содержит теги '{ScenarioTag.TMS.value}' или '{ScenarioTag.LABEL.value}'"
            )
            return None, None, None
        if tms_code in self.already_reported:
            log.info(f"Сценарий {tms_code} уже был обновлен")
            return None, None, None

        return tms_code, label, owner

    def _find(self, tms_code: str, label: str) -> tuple[Optional[str], Optional[str]]:
        """В случае успеха возвращает code юнита и его папку"""
        code = None
        folder = None
        if tms_code:
            code, folder = self._find_by_tql(
                TQL_UNIT_TEMPLATE.format(code=tms_code, space=self.space)
            )
            if code is None:
                # Поиск ТК по номеру до миграции
                code, folder = self._find_by_tql(
                    TQL_OLD_JIRA_KEY_TEMPLATE.format(code=tms_code, space=self.space)
                )

        if code is None and label:
            code, folder = self._find_by_tql(
                TQL_LABEL_TEMPLATE.format(label=label, space=self.space)
            )
        return code, folder

    def _find_by_tql(self, tql: str) -> tuple[Optional[str], Optional[str]]:
        search_results = self.client.units.find_by_tql(
            TqlRequest(query=tql, attributes=["folder"])
        )
        found_elements_count = search_results["totalElements"]
        if found_elements_count > 1:
            raise TooManyTestCasesException(
                f"Найдено более одного элемента по запросу: {tql}"
            )

        if found_elements_count:
            entry = search_results["content"][0]
            return entry["unit"]["code"], entry["attributes"][0]["value"]["code"]
        return None, None

    def _create(self, context, label: str | None, owner: str | None) -> str:
        test_case_context = TestCaseContext.parse(context)
        test_case_request = test_case_context.to_create_request(self.space)
        test_case_request.attributes.folder = self.default_folder
        test_case_request.attributes.label = [label] if label else []
        test_case_request.attributes.owner = owner

        code = self.client.test_cases.create(test_case_request)["id"]
        log.info(f"Создан новый ТК: {code}")

        self._update_test_data(code, test_case_context.test_data)
        return code

    def _update(self, context, code: str, folder: str, owner: str | None) -> str:
        test_case_context = TestCaseContext.parse(context)
        test_case_request = test_case_context.to_update_request()
        test_case_request.attributes.owner = owner
        test_case_request.attributes.folder = folder

        only_updated_fields = test_case_request.model_dump(exclude_unset=True)
        code = self.client.test_cases.update(code, only_updated_fields)["id"]
        log.info(f"Обновлен ТК: {code}")

        self._update_test_data(code, test_case_context.test_data)
        return code

    def _update_test_data(self, code: str, test_data_context: TestDataContext):
        if test_data_context is not None:
            self.client.test_cases.update_test_data(
                code, test_data_context.to_request()
            )
            log.info(f"TK {code}: обновлены тестовые данные")


class StubTestCultureReporter:
    def __init__(self):
        log.info("Отключена интеграция с TestCulture")

    def before_scenario(self, context, scenario):
        pass


def _init_test_culture_reporter():
    try:
        ow_session_cookies = None
        if TEST_CULTURE_TOKEN is None:
            ow_session_cookies = (
                KeyCloakFrontSession(TEST_CULTURE_URL)
                .open(TEST_CULTURE_USERNAME, TEST_CULTURE_PASSWORD)
                .session.cookies
            )

        client = TestCultureClient(
            url=TEST_CULTURE_URL,
            token=TEST_CULTURE_TOKEN,
            cookies=ow_session_cookies,
            verify=False,
        )
        return TestCultureReporter(
            client,
            space=TEST_CULTURE_SPACE,
            default_folder=TEST_CULTURE_DEFAULT_FOLDER_CODE,
            update_test_case=TEST_CULTURE_UPDATE_TEST_CASE,
        )
    except Exception as ex:
        log.error("Не удалось создать интеграцию с TestCulture")
        traceback.print_exception(ex)
        return StubTestCultureReporter()


test_culture_reporter = (
    _init_test_culture_reporter()
    if TEST_CULTURE_INTEGRATION_ENABLED
    else StubTestCultureReporter()
)
