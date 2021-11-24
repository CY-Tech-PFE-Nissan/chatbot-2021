# How to contribute

## I. Create an Issue

Whenever you want to add a feature to the project, you have to create the associated issue and put it in the `To do` column (in the project board) if it wasn't yet. To add an issue in the project board, click on `+Add cards`, opened issues that are not in the project board will be displayed.

When you are creating a new issue do not forget to associate some labels to it (a priority level at least). It will be clearer for collaborators. Eventually you can also assign the issue to someone.

## II. Update project board

If you are currently working on a particular issue, you should move the issue card into the `In Progress` column. To do so you just have to drag and drop the issue card in the chosen column. Everyone will then see which issues are taken care of.

## III. Create a branch

When you want to add a new feature or work on an existing feature for debugging or whatever, you may create a new working branch (usually `features/featureName`). You can create either on the GitHub platform or locally using the following command:

```sh
git checkout -b features/featureName
```

## IV. Ensure code quality

To ensure the code quality during your development, you should check that you have installed `pre-commit` in your `.git` folder using the command:

```sh
pre-commit install
```

You might need to install first the `pre-commit` package using the command:

```sh
pip install pre-commit
```

## V. Close an Issue

When you have resolve an issue on your branch, you may make a Pull request. You can manually link up to ten issues to it. When you merge a linked pull request into the default branch of a repository, its linked issues are automatically closed.

**Do not close an issue if the associated branch is not merged into the default branch.**
