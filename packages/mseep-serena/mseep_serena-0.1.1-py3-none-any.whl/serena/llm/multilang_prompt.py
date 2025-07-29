import os
from collections.abc import Callable
from enum import Enum
from typing import Any, Generic, TypeVar

import yaml
from sensai.util.string import ToStringMixin

from .jinja_template import JinjaTemplate

LANG_CODES = ["en", "de"]


class PromptTemplate(ToStringMixin):
    def __init__(self, name: str, jinja_template_string: str) -> None:
        self.name = name
        self.jinja_template = JinjaTemplate(jinja_template_string.strip())
        self.parameters = self.jinja_template.get_parameters()

    def _tostring_excludes(self) -> list[str]:
        return ["jinja_template"]

    def instantiate(self, **kwargs: Any) -> str:
        return self.jinja_template.render(**kwargs)


class PromptList:
    def __init__(self, items: list[str]) -> None:
        self.items = [x.strip() for x in items]

    def to_string(self) -> str:
        bullet = " * "
        indent = " " * len(bullet)
        items = [x.replace("\n", "\n" + indent) for x in self.items]
        return "\n * ".join(items)


T = TypeVar("T")


class MultiLangContainer(Generic[T], ToStringMixin):
    """
    Represents a container of items which are associated with different languages
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.lang2item: dict[str, T] = {}

    def _tostring_excludes(self) -> list[str]:
        return ["lang2item"]

    def _tostring_additional_entries(self) -> dict[str, Any]:
        return dict(languages=list(self.lang2item.keys()))

    class FallbackMode(Enum):
        ANY = "any"
        """
        If the requested language is not found, return the item for any language
        """
        EXCEPTION = "exception"
        """
        If the requested language is not found, raise an exception
        """

    def add_item(self, item: T, lang: str = "") -> None:
        self.lang2item[lang] = item

    def get_item(self, lang: str, fallback_mode: FallbackMode = FallbackMode.EXCEPTION) -> T:
        """
        Gets the item for the given language.

        :param lang: the language shortcode for which to obtain the prompt template
        :param fallback_mode: defines what to do if there is no item for the given language
        :return: the item
        """
        item = self.lang2item.get(lang)
        if item is not None:
            return item
        else:
            if fallback_mode == self.FallbackMode.EXCEPTION:
                raise KeyError(f"Item for language '{lang}' not found for name '{self.name}'")
            if fallback_mode == self.FallbackMode.ANY:
                return next(iter(self.lang2item.values()))
            else:
                raise ValueError(f"Invalid fallback mode '{fallback_mode}'")


class MultiLangPromptTemplate(MultiLangContainer[PromptTemplate]):
    """
    Represents a prompt template which potentially supports multiple languages.
    """

    def get_parameters(self) -> list[str]:
        """
        Gets the parameters of the prompt template (which must be the same for all languages).

        :return: the list of parameters required to instantiate the template
        """
        prev_params = None
        for template in self.lang2item.values():
            params = set(template.parameters)
            if prev_params is not None:
                assert (
                    params == prev_params
                ), f"Parameters of MLPT '{self.name}' are inconsistent: {sorted(params)} vs {sorted(prev_params)}"
            prev_params = params
        assert prev_params is not None
        return sorted(prev_params)


class MultiLangPromptList(MultiLangContainer[PromptList]):
    pass


class MultiLangPromptTemplateCollection:
    """
    Represents a collection of multi-language prompts, which are read from the prompts/ directory.
    The language of a prompt is determined by suffix in the prompt name, e.g. "_de" for German.
    For yaml files, the language can also be set globally for all prompts within it.

    The prompts/ folder may contain:
        - .txt files with a single prompt template (filename defines prompt name, content is the prompt template)
        - .yml files with multiple prompt templates under the top-level key 'prompts'.
          Each key under 'prompts' defines a prompt name and the corresponding value is the prompt template.
          The value can also be a list of prompts instead of a single template.
          The language of all can be set by specifying the key 'lang' in addition to 'prompts'.
    """

    def __init__(self) -> None:
        self.prompt_templates: dict[str, MultiLangPromptTemplate] = {}
        self.prompt_lists: dict[str, MultiLangPromptList] = {}
        prompts_dir = self._prompt_template_folder()
        self._read_prompt_templates(prompts_dir)

    @classmethod
    def _prompt_template_folder(cls) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        prompts_dir = None
        for i in range(5):
            dir_path = os.path.join(dir_path, "..")
            prompts_dir = os.path.join(dir_path, "prompts")
            if os.path.isdir(prompts_dir):
                break
        if prompts_dir is None or not os.path.isdir(prompts_dir):
            raise FileNotFoundError("Could not find the 'prompts' directory")
        return prompts_dir

    @staticmethod
    def _container_lang(prompt_name: str, collection: dict[str, T], container_factory: Callable[[str], T]) -> tuple[T, str]:
        lang = ""
        if prompt_name[-2:] in LANG_CODES and prompt_name[-3] == "_":
            lang = prompt_name[-2:]
            prompt_name = prompt_name[:-3]

        container = collection.get(prompt_name)
        if container is None:
            container = container_factory(prompt_name)
            collection[prompt_name] = container

        return container, lang

    def _add_prompt_template(self, prompt_name: str, jinja_prompt_template: str) -> None:
        """
        :param prompt_name: a prompt name, which may have a language shortcode suffix (e.g. "_de")
        :param jinja_prompt_template: the actual prompt string which may contain placeholders/parameters (e.g. "{name}")
        """
        multilang_prompt_template, lang = self._container_lang(prompt_name, self.prompt_templates, MultiLangPromptTemplate)
        multilang_prompt_template.add_item(PromptTemplate(prompt_name, jinja_prompt_template), lang=lang)

    def _add_prompt_list(self, prompt_name: str, prompt_list: list[str]) -> None:
        """
        :param prompt_name: a prompt name, which may have a language shortcode suffix (e.g. "_de")
        :param prompt_list: a list of prompts
        """
        multilang_prompt_list, lang = self._container_lang(prompt_name, self.prompt_lists, MultiLangPromptList)
        multilang_prompt_list.add_item(PromptList(prompt_list), lang=lang)

    def _read_prompt_templates(self, prompts_dir: str) -> None:
        for fn in os.listdir(prompts_dir):
            path = os.path.join(prompts_dir, fn)
            if fn.endswith(".txt"):
                with open(path, encoding="utf-8") as file:
                    prompt_template_string = file.read()
                self._add_prompt_template(fn[:-4], prompt_template_string)
            elif fn.endswith(".yml"):
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    assert "prompts" in data, f"YAML file {fn} must contain key 'prompts'"
                    lang_suffix = ("_" + data["lang"]) if "lang" in data else ""
                    for prompt_name, prompt in data["prompts"].items():
                        prompt_name += lang_suffix
                        if isinstance(prompt, list):
                            self._add_prompt_list(prompt_name, prompt)
                        elif isinstance(prompt, str):
                            self._add_prompt_template(prompt_name, prompt)
                        else:
                            raise ValueError(f"Invalid prompt type: {prompt}")

    def get_multilang_prompt_template(self, prompt_name: str) -> MultiLangPromptTemplate:
        return self.prompt_templates[prompt_name]

    def get_multilang_prompt_list(self, prompt_name: str) -> MultiLangPromptList:
        return self.prompt_lists[prompt_name]
