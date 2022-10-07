How to contribute to the `nigsp` package
========================================

## Contribution types

### Contributing with small documentation changes

If you are new to GitHub and just have a small documentation change
recommendation (such as: typos detection, small improvements in the
content, ...), please open an issue in the relative project, and label
it with the "Documentation" label. Chances are those types of changes
are easily doable with GitHub\'s online editor, which means you can do
them, or ask for help from the developers!

### Contributing with user testing

Another, non-coding friendly way to contribute to `nigsp` is by
testing the packages. There are different kinds of tests, but to
simplify things you can think mainly about automatic tests and user
tests. To know more about **Automatic tests**, you can read the [testing
section](#automatic-testing). **User testing** are warm, human, emotional and
opinionated tests that not only check that the code is doing what it
needs to do, but also whether there's a better way to do it - namely
better reports, clearer screen outputs, warnings and exceptions,
unexpected bugs that have to be corrected. If you want to perform one,
open an issue on GitHub and don't be afraid to ask questions!

### Contributing with test files

If you want a particular filetype supported, think about opening an issue or writing to the main developer with an example file - and the very good reason to add support for that filetype!

### Contributing documentation through GitHub

We use [mkdocs](https://www.mkdocs.org/) to create our
documentation. Every contribution is welcome and it follows the same
steps as a code contribution, explained below.

### Contributing code through GitHub

The best way to make this kind
of contribution, in a nutshell, is to: 1. Open an issue with the
intended modifications. 2. Label it, discuss it, (self-)assign it. 3.
Open a Pull Request (PR) to resolve the issue and label it. 4. Wait for
a review, discuss it or comply, repeat until ready. Issues and PR chats
are great to maintain track of the conversation on the contribution.
They are based upon GitHub-flavoured
[Markdown](https://daringfireball.net/projects/markdown). GitHub has a
helpful page on [getting started with writing and formatting Markdown on
GitHub](https://help.github.com/articles/getting-started-with-writing-and-formatting-on-github).

### Contributing with Pull Requests Reviews

A big challenge of software development is merging code accurately
without having to wait too much time. For this reason, Reviewers for PRs
are more than welcome! It is a task that requires some experience, but
it's very necessary! Read the [related section below](#reviewing_prs) to
start!

## Issues and Milestones

We use Issues and Milestones to keep track of and
organise our workflow.  **Issues** describe pieces of work that need to
be completed to move the project forwards. We try to keep them as simple
and clear as possible: an issue should describe a unitary, possibly
small piece of work (unless it's about refactoring). Don't be scared of
opening many issues at once, if it makes sense! Just check that what
you're proposing is not listed in a previous issue (open or closed) yet
(we don't like doubles). Issues get labelled. That helps the
contributors to know what they're about. Check the label list to know
what types are there, and use them accordingly! Issues can also be
**assigned**. If you want to work on an assigned issue, ask permission
first! - **Milestones** set the higher level workflow. They sketch
deadlines and important releases. Issues are assigned to these
milestones by the maintainers. If you feel that an issue should be
assigned to a specific milestone but the maintainers have not done so,
discuss it in the issue chat! We might have just missed it,
or we might not (yet) see how it aligns with the overall project
structure/milestone.

## Labels

The current list of labels are
[here](https://github.com/MIPLabCH/nigsp/labels). They can be used
for **Issues**, **PRs**, or both. We use
[auto](https://github.com/intuit/auto) to automate our semantic
versioning and Pypi upload, so **it\'s extremely important to use the
right PR labels**!

### Issue & PR labels

- ![Documentation](https://img.shields.io/badge/-Documentation-1D70CF?style=flat-square) Improvements or additions to documentation. This
  category includes (but is not limited to) docs pages, docstrings,
  and code comments.

- ![Duplicate](https://img.shields.io/badge/-Duplicate-CFD3D7?style=flat-square) Whatever this is, it exists already! Maybe it's a closed
  Issue/PR, that should be reopened.

- ![Enhancement](https://img.shields.io/badge/-Enhancement-A2EEEF?style=flat-square) New features added or requested. This normally goes with a `minormod` label for PRs.

- ![Outreach](https://img.shields.io/badge/-Outreach-0E8A16?style=flat-square) As part of the scientific community, we care about outreach. Check the relevant section about it, but know that this
  Issue/PR contains information or tasks about abstracts, talks,
  demonstrations, papers.

- ![Paused](https://img.shields.io/badge/-Paused-F7C38C?style=flat-square) Issue or PR should not be worked on until the resolution of other issues or PRs.

- ![released](https://img.shields.io/badge/-released-ffffff?style=flat-square) This Issue or PR has been released.

- ![Testing](https://img.shields.io/badge/-Testing-FFB5B4?style=flat-square) This is for testing features, writing tests or producing testing code. Both user testing and CI testing!

- ![Urgent](https://img.shields.io/badge/-Urgent-FFF200?style=flat-square) If you don\'t know where to start, start here! This is probably related to a milestone due soon!

### Issue-only labels

- ![BrainHack](https://img.shields.io/badge/-BrainHack-000000?style=flat-square) This issue is suggested for BrainHack participants!

- ![Bug](https://img.shields.io/badge/-Bug-D73A4A?style=flat-square) Something isn't working. It either breaks the code or has an
  unexpected outcome.

- ![Discussion](https://img.shields.io/badge/-Discussion-1C778C?style=flat-square) Discussion of a concept or implementation. These Issues
  are prone to be open ad infinitum. Jump in the conversation if you
  want!

- ![Good first issue](https://img.shields.io/badge/-Good%20first%20issue-4E2A84?style=flat-square) Good for newcomers. These issues calls for a
  **fairly** easy enhancement, or for a change that helps/requires
  getting to know the code better. They have educational value, and
  for this reason, unless urgent, experts in the topic should refrain
  from closing them - but help newcomers closing them.

- ![Hacktoberfest](https://img.shields.io/badge/-Hacktoberfest-FF7518?style=flat-square) Dedicated to the hacktoberfest event, so that people
  can help and feel good about it (and show it with a T-shirt!).
  **Such commits will not be recognised in the all-contributor table,
  unless otherwise specified**.

- ![Help wanted](https://img.shields.io/badge/-Help%20wanted-57DB1A?style=flat-square) Extra attention is needed here! It's a good place to have a look!

- ![Refactoring](https://img.shields.io/badge/-Refactoring-9494FF?style=flat-square) Improve nonfunctional attributes. Which means rewriting
  the code or the documentation to improve performance or just because
  there's a better way to express those lines. It might create a
  `majormod` PR.

- ![Question](https://img.shields.io/badge/-Question-D876E3?style=flat-square) Further information is requested, from users to
  developers. Try to respond to this!

- ![Wontfix](https://img.shields.io/badge/-Wontfix-ffffff?style=flat-square) This will not be worked on, until further notice.

### PR-only labels

#### Labels for semantic release and changelogs

- ![BugFIX](https://img.shields.io/badge/-BugFIX-D73A4A?style=flat-square) These PRs close an issue labelled `Bug`. They also increase
  the semantic versioning for fixes (+0.0.1).

 - ![dependencies](https://img.shields.io/badge/-dependencies-0366D6?style=flat-square) Pull requests that update a dependency file

- ![Documentation](https://img.shields.io/badge/-Documentation-1D70CF?style=flat-square) See above. This PR won\'t trigger a release, but it will be reported in the changelog.

- ![Majormod](https://img.shields.io/badge/-Majormod-05246D?style=flat-square) These PRs call for a new major release (+1.0.0). This
  means that the PR is breaking backward compatibility.

- ![Minormod](https://img.shields.io/badge/-Minormod-05246D?style=flat-square) This PR generally closes an `Enhancement` issue. It increments the minor version (0.+1.0)

- ![Minormod-breaking](https://img.shields.io/badge/-Minormod&ndash;breaking-05246D?style=flat-square) This label should be used during development stages (<1.0.0) only. These PRs call for a new minor release during development (0.+1.0) that **will** break backward compatibility.

- ![Internal](https://img.shields.io/badge/-Internal-ffffff?style=flat-square) This PR contains changes to the internal API. It won\'t
  trigger a release, but it will be reported in the changelog.

- ![Testing](https://img.shields.io/badge/-Testing-FFB5B4?style=flat-square) See above. This PR won\'t trigger a release, but it will be
  reported in the changelog.

- ![Skip release](https://img.shields.io/badge/-Skip%20release-ffffff?style=flat-square) This PR will **not** trigger a release.

- ![Release](https://img.shields.io/badge/-Release-ffffff?style=flat-square) This PR will force the trigger of a release.

#### Other labels

- ![Invalid](https://img.shields.io/badge/-Invalid-960018?style=flat-square): These PRs don't seem right. They actually seem so not
  right that they won't be further processed. This label invalidates a
  Hacktoberfest contribution. If you think this is wrong, start a
  discussion in the relevant issue (or open one if missing). Reviewers
  are asked to give an explanation for the use of this label.

### Good First Issues

Good First Issues are issues that are either very simple, or that help
the contributor get to know the programs or the languages better. We use
it to help contributors with less experience to learn and familiarise
with Git, GitHub, Python3, and graph signal processing. We invite more expert
contributors to avoid those issues, leave them to beginners and possibly
help them out in the resolution of the issue. However, if the issue is
left unassigned or unattended for long, and it's considered important or
urgent, anyone can tackle it.

## Contribution workflow

There are many descriptions of a good contribution workflow out there.
For instance, we suggest to have a look at [tedana's workflow](https://github.com/ME-ICA/tedana/blob/master/CONTRIBUTING.md#making-a-change).
We follow a very similar workflow. The only three
differences are:

- If you see an open issue that you would like to work on, check if it
  is assigned. If it is, ask the assignee if they need help or want to
  be substituted before starting to work on it.
- We ask you to test the code locally before merging it, and then, if
  possible, write some automatic tests for the code to be run in our
  Continuous Integration! Check the testing section below to know
  more.
- We suggest opening a draft PR as soon as you can - so it's easier
  for us to help you!

## Pull Requests

To improve understanding pull requests \"at a glance\" and use the power
of `auto`, we use the labels listed above. Multiple labels can be
assigned to a PR - in fact, all those that you think are relevant. We
strongly advise to keep the changes you\'re introducing with your PR
limited to your original goal. Adding to the scope of your PR little
style corrections or code refactoring here and there in the code that
you\'re already modifying is a great help, but when they become too much
(and they are not relevant to your PR) they risk complicating the nature
of the PR and the reviewing process. It is much better to open another
PR with the objective of doing such corrections! Moreover, if you\'re
tempted to assign more than one label that would trigger a release (e.g.
bug and minormod or bug and majormod, etc.), you might want to split your PR
instead. When opening a pull request, assign it at least one label.

We encourage you to open a PR as soon as possible - even before you
finish working on them. This is useful especially to you - so that you
can receive comments and suggestions early on, rather than having to
process a lot of comments in the final review step! However, if it's an
incomplete PR, please open a **Draft PR**. That helps us process PRs by
knowing which one to have a look first - and how picky to be when doing
so.

Reviewing PRs is a time consuming task and it can be stressful for both
the reviewer and the author. Avoiding wasting time and the need of
little fixes - such as fixing grammar mistakes and typos, styling code,
or adopting conventions - is a good start for a successful (and quick)
review. Before graduating a Draft PR to a PR ready for review, please
check that:

- You did all you wanted to include in your PR. If at a later stage
  you realize something is missing and it's not a minor thing, you
  will need to open a new PR.
- If your contribution contains code or tests, you ran and passed all
  of the tests locally with [pytest](#automatic_testing).
- If you're writing documentation, you built it locally with
  sphinx and the format is what you intended.
- Your code is harmonious with the rest of the code - no repetitions
  of any sort!

Your code respects the [adopted Style](#style_guide), especially if:

- Your code is lintered adequately and respects the [PEP8](https://www.python.org/dev/peps/pep-0008/) convention.
- Your docstrings follow the [numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) convention.
- There are no typos or grammatical mistakes and the text is fluid.

- The code is sufficiently commented and the comments are clear.

- Your PR title is clear enough to be meaningful when appended to the version changelog.

- You have the correct labels.

### Before merging

To be merged, PRs have to:

1. Pass all the CircleCI tests, and possibly all the codecov checks.
2. Have the necessary amount of approving reviews, even if you're a
   long time contributor.

   Note : You can ask one (or more) contributor to do
   that review, if you think they align more with the content of your
   PR. You need **one** review for documentation, tests, and small
   changes, and **two** reviews for bugs, refactoring and enhancements.
3. Have at least a release-related label (or a `Skip
   release` label).
4. Have a short title that clearly explains in one sentence the aim of
   the PR.
5. Contain at least a unit test for your contribution, if the PR
   contains code (it would be better if it contains an integration or
   function test and all the breaking tests necessary). If you're not
   confident about writing tests, it is possible to refer to an issue
   that asks for the test to be written, or another (Draft) PR that
   contains the tests required.

As we're trying to maintain at least 90% code coverage, you're strongly
encouraged to write all of the tests necessary to keep coverage above
that threshold. If coverage drops too low, you might be asked to add
more tests and/or your PR might be rejected. See the [Automatic testing](#automatic-testing) section.

Don't merge your own pull request! That\'s a task for the main reviewer
of your PR or the project manager. Remember that the project manager
doesn't have to be a reviewer of your PR!

## Reviewing PRs

Reviewing PRs is an extremely important task in collaborative
development. In fact, it is probably the task that requires the most
time in the development, and it can be stressful for both the reviewer
and the author. Remember that, as a PR Reviewer, you are guaranteeing
that the changes work and integrate well with the rest of the
repository, hence **you are responsible for the quality of the
repository and its next version release**. If they don\'t integrate
well, later PR reviewers might have to ask for broader changes than
expected.

There are many best practices to review code online, for
instance [this medium blog post](https://medium.com/an-idea/the-code-review-guide-9e793edcd683), but
here are some good rules of thumbs that we need to follow while
reviewing PRs:

- Be **respectful** to the PR authors and be clear in what you are
  asking/suggesting - remember that, like you, they are contributing
  their spare time and doing their best job!

- If there is a *Draft PR*, you can comment on its development in the
  message board or making "Comment" reviews. Don't ask for changes,
  and especially, **don't approve the PR**

- If the PR graduated *from Draft to full PR*, check that it follows the
  sections [Pull requests](#pull-requests) and [Style Guide](#style-guide) of these
  guidelines. If not, invite the author to do so before starting a
  review.
- **Don't limit your review to the parts that are changed**. Look at
  the entire file, see if the changes fit well in it, and see if the
  changes are properly addressed everywhere in the code - in the
  documentation, in the tests, and in other functions. Sometimes the
  differences reported don't show the full impact of the PR in the
  repository!
- If your want to make Pull Requests an educational process, invite
  the author of the PR to make changes before actually doing them
  yourself. Request changes via comments or in the message board or by
  checking out the PR locally, making changes and then submitting a PR
  to the author's branch.
- If you decide to use the suggestion tool in reviews, or to start a
  PR to the branch under review, please alert the Project Manager.
  Bots might automatically assign you contribution types that will
  have to be removed (remember, your contribution in this case is
  "Reviewer"). Instead of starting a PR to the branch under review,
  think about opening a new PR with those modifications (unless they
  are needed to pass tests), and alert the Main Reviewer. In any case
  **don't commit directly to the branch under review**!
- If you're reviewing documentation, build it locally with [`mkdocs serve`](https://www.mkdocs.org/getting-started/#creating-a-new-project) command.
- If you're asking for changes, **don't approve the PR**. Approve it
  only after everything was sufficiently addressed. Someone else might
  merge the PR in taking your word for granted.
- If you are the main reviewer, and the last reviewer required to
  approve the PR, merge the PR!

Before approving and/or merging PRs, be sure that:

- All the tests in CircleCI pass without errors.
- Prefereably, codecov checks pass as well. If they don\'t, discuss
  what to do.
- The title describes the content of the PR clearly enough to be
  meaningful on its own - remember that it will appear in the version
  changelog!
- The PR has the appropriate labels to trigger the appropriate version
  release and update the contributors table.

## Style Guide

Docstrings should follow
[numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html)
convention. We encourage extensive documentation. The python code itself
should follow [PEP8](https://www.python.org/dev/peps/pep-0008/)
convention whenever possible: there are continuous integration tests
checking that! You can use linters to help you write your code following
style conventions. Linters are add-ons that you can run on the written
script file. We suggest the use of **flake8** for Python 3. Many editors
(Atom, VScode, Sublimetext, \...) support addons for online lintering,
which means you'll see warnings and errors while you write the code -
check out if your does!

Since we adopt [auto](https://intuit.github.io/auto/home.html), the PR
title will be automatically reported as part of the changelog when
updating versions. Try to describe in one (short) sentence what your PR
is about - possibly using the imperative and starting with a capital
letter. For instance, a good PR title could be:
`Implement support for <randomtype> files` or
`Reorder dictionary entries`, rather than `<randomtype> support` or
`reorders keys`.

## Automatic Testing

We use Continuous Integration (CI) to make life easier. In
particular, we use the [CircleCI](https://circleci.com/) platform to run
automatic testing! **Automatic tests** are cold, robotic, emotionless,
and opinionless tests that check that the program is doing what it is
expected to. They are written by the developers and run (by CircleCI)
every time they send a Pull Request to `nigsp`. They
complement the warm, human, emotional and opinionated **user tests**, as
they tell us if a piece of code is failing. CircleCI uses
[pytest](https://docs.pytest.org/en/latest/) to run the tests. The great
thing about it is that you can run it in advance on your local version
of the code! We can measure the amount of code that is tested with
[codecov](https://docs.pytest.org/en/latest/), which is an indication of
how reliable our packages are! We try to maintain a 90% code coverage,
and for this reason, PR should contain tests! The four main type of
tests we use are:

1. **Unit tests**: Unit tests check that a minimal piece of code is doing what it
should be doing. Normally this means calling a function with
some mock parameters and checking that the output is equal to
the expected output. For example, to test a function that adds
two given numbers together (1 and 3), we would call the function
with those parameters, and check that the output is 4.

2. **Breaking tests**: Breaking tests are what you expect - they check that the program
is breaking when it should. This means calling a function with
parameters that are expected **not** to work, and check that it
raises a proper error or warning.

3. **Integration tests**: Integration tests check that the code has an expected output,
being blind to its content. This means that if the program
should output a new file, the file exists - even if it's empty.
This type of tests are normally run on real data and call the
program itself. For instance, documentation PRs should check
that the documentation page is produced!

4. **Functional tests**: If integration tests and unit tests could have babies, those
would be functional tests. In practice, this kind of tests check
that an output is produced, and *also* that it contains what it
should contain. If a function should output a new file or an
object, this test passes only if the file exists *and* it is
like we expect it to be. They are run on real or mock data, and
call the program itself or a function.

## Recognising contributors

We welcome and recognize [all
contributions](https://allcontributors.org/docs/en/specification) from
documentation to testing to code development. You can see a list of
current contributors in the README (kept up to date by the [all
contributors bot](https://allcontributors.org/docs/en/bot/overview)).

**Thank you!**

*--- Based on contributing guidelines from the [STEMMRoleModels](https://github.com/KirstieJane/STEMMRoleModels) project.*
