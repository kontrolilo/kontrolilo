# -*- coding: utf-8 -*-
from tests.integration.base_gradle import GradleCheckBase


class TestGradleCheckKotlin(GradleCheckBase):
    def get_language(self) -> str:
        return 'kotlin'
