import copy
import logging

from jinja2 import Environment, StrictUndefined

from pr_agent.algo.ai_handler import AiHandler
from pr_agent.algo.pr_processing import get_pr_diff
from pr_agent.algo.token_handler import TokenHandler
from pr_agent.config_loader import settings
from pr_agent.git_providers import get_git_provider
from pr_agent.git_providers.git_provider import get_main_pr_language


class PRQuestions:
    def __init__(self, pr_url: str, args=None):
        question_str = self.parse_args(args)
        self.git_provider = get_git_provider()(pr_url)
        self.main_pr_language = get_main_pr_language(
            self.git_provider.get_languages(), self.git_provider.get_files()
        )
        self.ai_handler = AiHandler()
        self.question_str = question_str
        self.vars = {
            "title": self.git_provider.pr.title,
            "branch": self.git_provider.get_pr_branch(),
            "description": self.git_provider.get_pr_description(),
            "language": self.main_pr_language,
            "diff": "",  # empty diff for initial calculation
            "questions": self.question_str,
        }
        self.token_handler = TokenHandler(self.git_provider.pr,
                                          self.vars,
                                          settings.pr_questions_prompt.system,
                                          settings.pr_questions_prompt.user)
        self.patches_diff = None
        self.prediction = None

    def parse_args(self, args):
        if args and len(args) > 0:
            question_str = " ".join(args)
        else:
            question_str = ""
        return question_str

    async def answer(self):
        logging.info('Answering a PR question...')
        if settings.config.publish_output:
            self.git_provider.publish_comment("Preparing answer...", is_temporary=True)
        logging.info('Getting PR diff...')
        self.patches_diff = get_pr_diff(self.git_provider, self.token_handler)
        logging.info('Getting AI prediction...')
        self.prediction = await self._get_prediction()
        logging.info('Preparing answer...')
        pr_comment = self._prepare_pr_answer()
        if settings.config.publish_output:
            logging.info('Pushing answer...')
            self.git_provider.publish_comment(pr_comment)
            self.git_provider.remove_initial_comment()
        return ""

    async def _get_prediction(self):
        variables = copy.deepcopy(self.vars)
        variables["diff"] = self.patches_diff  # update diff
        environment = Environment(undefined=StrictUndefined)
        system_prompt = environment.from_string(settings.pr_questions_prompt.system).render(variables)
        user_prompt = environment.from_string(settings.pr_questions_prompt.user).render(variables)
        if settings.config.verbosity_level >= 2:
            logging.info(f"\nSystem prompt:\n{system_prompt}")
            logging.info(f"\nUser prompt:\n{user_prompt}")
        model = settings.config.model
        response, finish_reason = await self.ai_handler.chat_completion(model=model, temperature=0.2,
                                                                        system=system_prompt, user=user_prompt)
        return response

    def _prepare_pr_answer(self) -> str:
        answer_str = f"Question: {self.question_str}\n\n"
        answer_str += f"Answer:\n{self.prediction.strip()}\n\n"
        if settings.config.verbosity_level >= 2:
            logging.info(f"answer_str:\n{answer_str}")
        return answer_str
