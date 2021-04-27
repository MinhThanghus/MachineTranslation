from tensor2tensor.data_generators import problem, text_problems
from tensor2tensor.utils import registry
import os


@registry.register_problem
class UniEnVi(text_problems.Text2TextProblem):
    @property
    def is_generate_per_split(self):
        return False

    def generate_samples(self, data_dir, tmp_dir, dataset_split):
        # OpenSubtitles2018
        my_data_dir = '/content/drive/MyDrive/ducnv/NMT/data/OpenSubtitles2018'
        with open(os.path.join(my_data_dir, 'OpenSubtitles.en-vi.en'), encoding='utf8') as file:
            en_lines = file.readlines()

        with open(os.path.join(my_data_dir, 'OpenSubtitles.en-vi.vi'), encoding='utf8') as file:
            vi_lines = file.readlines()

        if len(en_lines) != len(vi_lines):
            raise Exception("OpenSubtitles data ERORR ###################################################")

        for (en, vi) in zip(en_lines, vi_lines):
            yield {
                'inputs': en.strip(),
                'targets': vi.strip()
            }

        # TED2015
        my_data_dir = '/content/drive/MyDrive/ducnv/NMT/data/TED'
        with open(os.path.join(my_data_dir, 'train.en'), encoding='utf8') as file:
            en_lines = file.readlines()

        with open(os.path.join(my_data_dir, 'train.vi'), encoding='utf8') as file:
            vi_lines = file.readlines()

        if len(en_lines) != len(vi_lines):
            raise Exception("TED2015 data ERORR ###################################################")

        for (en, vi) in zip(en_lines, vi_lines):
            yield {
                'inputs': en.strip(),
                'targets': vi.strip()
            }

        # TED2020
        my_data_dir = '/content/drive/MyDrive/ducnv/NMT/data/TED'
        with open(os.path.join(my_data_dir, 'TED2020.en-vi.en'), encoding='utf8') as file:
            en_lines = file.readlines()

        with open(os.path.join(my_data_dir, 'TED2020.en-vi.vi'), encoding='utf8') as file:
            vi_lines = file.readlines()

        if len(en_lines) != len(vi_lines):
            raise Exception("TED2015 data ERORR ###################################################")

        for (en, vi) in zip(en_lines, vi_lines):
            yield {
                'inputs': en.strip(),
                'targets': vi.strip()
            }