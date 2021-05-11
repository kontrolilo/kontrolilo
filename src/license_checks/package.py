# -*- coding: utf-8 -*-
class Package:
    name: str
    version: str
    license: str

    def __init__(self,
                 name: str,
                 version: str,
                 license: str) -> None:
        super().__init__()

        self.name = name
        self.version = version
        self.license = license

    def __repr__(self) -> str:
        return f'Package(name={self.name},version={self.version},license={self.license})'

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version and self.license == other.license
