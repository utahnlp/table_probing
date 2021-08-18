class AnnList:

    def __init__(self):

        self.anns = []


    def add(self, ann):

        ann_exists = [x for x in self.anns if x.id == ann.id]

        if ann_exists == []:
            self.anns.append(ann)

    def add_a_bunch(self, ann_list):

        for ann in ann_list:
            self.add(ann)

    def print(self):

        print("".join(["+" for i in range(70)]))
        for ann in self.anns:
            print("%20s %5d" % (ann.id, ann.score))

    def disagreed(self, id):

        for ann in self.anns:
            if ann.id == id:
                ann.disagreed()

    def adjust_scores(self, annotator, n):
        
        for ann in self.anns:
            if ann.id == annotator.id:
                ann.disagreed(n)


class Annotator:

    def __init__(self, id):

        self.id = id
        self.score = 0

    def disagreed(self, n):
        self.score += n