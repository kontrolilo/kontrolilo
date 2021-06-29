---
title: "Contributing"
weight: 30
---

### Guide

A contribution guide can be found in [CONTRIBUTING.md](https://github.com/kontrolilo/kontrolilo/blob/main/CONTRIBUTING.md)

### Documentation

The documentation is built using [hugo](https://gohugo.io) and [hugo-theme-learn](https://themes.gohugo.io//theme/hugo-theme-learn/en). The theme is included in the repository using the `git submodule` command. To update the theme to the latest version, use the follwing commands:

```bash
git remote add theme https://github.com/matcornic/hugo-theme-learn.git
git fetch theme master
 it subtree pull --prefix docs/themes/hugo-theme-learn theme master --squash
```
