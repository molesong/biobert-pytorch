DATA="euadr"

for SPLIT in {1..10}
do
  ENTITY=$DATA-$SPLIT

  echo "***** " $DATA " test score " $SPLIT " *****"
  python scripts/re_eval.py \
    --output_path=./output/$ENTITY/test_results.txt \
    --answer_path=../datasets/RE/$DATA/$SPLIT/test_original.tsv
done


#run only one.
DATA="GAD"
SPLIT="1"
ENTITY=$DATA-$SPLIT
RE_data_dir="/home/data/t200404/bioinfo/P_subject/NLP/biobert/datasets/for_train/datasets_from_download/RE"
python scripts/re_eval.py \
  --output_path=./output/$ENTITY/test_results.txt \
  --answer_path=$RE_data_dir/$DATA/$SPLIT/test_original.tsv