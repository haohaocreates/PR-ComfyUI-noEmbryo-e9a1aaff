import io
import json
# from os import walk
from os.path import realpath, join
from pprint import pprint

MANIFEST = {"name": "noEmbryo Nodes",
            "version": (0,0,1),
            "author": "noEmbryo",
            "project": "https://github.com/noembryo",
            "description": "Nodes for ComfyUI",
}

LISTS_PATH = realpath("./custom_nodes/ComfyUI-noEmbryo/TermLists/")


class PromptTermList:
    idx = 0
    data = {"None": ""}
    data_labels = []
    has_error = False
    input_error = ("Trying to store invalid input!\nUse the format:\n"
                   "label=... ...\nvalue=.... .... ...")

    def __init__(self):
        super(PromptTermList, self).__init__()
        self.name = type(self).__name__

    @classmethod
    def load_data_from_json(cls, json_file_path):
        """ Loads a json file from a path

        :type json_file_path: str
        :param json_file_path: The path to the json file
        """
        try:
            with io.open(json_file_path, mode="r", encoding="utf-8") as f:
                # global data
                cls.data = json.load(f)
                cls.data_labels = list(cls.data.items())
        except FileNotFoundError:
            pass

    # noinspection PyMethodParameters
    @classmethod
    def INPUT_TYPES(cls):
        list_path = join(LISTS_PATH, "TermList{}.json".format(cls.idx))
        cls.load_data_from_json(list_path)
        term_list = [i[0] for i in cls.data_labels]
        return {"required": {"text": ("STRING", {"forceInput": True}),
                             "term_list": (term_list,),
                             },
                "optional":
                    {"store_input": ("BOOLEAN", {"default": False,
                                                 "label_on": True,
                                                 "label_off": False},),
                     },
                }

    def save_data_from_input(self, text):
        """ Extracts the json values from the input text and stores them in the json file

        :type text: str
        :param text: The text input
        """
        # global data
        lines = text.splitlines()
        if not len(lines) > 1:
            self.has_error = True
            print(f"{self.name}:", self.input_error)
            return
        if not all((lines[0].startswith("label="), lines[1].startswith("value="))):
            self.has_error = True
            print(f"{self.name}:", self.input_error)
            return
        label = lines[0][6:]
        value = lines[1][6:]
        if not value:
            del self.data[label]
        else:
            self.data[label] = value
            if label in self.data:
                print(f'{self.name}: The label "{label}" is updated!')
            else:
                print(f'{self.name}: The label "{label}" is saved!')
        with io.open(join(LISTS_PATH, "TermList{}.json".format(self.idx)),
                     mode="w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Term",)
    # OUTPUT_NODE = True
    CATEGORY = "conditioning/Term Nodes"
    FUNCTION = "run"

    def run(self, text, term_list, store_input):
        selected = term_list[:len(term_list)]
        text_out = ""
        for i in self.data_labels:
            if i[0] == selected:
                text_out = i[1]
                break
        if text:
            if store_input:
                self.save_data_from_input(text)
                if not self.has_error:
                    text_out = ""
                else:
                    self.has_error = False
                    text_out = self.input_error
            else:
                if text_out:
                    text_out = f"{text_out}, {text}"
                else:
                    text_out = text
        return (text_out,)


class PromptTermList1(PromptTermList):
    idx = 1


class PromptTermList2(PromptTermList):
    idx = 2


class PromptTermList3(PromptTermList):
    idx = 3


class PromptTermList4(PromptTermList):
    idx = 4


class PromptTermList5(PromptTermList):
    idx = 5


class PromptTermList6(PromptTermList):
    idx = 6


NODE_CLASS_MAPPINGS = {"PromptTermList1": PromptTermList1,
                       "PromptTermList2": PromptTermList2,
                       "PromptTermList3": PromptTermList3,
                       "PromptTermList4": PromptTermList4,
                       "PromptTermList5": PromptTermList5,
                       "PromptTermList6": PromptTermList6
                       }

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {"PromptTermList1": "PromptTermList 1",
                              "PromptTermList2": "PromptTermList 2",
                              "PromptTermList3": "PromptTermList 3",
                              "PromptTermList4": "PromptTermList 4",
                              "PromptTermList5": "PromptTermList 5",
                              "PromptTermList6": "PromptTermList 6"
                              }