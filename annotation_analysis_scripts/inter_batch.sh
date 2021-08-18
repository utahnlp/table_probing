#!/bin/bash

python3 src/inter_batch_disagreement.py \
        results/tableQA_relevant_rows_expert_annotations.csv \
        results/tableQA_relevant_rows_pilot_annotations.csv \
        results/expert_pilot_disagreement.csv
