#!/bin/sh

dg_path=$(dirname $(realpath "$0"))

DG_ai_1="Geni"
DG_ai_1_desc="is a programmer who wants to implement $DG_ai_2's designs. If any of $DG_ai_2's requests are unclear, $DG_ai_1 will ask for details; otherwise, $DG_ai_1 will use python and pygame, sharing source code for $DG_ai_2 to examine in the chat"
DG_ai_2="Desi"
DG_ai_2_desc="is a brilliant designer who wants to create a game with code by $DG_ai_1. The game will use no external assets, so that it can be fully designed and tested during the chat. It will have a modern and original design, within reasonable limits. $DG_ai_2 will be clear and concise with feature requests and when answering any follow-up questions",

PYTHONPATH="$dg_path/.." \
  $dg_path/../bin/sply_double_chat.py \
    c1_backend="llama-server" \
    c1_model_id="" \
    c1_hostname="localhost" \
    c1_port=8080 \
    c1_user_name="$DG_ai_2" \
    c1_user_desc="$DG_ai_2_desc" \
    c1_ai_name="$DG_ai_1" \
    c1_ai_desc="$DG_ai_1_desc" \
    c1_in_suffix="$DG_ai_1:" \
    c1_in_suffix_enabled="False" \
    c1_rev_prompt="$DG_ai_2:" \
    c1_temp=0.6 \
    c1_num_ctx=16384 \
    c2_backend="llama-server" \
    c2_model_id="" \
    c2_hostname="localhost" \
    c2_port=8081 \
    c2_user_name="$DG_ai_1" \
    c2_user_desc="$DG_ai_1_desc" \
    c2_ai_name="$DG_ai_2" \
    c2_ai_desc="$DG_ai_2_desc" \
    c2_in_suffix="$DG_ai_2:" \
    c2_in_suffix_enabled="False" \
    c2_rev_prompt="$DG_ai_1:" \
    c2_temp=0.9 \
    c2_num_ctx=16384 \
    "$@"

