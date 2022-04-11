import csv

class Annotator:

    def __init__(self, id):

        self.id = id
        self.rowsAnnotated = 0.0
        self.tablesAnnotated = 0
        self.onesMarked = 0.0
        self.zerosMarked = 0.0
        self.nonesMarked = 0.0

        # agreement w.r.t majority
        self.agreement_00 = 0.0
        self.agreement_11 = 0.0
        self.agreement_none_00 = 0.0
        self.agreement_none_11 = 0.0

        # deviance w.r.t majority
        self.deviations_01 = 0.0
        self.deviations_10 = 0.0
        self.devianceNone_01 = 0.0
        self.devianceNone_10 = 0.0

        # pairwise agreement
        self.pairwise_00 = 0.0
        self.pairwise_11 = 0.0
        self.pairwise_none_00 = 0.0
        self.pairwise_none_11 = 0.0

        # pairwise deviance
        self.pairwise_01 = 0.0
        self.pairwise_10 = 0.0
        self.pairwiseNone_01 = 0.0
        self.pairwiseNone_10 = 0.0

    def deviate_01(self, n):

        self.deviations_01 += n

    def deviate_10(self, n):

        self.deviations_10 += n

    def score_majority(self, annotation, annotationNone, gold, goldNone):

        self.tablesAnnotated += 1

        if len(annotation) != len(gold):
            return "ERROR"

        n = len(annotation)

        for i in range(n):

            # number of rows annotated
            self.rowsAnnotated += 1

            bit = annotation[i]
            goldBit = gold[i]

            # no. of 1s and 0s marked
            if bit == '1':
                self.onesMarked += 1
            elif bit == '0':
                self.zerosMarked += 1

            # deviance - 01 and 10
            # annotator marked 0, majority 1
            if (bit == '0') and (goldBit == '1'):
                self.deviate_01(1)
            # annotator marked 1, majority 0
            elif (bit == '1') and (goldBit == '0'):
                self.deviate_10(1)

            # agreement - 01 and 10
            # 00 agreement
            elif (bit == '0') and (goldBit == '0'):
                self.agreement_00 += 1
            elif (bit == '1') and (goldBit == '1'):
                self.agreement_11 += 1

        # do the same for none

        # number of None rows selected
        # add one row for each none
        self.rowsAnnotated += 1

        if annotationNone == '1':
            self.nonesMarked += 1

        # 10 and 01 mistakes in annotation of None row
        if annotationNone == '0' and goldNone == '1':
            self.devianceNone_01 += 1
        elif annotationNone == '1' and goldNone == '0':
            self.devianceNone_10 += 1
        elif annotationNone == '0' and goldNone == '0':
            self.agreement_none_00 += 1
        elif annotationNone == '1' and goldNone == '1':
            self.agreement_none_11 += 1


    def score_majority_normal(self, annotation, annotationNone, gold, goldNone):

        if len(annotation) != len(gold):
            return "ERROR"

        n = len(annotation)
        # add 1 to the normalization factor for the none row
        nf = float(n) + 1.0
        self.tablesAnnotated += 1

        for i in range(n):

            # number of rows annotated
            self.rowsAnnotated += 1

            bit = annotation[i]
            goldBit = gold[i]

            # no. of 1s and 0s marked
            if bit == '1':
                self.onesMarked += 1.0/nf
            elif bit == '0':
                self.zerosMarked += 1.0/nf

            # deviance - 01 and 10
            # annotator marked 0, majority 1
            if (bit == '0') and (goldBit == '1'):
                self.deviate_01(1.0/nf)
            # annotator marked 1, majority 0
            elif (bit == '1') and (goldBit == '0'):
                self.deviate_10(1.0/nf)

            # agreement - 01 and 10
            # 00 agreement
            elif (bit == '0') and (goldBit == '0'):
                self.agreement_00 += 1.0/nf
            elif (bit == '1') and (goldBit == '1'):
                self.agreement_11 += 1.0/nf

        # do the same for none

        # number of None rows selected
        self.rowsAnnotated += 1
        
        if annotationNone == '1':
            self.nonesMarked += 1.0/nf

        # 10 and 01 mistakes in annotation of None row
        if annotationNone == '0' and goldNone == '1':
            self.devianceNone_01 += 1.0/nf
        elif annotationNone == '1' and goldNone == '0':
            self.devianceNone_10 += 1.0/nf
        elif annotationNone == '0' and goldNone == '0':
            self.agreement_none_00 += 1.0/nf
        elif annotationNone == '1' and goldNone == '1':
            self.agreement_none_11 += 1.0/nf


    def score_pairwise(self, annotation, annotationNone, other, otherNone):

        if len(annotation) != len(other):
            return "ERROR"

        n = len(annotation)

        for i in range(n):

            bit = annotation[i]
            otherBit = other[i]

            # deviance - 01 and 10
            # annotator marked 0, other 1
            if (bit == '0') and (otherBit == '1'):
                self.pairwise_01 += 1
            # annotator marked 1, other 0
            elif (bit == '1') and (otherBit == '0'):
                self.pairwise_10 += 1

            # agreement - 01 and 10
            # 00 agreement
            elif (bit == '0') and (otherBit == '0'):
                self.pairwise_00 += 1
            elif (bit == '1') and (otherBit == '1'):
                self.pairwise_11 += 1

        # do the same for none

        # 10 and 01 disagreements in annotation of None row
        if annotationNone == '0' and otherNone == '1':
            self.pairwiseNone_01 += 1
        elif annotationNone == '1' and otherNone == '0':
            self.pairwiseNone_10 += 1
        elif annotationNone == '0' and otherNone == '0':
            self.pairwise_none_00 += 1
        elif annotationNone == '1' and otherNone == '1':
            self.pairwise_none_11 += 1

    def score_pairwise_normal(self, annotation, annotationNone, other, otherNone):

        if len(annotation) != len(other):
            return "ERROR"

        n = len(annotation)
        nf = len(annotation) + 1.0

        for i in range(n):

            bit = annotation[i]
            otherBit = other[i]

            # deviance - 01 and 10
            # annotator marked 0, other 1
            if (bit == '0') and (otherBit == '1'):
                self.pairwise_01 += 1.0/nf
            # annotator marked 1, other 0
            elif (bit == '1') and (otherBit == '0'):
                self.pairwise_10 += 1.0/nf

            # agreement - 01 and 10
            # 00 agreement
            elif (bit == '0') and (otherBit == '0'):
                self.pairwise_00 += 1.0/nf
            elif (bit == '1') and (otherBit == '1'):
                self.pairwise_11 += 1.0/nf

        # do the same for none

        # 10 and 01 disagreements in annotation of None row
        if annotationNone == '0' and otherNone == '1':
            self.pairwiseNone_01 += 1.0/nf
        elif annotationNone == '1' and otherNone == '0':
            self.pairwiseNone_10 += 1.0/nf
        elif annotationNone == '0' and otherNone == '0':
            self.pairwise_none_00 += 1.0/nf
        elif annotationNone == '1' and otherNone == '1':
            self.pairwise_none_11 += 1.0/nf

    def score_pairs(self, annotators, pair):

        allAnnotators = pair.fetchWorkers()
        allLabels = pair.fetchLabels()
        ls = zip(allAnnotators, allLabels)

        # find what self has annotated
        annotation = ""
        annotationNone = ""
        for i, annID in enumerate(allAnnotators):
            if annID == self.id:
                annotation = allLabels[i][:-1]
                annotationNone = allLabels[i][-1]

        # score self for all pairs
        for annID, label in ls:
            annotator = annotators[annID]
            other = label[:-1]
            otherNone = label[-1]

            if annotator.id != self.id:

                self.score_pairwise(annotation, annotationNone, other, otherNone)


    @staticmethod
    def score_all_pairs(annotators, pair):

        pairAnnotators = pair.fetchWorkers()

        for annID in pairAnnotators:

            annotators[annID].score_pairs(annotators, pair)


    def score_pairs_normal(self, annotators, pair):

        allAnnotators = pair.fetchWorkers()
        allLabels = pair.fetchLabels()
        ls = zip(allAnnotators, allLabels)

        # find what self has annotated
        annotation = ""
        annotationNone = ""
        for i, annID in enumerate(allAnnotators):
            if annID == self.id:
                annotation = allLabels[i][:-1]
                annotationNone = allLabels[i][-1]

        # score self for all pairs
        for annID, label in ls:
            annotator = annotators[annID]
            other = label[:-1]
            otherNone = label[-1]

            if annotator.id != self.id:

                self.score_pairwise_normal(annotation, annotationNone, other, otherNone)


    @staticmethod
    def score_all_pairs_normal(annotators, pair):

        pairAnnotators = pair.fetchWorkers()

        for annID in pairAnnotators:

            annotators[annID].score_pairs_normal(annotators, pair)


    def print(self):

        print("%15s %5f %5f %5f %5f %5f %5f %5f %5f" % 
              (self.id, self.rowsAnnotated, self.onesMarked, self.zerosMarked,
               self.deviations_01, self.deviations_10, self.nonesMarked,
               self.devianceNone_01, self.devianceNone_10))

    @staticmethod
    def printList(ls):

        print("==================================================")
        print("%15s %5s %5s %5s %5s %5s %5s %5s %5s" % 
                ("ID", "Rows", "1", "0", "01", "10",
                 "none", "non01", "non10"))

        for i in ls:
            i.print()
        print("==================================================")

    @staticmethod
    def writeCSVMajorityNonNormal(ls, csvname):

        with open(csvname, "w+") as f:

            writer = csv.writer(f)

            writer.writerow(["ID", "Tables", "Rows", "m1", "m0", "none",
                             "d01", "d10", "a00", "a11", "none_01",
                             "none_10", "none_00", "none_11"])

            for row in ls:

                writer.writerow([row.id, row.tablesAnnotated, 
                                 row.rowsAnnotated, row.onesMarked,
                                 row.zerosMarked, row.nonesMarked, 
                                 row.deviations_01, row.deviations_10,
                                 row.agreement_00, row.agreement_11,
                                 row.devianceNone_01, row.devianceNone_10,
                                 row.agreement_none_00, row.agreement_none_11])

    @staticmethod
    def writeCSVPairwiseNonNormal(ls, csvname):

        with open(csvname, "w+") as f:

            writer = csv.writer(f)

            writer.writerow(["ID", "Tables", "Rows", "m1", "m0", "none",
                             "d01", "d10", "a00", "a11", "none_01",
                             "none_10", "none_00", "none_11"])

            for row in ls:

                writer.writerow([row.id, row.tablesAnnotated,
                                 row.rowsAnnotated, row.onesMarked,
                                 row.zerosMarked, row.nonesMarked, 
                                 row.pairwise_01, row.pairwise_10,
                                 row.pairwise_00, row.pairwise_11,
                                 row.pairwiseNone_01, row.pairwiseNone_10,
                                 row.pairwise_none_00, row.pairwise_none_11])

    @staticmethod
    def writeCSVMajorityNormal(ls, csvname):

        with open(csvname, "w+") as f:

            writer = csv.writer(f)

            writer.writerow(["ID", "Tables", "Rows", "m1", "m0", "none",
                             "d01", "d10", "a00", "a11", "none_01",
                             "none_10", "none_00", "none_11"])

            for row in ls:
                r = row.rowsAnnotated
                writer.writerow([row.id, row.tablesAnnotated, 
                                 row.rowsAnnotated, row.onesMarked,
                                 row.zerosMarked, row.nonesMarked, 
                                 row.deviations_01, row.deviations_10,
                                 row.agreement_00, row.agreement_11,
                                 row.devianceNone_01, row.devianceNone_10,
                                 row.agreement_none_00, row.agreement_none_11])

    @staticmethod
    def writeCSVPairwiseNormal(ls, csvname):

        with open(csvname, "w+") as f:

            writer = csv.writer(f)

            writer.writerow(["ID", "Tables", "Rows", "m1", "m0", "none",
                             "d01", "d10", "a00", "a11", "none_01",
                             "none_10", "none_00", "none_11"])

            for row in ls:
                r = row.rowsAnnotated
                writer.writerow([row.id, row.tablesAnnotated, 
                                 row.rowsAnnotated, row.onesMarked,
                                 row.zerosMarked, row.nonesMarked, 
                                 row.pairwise_01, row.pairwise_10,
                                 row.pairwise_00, row.pairwise_11,
                                 row.pairwiseNone_01, row.pairwiseNone_10,
                                 row.pairwise_none_00, row.pairwise_none_11])
