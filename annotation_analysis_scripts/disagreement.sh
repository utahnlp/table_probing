#!/bin/bash

python3 src/individual_disagreement.py \
        results/tableQA_relevant_rows_pilot_annotations.csv \
        results/tableQA_relevant_rows_expert_annotations.csv \
        results/disagreement_visual_pilot_expert.html