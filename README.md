<div align="center">

<div align="center">

<img src="./pics/logo-dark.png#gh-dark-mode-only" width="330"/>
<img src="./pics/logo-light.png#gh-light-mode-only" width="330"/><br/>
Making pull requests less painful with an AI agent
</div>

[![GitHub license](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/Codium-ai/pr-agent/blob/main/LICENSE)
[![Discord](https://badgen.net/badge/icon/discord?icon=discord&label&color=purple)](https://discord.com/channels/1057273017547378788/1126104260430528613)
    <a href="https://github.com/Codium-ai/pr-agent/commits/main">
    <img alt="GitHub" src="https://img.shields.io/github/last-commit/Codium-ai/pr-agent/main?style=for-the-badge" height="20">
    </a>
</div>
<div style="text-align:left;">

CodiumAI `PR-Agent` is an open-source tool aiming to help developers review pull requests faster and more efficiently. It automatically analyzes the pull request and can provide several types of feedback:

**Auto-Description**: Automatically generating PR description - title, type, summary, code walkthrough and PR labels.
\
**PR Review**: Adjustable feedback about the PR main theme, type, relevant tests, security issues, focus, score, and various suggestions for the PR content.
\
**Question Answering**: Answering free-text questions about the PR.
\
**Code Suggestion**: Committable code suggestions for improving the PR.

<h3>Example results:</h2>
</div>
<h4>/describe:</h4>
<div align="center">
<p float="center">
<img src="https://codium.ai/images/describe.gif" width="800">
</p>
</div>
<h4>/review:</h4>
<div align="center">
<p float="center">
<img src="https://codium.ai/images/review.gif" width="800">
</p>
</div>
<h4>/ask:</h4>
<div align="center">
<p float="center">
<img src="https://codium.ai/images/ask.gif" width="800">
</p>
</div>
<h4>/improve:</h4>
<div align="center">
<p float="center">
<img src="https://codium.ai/images/improve.gif" width="800">
</p>
</div>
<div align="left">


- [Overview](#overview)
- [Try it now](#try-it-now)
- [Installation](#installation)
- [Usage and tools](#usage-and-tools)
- [Configuration](./CONFIGURATION.md)
- [How it works](#how-it-works)
- [Roadmap](#roadmap)
- [Similar projects](#similar-projects)
</div>


## Overview
`PR-Agent` offers extensive pull request functionalities across various git providers:
|       |                                             | GitHub | Gitlab | Bitbucket |
|-------|---------------------------------------------|:------:|:------:|:---------:|
| TOOLS | Review                                      |   :white_check_mark:    |   :white_check_mark:    |   :white_check_mark:       |
|       | ⮑ Inline review                             |   :white_check_mark:    |   :white_check_mark:    |           |
|       | Ask                                         |   :white_check_mark:    |   :white_check_mark:    |           |
|       | Auto-Description                            |   :white_check_mark:    |  :white_check_mark:      |           |
|       | Improve Code                                |   :white_check_mark:    |   :white_check_mark:    |           |
|       | Reflect and Review                          |   :white_check_mark:    |                         |           |
|       |                                             |        |        |           |
| USAGE | CLI                                         |   :white_check_mark:    |   :white_check_mark:    |   :white_check_mark:       |
|       | Tagging bot                                 |   :white_check_mark:    |   :white_check_mark:    |           |
|       | Actions                                     |   :white_check_mark:    |        |           |
|       |                                             |        |        |           |
| CORE  | PR compression                              |   :white_check_mark:    |   :white_check_mark:    |   :white_check_mark:       |
|       | Repo language prioritization                |   :white_check_mark:    |   :white_check_mark:    |   :white_check_mark:       |
|       | Adaptive and token-aware<br />file patch fitting |   :white_check_mark:    |   :white_check_mark:    |   :white_check_mark:       |
|       | Incremental PR Review |   :white_check_mark:    |      |         |

Examples for invoking the different tools via the CLI:
- **Review**:       python cli.py --pr-url=<pr_url>  review
- **Describe**:     python cli.py --pr-url=<pr_url>  describe
- **Improve**:      python cli.py --pr-url=<pr_url>  improve
- **Ask**:          python cli.py --pr-url=<pr_url>  ask "Write me a poem about this PR"
- **Reflect**:      python cli.py --pr-url=<pr_url>  reflect

"<pr_url>" is the url of the relevant PR (for example: https://github.com/Codium-ai/pr-agent/pull/50).

In the [configuration](./CONFIGURATION.md) file you can select your git provider (GitHub, Gitlab, Bitbucket), and further configure the different tools.

## Try it now

Try GPT-4 powered PR-Agent on your public GitHub repository for free. Just mention `@CodiumAI-Agent` and add the desired command in any PR comment! The agent will generate a response based on your command.

![Review generation process](https://codium.ai/images/demo.gif)

To set up your own PR-Agent, see the [Installation](#installation) section

---

## Installation

To get started with PR-Agent quickly, you first need to acquire two tokens:

1. An OpenAI key from [here](https://platform.openai.com/), with access to GPT-4.
2. A GitHub personal access token (classic) with the repo scope.

There are several ways to use PR-Agent:

- [Method 1: Use Docker image (no installation required)](INSTALL.md#method-1-use-docker-image-no-installation-required)
- [Method 2: Run as a GitHub Action](INSTALL.md#method-2-run-as-a-github-action)
- [Method 3: Run from source](INSTALL.md#method-3-run-from-source)
- [Method 4: Run as a polling server](INSTALL.md#method-4-run-as-a-polling-server)
  - Request reviews by tagging your GitHub user on a PR
- [Method 5: Run as a GitHub App](INSTALL.md#method-5-run-as-a-github-app)
  - Allowing you to automate the review process on your private or public repositories

## Usage and Tools

**PR-Agent** provides five types of interactions ("tools"): `"PR Reviewer"`, `"PR Q&A"`, `"PR Description"`, `"PR Code Sueggestions"` and `"PR Reflect and Review"`.

- The "PR Reviewer" tool automatically analyzes PRs, and provides various types of feedback.
- The "PR Q&A" tool answers free-text questions about the PR.
- The "PR Description" tool automatically sets the PR Title and body.
- The "PR Code Suggestion" tool provide inline code suggestions for the PR that can be applied and committed.
- The "PR Reflect and Review" tool initiates a dialog with the user, asks them to reflect on the PR, and then provides a more focused review.

## How it works

![PR-Agent Tools](https://www.codium.ai/wp-content/uploads/2023/07/codiumai-diagram-v4.jpg)

Check out the [PR Compression strategy](./PR_COMPRESSION.md) page for more details on how we convert a code diff to a manageable LLM prompt

## Roadmap

- [ ] Support open-source models, as a replacement for OpenAI models. (Note - a minimal requirement for each open-source model is to have 8k+ context, and good support for generating JSON as an output)
- [x] Support other Git providers, such as Gitlab and Bitbucket.
- [ ] Develop additional logic for handling large PRs, and compressing git patches
- [ ] Add additional context to the prompt. For example, repo (or relevant files) summarization, with tools such a [ctags](https://github.com/universal-ctags/ctags)
- [ ] Adding more tools. Possible directions:
  - [x] PR description
  - [x] Inline code suggestions
  - [x] Reflect and review
  - [ ] Enforcing CONTRIBUTING.md guidelines
  - [ ] Performance (are there any performance issues)
  - [ ] Documentation (is the PR properly documented)
  - [ ] Rank the PR importance
  - [ ] ...

## Similar Projects

- [CodiumAI - Meaningful tests for busy devs](https://github.com/Codium-ai/codiumai-vscode-release)
- [Aider - GPT powered coding in your terminal](https://github.com/paul-gauthier/aider)
- [openai-pr-reviewer](https://github.com/coderabbitai/openai-pr-reviewer)
- [CodeReview BOT](https://github.com/anc95/ChatGPT-CodeReview)
- [AI-Maintainer](https://github.com/merwanehamadi/AI-Maintainer)
