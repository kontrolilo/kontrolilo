# Changelog

<!--next-version-placeholder-->

## v1.8.0 (2021-06-09)
### Feature
* License list is sorted when linting ([`80884ed`](https://github.com/nbyl/pre-commit-license-checks/commit/80884ed2933752ded16ae8808dfccdbfb69051fe))
* Create new linter for configuration files ([`7a3d42d`](https://github.com/nbyl/pre-commit-license-checks/commit/7a3d42d0c151545d8d8675f0c3ae4019ed88d080))

## v1.7.0 (2021-06-07)
### Feature
* Invalidate cached urls on error ([`3d10542`](https://github.com/nbyl/pre-commit-license-checks/commit/3d1054297fecb53781683d4e786ded9e308b713c))

## v1.6.0 (2021-05-25)
### Feature
* Add support to check licenses against a gradle setup ([`16c3744`](https://github.com/nbyl/pre-commit-license-checks/commit/16c374403e6087cfffecddbe0ee370ba0ecf02e0))

## v1.5.0 (2021-05-20)
### Feature
* Maven checker uses wrapper when present ([`a71fe9e`](https://github.com/nbyl/pre-commit-license-checks/commit/a71fe9e6d7428c64dfce10fd6f95ce36235f9357))
* Maven parser can now parse the licenses of a maven project ([`996d3b5`](https://github.com/nbyl/pre-commit-license-checks/commit/996d3b5d12db1b806feeb0300f615d775f62f8c2))

### Documentation
* Consolidate the configuration docs ([`7072aff`](https://github.com/nbyl/pre-commit-license-checks/commit/7072aff47e0e3fb236b21a7685ba4e8ccfe838e7))

## v1.4.0 (2021-05-19)
### Feature
* Cache external configuration for one day ([`48dabef`](https://github.com/nbyl/pre-commit-license-checks/commit/48dabefb8b9f1045dbc7ddc3a8206ac16007983b))

## v1.3.1 (2021-05-17)
### Fix
* Add requsts library as explicit dependency ([`54ddaca`](https://github.com/nbyl/pre-commit-license-checks/commit/54ddaca4bf56a1bab619b3f6af9c62af87cd2a58))

## v1.3.0 (2021-05-13)
### Feature
* Include other configuration file from external url ([`3b59ae1`](https://github.com/nbyl/pre-commit-license-checks/commit/3b59ae16e4c9410c87248b3b86ed0ae5cab25674))

## v1.2.0 (2021-05-12)
### Feature
* Make startup scripts more robust ([`39806b4`](https://github.com/nbyl/pre-commit-license-checks/commit/39806b4df67ac48da9d83795148ee2142111d7c2))

## v1.1.1 (2021-05-11)
### Fix
* Suppress output of license tools unless debug is set ([`6220cb9`](https://github.com/nbyl/pre-commit-license-checks/commit/6220cb9cea4c957a92a7d04475a1386b6d7ee0a7))

## v1.1.0 (2021-05-11)
### Feature
* Make exclusion more general and add it to npm as well ([`fd48b28`](https://github.com/nbyl/pre-commit-license-checks/commit/fd48b28badbbcb10524e36506dd17cce818ad171))
* Print file warning only, when config file is not yet present ([`bc54f63`](https://github.com/nbyl/pre-commit-license-checks/commit/bc54f630571296b27ce6dbb1961f674c53ede600))
* Print list of offending packages and their licenses ([`0891bb4`](https://github.com/nbyl/pre-commit-license-checks/commit/0891bb48dc9ef9f3ca85d4fc88466d2f7a59db72))

### Documentation
* Add badges for code climate ([`6b92adb`](https://github.com/nbyl/pre-commit-license-checks/commit/6b92adb9ae43c11889f60f32d2bce389c76283a9))

## v1.0.1 (2021-05-10)
### Fix
* Make npm less noisy when running install ([`a775325`](https://github.com/nbyl/pre-commit-license-checks/commit/a775325c591c14712644de73cadd79a63bac1887))

### Documentation
* Clarify output ([`6ae39ea`](https://github.com/nbyl/pre-commit-license-checks/commit/6ae39ead5b585522d50ab6534675316fb2e19317))
* Don't use brackets ([`05a5343`](https://github.com/nbyl/pre-commit-license-checks/commit/05a5343713e62b4db9808df351960f788d939f48))
* Add shiny badges ([`663afcb`](https://github.com/nbyl/pre-commit-license-checks/commit/663afcb50377785abacf0cb66312393e82bdf6b9))

## v1.0.0 (2021-05-07)
### Feature
* Unit tests are now finished ([`902820f`](https://github.com/nbyl/pre-commit-license-checks/commit/902820f792d68ac532f38f34ab074df7796c42ba))
* Checker can now check npm for licenses ([`aedec33`](https://github.com/nbyl/pre-commit-license-checks/commit/aedec33aea8c5c5dfa6390b5777e7f08c4feb715))
* Add skeleton for node checker ([`640199e`](https://github.com/nbyl/pre-commit-license-checks/commit/640199e2277be1eaf2b57c9a8642f918656ee7a9))

### Fix
* Rollback release because of wrong merge order ([`651dc35`](https://github.com/nbyl/pre-commit-license-checks/commit/651dc35af0ae2e227ca1b4fe89286aa076c72ced))
* Tests are failing ([`90b6d1f`](https://github.com/nbyl/pre-commit-license-checks/commit/90b6d1f3549f4f13d7ca705c4bec98cd6f101182))

### Breaking
* this changes the name and URL of the project  ([`08fbc74`](https://github.com/nbyl/pre-commit-license-checks/commit/08fbc74490549cea939d67f76cdab4d6f836c54a))
* this changes the commandline from the hooks file  ([`cba9dfb`](https://github.com/nbyl/pre-commit-license-checks/commit/cba9dfb5d33c77f4e66c28e7090265d0a6c0a0f5))
* this changes the calling package from pre-commit  ([`df95b1f`](https://github.com/nbyl/pre-commit-license-checks/commit/df95b1f3dc76439fe4f294b9b00ed3555fae17bc))

### Documentation
* Fix description ([`53fee57`](https://github.com/nbyl/pre-commit-license-checks/commit/53fee575f66a79ef58ead418fb095b8d9eb32012))

## v0.4.0 (2021-05-05)


## v0.3.0 (2021-05-05)


## v0.2.0 (2021-05-05)
### Feature
* Test automatic release ([`514c6a2`](https://github.com/nbyl/pre-commit-license-checks/commit/514c6a2eae7300c7f5bcc9f32d488ccc5c5412ed))
* Test automatic release ([`9407591`](https://github.com/nbyl/pre-commit-license-checks/commit/94075914bc2262ac9b10b697a2a98a0fb667bc30))

## v0.1.0 (2021-05-04)
### Feature
* Implement package exclusion ([`8d1e1c8`](https://github.com/nbyl/pre-commit-license-checks/commit/8d1e1c86346ceda5a218c455c09fb671fdb1e2aa))
* Check against allowed licenses ([`03ccef7`](https://github.com/nbyl/pre-commit-license-checks/commit/03ccef787f1760da6b516f8c47fa72dae378a596))
* Scan for paths to be tested ([`c166975`](https://github.com/nbyl/pre-commit-license-checks/commit/c166975eb6276bd7a2c1f21a0bf2c68c806d0e9b))

### Documentation
* Add first version of contribution guideline ([`b149dd5`](https://github.com/nbyl/pre-commit-license-checks/commit/b149dd5be2f30f5b84b9895b4b4248aebd1fc5e2))
* Add toc to readme ([`75eca8d`](https://github.com/nbyl/pre-commit-license-checks/commit/75eca8dae8fd1a69c2567f3dcf0e85485b176aa9))

## v0.1.0 (2021-05-04)
### Feature
* Implement package exclusion ([`8d1e1c8`](https://github.com/nbyl/pre-commit-license-checks/commit/8d1e1c86346ceda5a218c455c09fb671fdb1e2aa))
* Check against allowed licenses ([`03ccef7`](https://github.com/nbyl/pre-commit-license-checks/commit/03ccef787f1760da6b516f8c47fa72dae378a596))
* Scan for paths to be tested ([`c166975`](https://github.com/nbyl/pre-commit-license-checks/commit/c166975eb6276bd7a2c1f21a0bf2c68c806d0e9b))

### Documentation
* Add first version of contribution guideline ([`b149dd5`](https://github.com/nbyl/pre-commit-license-checks/commit/b149dd5be2f30f5b84b9895b4b4248aebd1fc5e2))
* Add toc to readme ([`75eca8d`](https://github.com/nbyl/pre-commit-license-checks/commit/75eca8dae8fd1a69c2567f3dcf0e85485b176aa9))
