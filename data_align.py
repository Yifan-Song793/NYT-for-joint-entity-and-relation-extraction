import json
import os
import re


def remove_french_letters(sent):
    sub_pair = {'é': 'e', 'à': 'a', 'è': 'e', 'ù': 'u', 'ê': 'e', 'ú': 'u', 'ó': 'o',
                'á': 'a', 'ü': 'u', 'í': 'i', 'ô': 'o', 'ö': 'o', 'ñ': 'n'}
    for k in sub_pair:
        if re.findall(k, sent):
            sent = re.sub(k, sub_pair[k], sent)
    return sent

class DataAlign():
    def __init__(self, path):
        self.path = path
        self.raw_train_sent2triplet = {}
        self.words2id = None
        self.relations2id = None
        self.id2words = {}
        self.id2relations = {}
        self.load_data()

    def load_data(self):
        with open(os.path.join(self.path, 'raw_train.json'), 'r') as fr:
            lines = fr.readlines()

        tmp_dict = {}
        for line in lines:
            tmp = eval(line)
            sent_no_blank = tmp['sentText'].replace(' ', '')
            if sent_no_blank not in tmp_dict:
                tmp_dict[sent_no_blank] = tmp['relationMentions']
            else:
                tmp_dict[sent_no_blank].extend(tmp['relationMentions'])

        for key in tmp_dict:
            triplets = []
            for triplet in tmp_dict[key]:
                for k in triplet:
                    triplet[k] = remove_french_letters(triplet[k])
                if triplet['label'] != 'None':
                    triplets.append(triplet)
            triplets = [dict(t) for t in set([tuple(d.items()) for d in triplets])]
            self.raw_train_sent2triplet[key] = triplets

        with open(os.path.join(self.path, 'words2id.json'), 'r') as fr:
            self.words2id = json.load(fr)

        with open(os.path.join(self.path, 'relations2id.json'), 'r') as fr:
            self.relations2id = json.load(fr)

        for k in self.words2id:
            self.id2words[self.words2id[k]] = k

        for k in self.relations2id:
            self.id2relations[self.relations2id[k]] = k

    def get_raw(self, name='train'):
        raw = []
        with open(os.path.join(self.path, '{}.json'.format(name)), 'r') as fr:
            data = json.load(fr)
        for sent, triplets in zip(data[1], data[2]):
            raw_sent = [self.id2words[k] for k in sent]
            raw_triplet = []
            for i, item in enumerate(triplets):
                if i % 3 == 2:
                    raw_triplet.append(self.id2relations[item])
                else:
                    raw_triplet.append(item)
            raw.append({"sent": raw_sent, "triplet": raw_triplet})

        return raw

    def statistic(self, data):
        overlap_cnt = 0
        for item in data:
            tmp = ''.join(item['sent'])
            tmp = tmp.replace(' ', '')
            if tmp in self.raw_train_sent2triplet:
                overlap_cnt += 1

        return overlap_cnt, len(data)

    def align(self, data):
        aligned = []
        for item in data:
            res = {'sent': item['sent'], 'rels': []}
            tmp = ''.join(item['sent'])
            tmp = tmp.replace(' ', '')
            raw_triplets = self.raw_train_sent2triplet[tmp]
            for i in range(len(item['triplet']) // 3):
                res['rels'].append(self.find_triplet(item['sent'], raw_triplets,
                                                      (item['triplet'][3 * i], item['triplet'][3 * i + 1], item['triplet'][3 * i + 2])))
            aligned.append(res)

        return aligned

    def find_triplet(self, sent, raws, triplet):
        for raw in raws:
            if re.findall(sent[triplet[0]] + '$', raw['em1Text']) and \
                re.findall(sent[triplet[1]] + '$', raw['em2Text']) and \
                triplet[2] == raw['label']:
                return {'e1s': triplet[0] - len(raw['em1Text'].split(' ')) + 1, 'e1e': triplet[0],
                        'e2s': triplet[1] - len(raw['em2Text'].split(' ')) + 1, 'e2e': triplet[1],
                        'r': self.relations2id[triplet[2]]}
        raise Exception('A sentence cannot be aligned!')


if __name__ == '__main__':
    names = ['train', 'valid', 'test']
    path = './nyt/'
    data_align = DataAlign(path)


    for name in names:
        raw = data_align.get_raw(name)
        overlap_cnt, total_cnt = data_align.statistic(raw)
        aligned = data_align.align(raw)
        with open(os.path.join(path, '{}_aligned.json'.format(name)), 'w') as fw:
            json.dump(aligned, fw)


    print('\nDatasets have been aligned.')
