import os
import json
from typing import Any, List, Dict, Optional
from abc import ABC


class TemplateCatalogue(ABC):
    def __init__(self, default_path: str, custom_path: Optional[str]):
        self.catalogue: Dict = dict()
        self.supported_templates: Dict = TemplateCatalogue.get_supported_templates(
            default_path, custom_path
        )

    @staticmethod
    def get_supported_templates(
        default_path: str, custom_path: Optional[str]
    ) -> Dict[str, str]:
        default_templates = TemplateCatalogue.get_templates(default_path)
        # print(f"custom path = {custom_path}")
        if custom_path is None:
            return default_templates
        else:
            custom_templates = TemplateCatalogue.get_templates(custom_path)
            return {**default_templates, **custom_templates}

    @staticmethod
    def get_templates(path: str) -> Dict[str, str]:
        templates = {
            os.path.splitext(f)[0].lower(): path
            for f in os.listdir(path)
            if f.endswith(".json")
        }
        # print(f"loaded templates [{templates}] for path {path}")
        return templates

    def find_template(self, node_name: str) -> Optional[Dict[str, Any]]:
        node_key = node_name.lower()
        node_template = self.catalogue.get(node_key)
        if node_template is not None:
            return node_template
        elif node_key in {*self.supported_templates}:
            path = self.supported_templates[node_key]
            template_file = f"{path}/{node_name}.json"
            with open(template_file) as template:
                self.catalogue[node_key] = json.load(template)
            return self.catalogue[node_key]
        else:
            return None

    @staticmethod
    def merge_settings(
        template: Dict[str, Any], settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        dct = template.copy()
        for k, v in settings.items():
            if isinstance(dct.get(k), dict):
                dct[k] = TemplateCatalogue.merge_settings(dct[k], v)
            elif isinstance(dct.get(k), list):
                dct[k] = TemplateCatalogue.merge_lists(dct[k], v)
            else:
                dct[k] = v
        return dct

    @staticmethod
    def merge_lists(template_list: List, settings_list: List) -> List:
        result_list = template_list.copy()
        for sd in settings_list:
            template_dct = next(
                (td for td in template_list if set(sd.keys()).issubset(set(td.keys()))),
                None,
            )
            if template_dct is None:
                result_list.append(sd)
            else:
                idx = result_list.index(template_dct)
                result_list[idx] = TemplateCatalogue.merge_settings(template_dct, sd)
        return result_list
