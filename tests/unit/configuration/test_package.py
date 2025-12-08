from kontrolilo.configuration.package import Package


class TestPackage:
    def test_repr(self):
        assert repr(Package('starlette', '0.14.1',
                            'BSD License')) == 'Package(name=starlette,version=0.14.1,license=BSD License)'

    def test_eq(self):
        assert Package('starlette', '0.14.1', 'BSD License').__eq__(
            Package('starlette', '0.14.1', 'BSD License')) == True
