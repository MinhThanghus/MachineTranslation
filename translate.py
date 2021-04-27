import tensorflow as tf
tfe = tf.contrib.eager
tfe.enable_eager_execution()
Modes = tf.estimator.ModeKeys

from tensor2tensor import problems
from tensor2tensor.utils import trainer_lib
from tensor2tensor.utils import registry
import numpy as np
from nltk import sent_tokenize
from configs import UniEnViConfig


class Translator:
    def __init__(self, config):
        self.translate_problem = problems.problem(config.PROBLEM)
        self.encoder = self.translate_problem.feature_encoders(config.VOCAB_DIR)
        self.hparams = trainer_lib.create_hparams(config.HPARAMS, data_dir=config.VOCAB_DIR, problem_name=config.PROBLEM)
        self.checkpoint_path = config.CHECKPOINT_PATH
        self.translate_model = registry.model(config.MODEL)(self.hparams, Modes.PREDICT)

    def encode(self, input_str):
        input = self.encoder['inputs'].encode(input_str) + [1]  # add EOS id
        batch_inputs = tf.reshape(input, [1, -1, 1])  # (batch_size, seq_length, depth)
        return {'inputs': batch_inputs}

    def decode(self, integers):
        integers = list(np.squeeze(integers))
        if 1 in integers:
            integers = integers[:integers.index(1)]
        return self.encoder['inputs'].decode(np.squeeze(integers))

    def translate_sent(self, input_str):
        encoded_inputs = self.encode(input_str)
        with tfe.restore_variables_on_create(self.checkpoint_path):
            model_output = self.translate_model.infer(encoded_inputs)['outputs']
        return self.decode(model_output)

    def translate_docs(self, docs):
        input_sents = sent_tokenize(docs)
        output_sents = []
        for sent in input_sents:
            output_sents.append(self.translate_sent(sent))
        return ' '.join(output_sents)

