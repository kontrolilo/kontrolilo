# -*- coding: utf-8 -*-
from tests.integration.base_gradle import GradleCheckBase


class TestGradleCheckJava(GradleCheckBase):
    def get_language(self) -> str:
        return 'java'
