# 0.18.2 (Tue Dec 12 2023)

:tada: This release contains work from a new contributor! :tada:

Thank you, null[@merelvdthiel](https://github.com/merelvdthiel), for all your work!

#### 🐛 Bug Fix

- update upstream path contributors file [#84](https://github.com/MIPLabCH/nigsp/pull/84) ([@merelvdthiel](https://github.com/merelvdthiel))

#### 📝 Documentation

- Fix documentation build and API [#80](https://github.com/MIPLabCH/nigsp/pull/80) ([@smoia](https://github.com/smoia))
- Add Furo theme to the documentation build [#70](https://github.com/MIPLabCH/nigsp/pull/70) ([@mscheltienne](https://github.com/mscheltienne) [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### ⚠️ Tests

- Use assert_allclose from numpy.testing instead of np.allclose in matrix comparison tests [#69](https://github.com/MIPLabCH/nigsp/pull/69) ([@mscheltienne](https://github.com/mscheltienne))

#### 🏠 Internal

- Bump actions/setup-python from 4 to 5 [#85](https://github.com/MIPLabCH/nigsp/pull/85) ([@dependabot[bot]](https://github.com/dependabot[bot]))
- [pre-commit.ci] pre-commit autoupdate [#79](https://github.com/MIPLabCH/nigsp/pull/79) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))
- Bump actions/checkout from 3 to 4 [#78](https://github.com/MIPLabCH/nigsp/pull/78) ([@dependabot[bot]](https://github.com/dependabot[bot]))
- int: Update actions versions [#78](https://github.com/MIPLabCH/nigsp/pull/78) ([@smoia](https://github.com/smoia))

#### Authors: 5

- [@dependabot[bot]](https://github.com/dependabot[bot])
- [@merelvdthiel](https://github.com/merelvdthiel)
- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Mathieu Scheltienne ([@mscheltienne](https://github.com/mscheltienne))
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.18.1 (Wed Aug 16 2023)

#### 🐛 Bug Fix

- Fix computation of degree matrix (from normal matrix to its adjacency) [#67](https://github.com/MIPLabCH/nigsp/pull/67) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- [pre-commit.ci] pre-commit autoupdate [#65](https://github.com/MIPLabCH/nigsp/pull/65) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]) [@smoia](https://github.com/smoia))

#### Authors: 2

- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.18.0 (Mon May 29 2023)

#### 🚀 Enhancement

- Add settings to consider self-loops when computing Laplacians [#64](https://github.com/MIPLabCH/nigsp/pull/64) ([@smoia](https://github.com/smoia) [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))
- docs: Save DOI badge version [#64](https://github.com/MIPLabCH/nigsp/pull/64) ([@smoia](https://github.com/smoia))

#### 📝 Documentation

- Update contributions [#62](https://github.com/MIPLabCH/nigsp/pull/62) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- Add codespell to code checks [#60](https://github.com/MIPLabCH/nigsp/pull/60) ([@smoia](https://github.com/smoia))
- Attempt to fix the auto release error [#61](https://github.com/MIPLabCH/nigsp/pull/61) ([@smoia](https://github.com/smoia))
- int: update CI/CD Ubuntu version [#58](https://github.com/MIPLabCH/nigsp/pull/58) ([@smoia](https://github.com/smoia))

#### Authors: 2

- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.17.0 (Tue Apr 18 2023)

#### 💥 Breaking Change during development

- Improve extension handling, and make `.tsv.gz` the default extension [#57](https://github.com/MIPLabCH/nigsp/pull/57) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- [pre-commit.ci] pre-commit autoupdate [#56](https://github.com/MIPLabCH/nigsp/pull/56) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### Authors: 2

- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.16.1 (Tue Apr 04 2023)

#### 🐛 Bug Fix

- fix: If the matrix diagonal is zeroed, zero the identity matrix ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.16.0 (Thu Mar 30 2023)

:tada: This release contains work from a new contributor! :tada:

Thank you, null[@NawalK](https://github.com/NawalK), for all your work!

#### 🚀 Enhancement

- Add map of filetypes to related loading functions for matricial data (`io.LOADMAT_DICT`) [#55](https://github.com/MIPLabCH/nigsp/pull/55) ([@smoia](https://github.com/smoia))
- Add outflow random walk normalisation (and specify former random walk as inflow random walk) [#54](https://github.com/MIPLabCH/nigsp/pull/54) ([@smoia](https://github.com/smoia))

#### 📝 Documentation

- Add logo folder with guidelines, eps and png files [#52](https://github.com/MIPLabCH/nigsp/pull/52) ([@NawalK](https://github.com/NawalK))

#### 🏠 Internal

- [pre-commit.ci] pre-commit autoupdate [#53](https://github.com/MIPLabCH/nigsp/pull/53) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))
- [pre-commit.ci] pre-commit autoupdate [#51](https://github.com/MIPLabCH/nigsp/pull/51) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))
- [pre-commit.ci] pre-commit autoupdate [#50](https://github.com/MIPLabCH/nigsp/pull/50) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))
- [pre-commit.ci] pre-commit autoupdate [#49](https://github.com/MIPLabCH/nigsp/pull/49) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### Authors: 3

- [@NawalK](https://github.com/NawalK)
- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.15.0 (Fri Dec 23 2022)

#### 🚀 Enhancement

- Adjust `io.load_nifti_get_mask` to expect 4 dimensions in timeseries and 3 in masks by default [#48](https://github.com/MIPLabCH/nigsp/pull/48) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- [pre-commit.ci] pre-commit autoupdate [#47](https://github.com/MIPLabCH/nigsp/pull/47) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### Authors: 2

- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.14.0 (Thu Dec 15 2022)

#### 💥 Breaking Change during development

- Make FC a metric with optional computation [#24](https://github.com/MIPLabCH/nigsp/pull/24) ([@smoia](https://github.com/smoia) [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### 🏠 Internal

- [pre-commit.ci] pre-commit autoupdate [#46](https://github.com/MIPLabCH/nigsp/pull/46) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### Authors: 2

- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.13.0 (Wed Dec 07 2022)

#### 🚀 Enhancement

- Add timeseries resizing methods and improve colorbar plotting options [#43](https://github.com/MIPLabCH/nigsp/pull/43) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- Bump actions/checkout from 2 to 3 [#44](https://github.com/MIPLabCH/nigsp/pull/44) ([@dependabot[bot]](https://github.com/dependabot[bot]))
- Bump actions/setup-python from 2 to 4 [#45](https://github.com/MIPLabCH/nigsp/pull/45) ([@dependabot[bot]](https://github.com/dependabot[bot]))

#### Authors: 2

- [@dependabot[bot]](https://github.com/dependabot[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.12.2 (Wed Dec 07 2022)

#### 🐛 Bug Fix

- Add dependabot config to keep GitHub actions up-to date [#42](https://github.com/MIPLabCH/nigsp/pull/42) ([@mscheltienne](https://github.com/mscheltienne))

#### Authors: 1

- Mathieu Scheltienne ([@mscheltienne](https://github.com/mscheltienne))

---

# 0.12.1 (Fri Dec 02 2022)

:tada: This release contains work from a new contributor! :tada:

Thank you, Mathieu Scheltienne ([@mscheltienne](https://github.com/mscheltienne)), for all your work!

#### 🐛 Bug Fix

- Synchronise required packages versions and add DS_Store to .gitignore [#41](https://github.com/MIPLabCH/nigsp/pull/41) ([@mscheltienne](https://github.com/mscheltienne))

#### 🏠 Internal

- [pre-commit.ci] pre-commit autoupdate [#39](https://github.com/MIPLabCH/nigsp/pull/39) ([@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### Authors: 2

- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Mathieu Scheltienne ([@mscheltienne](https://github.com/mscheltienne))

---

# 0.12.0 (Mon Nov 28 2022)

#### 💥 Breaking Change during development

- Add laplacian computation and normalisation independent functions [#36](https://github.com/MIPLabCH/nigsp/pull/36) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.11.0 (Wed Nov 23 2022)

#### 🚀 Enhancement

- Add edges vs nodes plotting, improve plotting in general [#35](https://github.com/MIPLabCH/nigsp/pull/35) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.10.1 (Mon Nov 21 2022)

#### 🐛 Bug Fix

- Fix initialisation (remove test packages) [#37](https://github.com/MIPLabCH/nigsp/pull/37) (s.moia@bcbl.eu)

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.10.0 (Mon Nov 21 2022)

#### 🚀 Enhancement

- Add function to recompose laplacian from eigenvalues and eigenvectors [#34](https://github.com/MIPLabCH/nigsp/pull/34) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.9.0 (Wed Oct 12 2022)

#### 🚀 Enhancement

- Add possibility (1) to specify which diagonal to use for matrices symmetric normalisation and (2) to avoid "0" elements in the diagonal [#29](https://github.com/MIPLabCH/nigsp/pull/29) ([@smoia](https://github.com/smoia))
- Add duecredit to keep track of citations [#27](https://github.com/MIPLabCH/nigsp/pull/27) ([@smoia](https://github.com/smoia))
- int: Bump up github-action-x/commit to 2.9 [#27](https://github.com/MIPLabCH/nigsp/pull/27) ([@smoia](https://github.com/smoia))

#### 💻 Refactored

- Apply automatic formatting (black & isort) on code (tests and push) [#26](https://github.com/MIPLabCH/nigsp/pull/26) ([@smoia](https://github.com/smoia))

#### 🐛 Bug Fix

- Remove auto restyling in tests and PR merges given pre-commit [#33](https://github.com/MIPLabCH/nigsp/pull/33) ([@smoia](https://github.com/smoia))
- Fix diagonal matrix check in `operations.laplacian.symmetric_normalisation` [#32](https://github.com/MIPLabCH/nigsp/pull/32) ([@smoia](https://github.com/smoia))

#### ⚠️ Pushed to `master`

- int: Remove empty line in config ([@smoia](https://github.com/smoia))
- int: Fix path for black formatting ([@smoia](https://github.com/smoia))

#### ⚠️ Tests

- Add style check test (flake8) [#25](https://github.com/MIPLabCH/nigsp/pull/25) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- Add isort, flake8, pydocstyle, and rst pre-coomit hooks (and dev dependencies) [#31](https://github.com/MIPLabCH/nigsp/pull/31) ([@smoia](https://github.com/smoia))
- Add pre-commit to repository [#30](https://github.com/MIPLabCH/nigsp/pull/30) ([@smoia](https://github.com/smoia) [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot]))

#### Authors: 2

- [@pre-commit-ci[bot]](https://github.com/pre-commit-ci[bot])
- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.8.0 (Thu Aug 25 2022)

#### 💥 Breaking Change during development

- Express SDI as log2 of bands quotient [#23](https://github.com/MIPLabCH/nigsp/pull/23) ([@smoia](https://github.com/smoia))

#### ⚠️ Pushed to `master`

- docs: Update documentation home page ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.7.1 (Mon Aug 22 2022)

#### 🐛 Bug Fix

- Fix metric plot threshold [#22](https://github.com/MIPLabCH/nigsp/pull/22) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.7.0 (Mon Aug 22 2022)

#### 💥 Breaking Change during development

- Add extensive testing and fixs issues [#16](https://github.com/MIPLabCH/nigsp/pull/16) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- Fix minor documentation issues [#21](https://github.com/MIPLabCH/nigsp/pull/21) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.6.1 (Mon Jul 18 2022)

#### 🐛 Bug Fix

- Fix issues with documentation and automatise API [#20](https://github.com/MIPLabCH/nigsp/pull/20) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.6.0 (Thu Jul 14 2022)

#### 🚀 Enhancement

- Implement multi-index (bandpass-like) graph split [#18](https://github.com/MIPLabCH/nigsp/pull/18) ([@smoia](https://github.com/smoia))

#### 📝 Documentation

- Add documentation structure, CLI, API, and installation. [#17](https://github.com/MIPLabCH/nigsp/pull/17) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.5.0 (Thu Jul 07 2022)

#### 🚀 Enhancement

- Handling averages of masked data better [#15](https://github.com/MIPLabCH/nigsp/pull/15) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.4.1 (Thu Jul 07 2022)

#### 🐛 Bug Fix

- Fix p value for Bernoulli's test [#14](https://github.com/MIPLabCH/nigsp/pull/14) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.4.0 (Thu Jul 07 2022)

#### 🚀 Enhancement

- Allow users to choose p value for both frequentist and Bernoulli's approach at all time. [#13](https://github.com/MIPLabCH/nigsp/pull/13) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.3.0 (Tue Jul 05 2022)

#### 💥 Breaking Change during development

- Improve random seed generator initialisation following latest recommendations and bump up required numpy version [#12](https://github.com/MIPLabCH/nigsp/pull/12) ([@smoia](https://github.com/smoia))

#### 💻 Refactored

- Small code improvement in io.py [#11](https://github.com/MIPLabCH/nigsp/pull/11) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.2.0 (Tue May 03 2022)

#### 💥 Breaking Change during development

- Change name of function `if_declare_force_type` to `change_var_type` to better match its new scope. [#10](https://github.com/MIPLabCH/nigsp/pull/10) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.1.3 (Tue May 03 2022)

#### 🐛 Bug Fix

- fix: Fix random seed initialisation ([@smoia](https://github.com/smoia))

#### ⚠️ Pushed to `master`

- docs: Fix citations ([@smoia](https://github.com/smoia))
- docs: Fix non-pip installation instructions ([@smoia](https://github.com/smoia))

#### ⚠️ Tests

- Add nifti io unit tests [#7](https://github.com/MIPLabCH/nigsp/pull/7) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- Do not save cache in CI builds (not needed) [#9](https://github.com/MIPLabCH/nigsp/pull/9) ([@smoia](https://github.com/smoia))
- Fix coverage settings to exclude tests and other minor elements [#8](https://github.com/MIPLabCH/nigsp/pull/8) ([@smoia](https://github.com/smoia))
- Fix coverage list [#6](https://github.com/MIPLabCH/nigsp/pull/6) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.1.2 (Wed Mar 23 2022)

#### ⚠️ Pushed to `master`

- Update README.md ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.1.1 (Wed Mar 23 2022)

#### ⚠️ Pushed to `master`

- Update README.md ([@smoia](https://github.com/smoia))

#### ⚠️ Tests

- Setup CircleCI for CI workflows [#4](https://github.com/MIPLabCH/nigsp/pull/4) ([@smoia](https://github.com/smoia))
- Fix break tests [#2](https://github.com/MIPLabCH/nigsp/pull/2) ([@smoia](https://github.com/smoia))

#### 🏠 Internal

- Add short documentation in README and mailmap [#5](https://github.com/MIPLabCH/nigsp/pull/5) ([@smoia](https://github.com/smoia))

#### Authors: 1

- Stefano Moia ([@smoia](https://github.com/smoia))

---

# 0.1.0 (Mon Mar 21 2022)

:tada: This release contains work from a new contributor! :tada:

Thank you, Stefano Moia ([@smoia](https://github.com/smoia)), for all your work!

#### 🚀 Enhancement

- Update `auto` configuration and enable CD workflows [#1](https://github.com/MIPLabCH/nigsp/pull/1) (s.moia@bcbl.eu [@smoia](https://github.com/smoia))

#### ⚠️ Pushed to `master`

- Fix internal settings (s.moia@bcbl.eu)
- Fix matrices loading (s.moia@bcbl.eu)
- Remove initial check on var (s.moia@bcbl.eu)
- Fix tests (s.moia@bcbl.eu)
- Improve data interpretation (s.moia@bcbl.eu)
- Fix node strength computation (s.moia@bcbl.eu)
- Fix extension check (s.moia@bcbl.eu)
- Fix testdir (s.moia@bcbl.eu)
- Fix integration test and add configuration (s.moia@bcbl.eu)
- Improve markerplot creation and force nilearn to be at least 0.7 (s.moia@bcbl.eu)
- Add markerplot plot as a block (s.moia@bcbl.eu)
- Fix markerplot creation and add plot of masked metrics (s.moia@bcbl.eu)
- Fix matrix export (s.moia@bcbl.eu)
- Workflow debug, plot metric nodes, improve logger (s.moia@bcbl.eu)
- Improve plot log text (s.moia@bcbl.eu)
- Generalise functions by allowing 4+ dimensions to be worked with (s.moia@bcbl.eu)
- Fix statistical tests and improve logging (s.moia@bcbl.eu)
- Fix surrogate creation for 3+D (s.moia@bcbl.eu)
- Fix atlas unfolding (s.moia@bcbl.eu)
- Set default metric average to False (s.moia@bcbl.eu)
- Fix metric calculation in objects (s.moia@bcbl.eu)
- Fix log messages in io (s.moia@bcbl.eu)
- Add seed and fix surrogates flags (s.moia@bcbl.eu)
- Fix GSDI export (s.moia@bcbl.eu)
- Debug 2 (s.moia@bcbl.eu)
- Fix outdir path generation when missing input (s.moia@bcbl.eu)
- Fix integration import (s.moia@bcbl.eu)
- Change workflow script name to avoid python confusions (s.moia@bcbl.eu)
- Fix commonpath attribution (s.moia@bcbl.eu)
- Ignore idea folder (s.moia@bcbl.eu)
- Debug 1 (s.moia@bcbl.eu)
- Add optional arguments in CLI (s.moia@bcbl.eu)
- Fix imports (s.moia@bcbl.eu)
- Fix message (s.moia@bcbl.eu)
- Add integration test (s.moia@bcbl.eu)
- Update p value (s.moia@bcbl.eu)
- Update name! (s.moia@bcbl.eu)
- Fix statistical test (s.moia@bcbl.eu)
- Fix fourier transformation (s.moia@bcbl.eu)
- Remove some action comments (s.moia@bcbl.eu)
- Remove unused imports (s.moia@bcbl.eu)
- Other minor fixes and check inputs in workflows (s.moia@bcbl.eu)
- !!! Fix graph projection creation and change name to fourier transform (s.moia@bcbl.eu)
- Add more tests and test files (s.moia@bcbl.eu)
- Add parser (s.moia@bcbl.eu)
- Little export progresses (s.moia@bcbl.eu)
- Main development (s.moia@bcbl.eu)
- More internal settings, start workflow (s.moia@bcbl.eu)
- Bunch of internal settings (s.moia@bcbl.eu)
- Initial commit ([@smoia](https://github.com/smoia))

#### Authors: 2

- smoia (s.moia@bcbl.eu)
- Stefano Moia ([@smoia](https://github.com/smoia))
