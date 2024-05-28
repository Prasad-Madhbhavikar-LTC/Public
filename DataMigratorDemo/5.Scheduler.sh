echo "Starting the Scheduling server"
conda init
conda deactivate
conda activate spark
cd Processing_Folder/Job_dump
inotifywait -m -P -e moved_to -e create --format "%f" --include _destination_details.yaml . | awk -F '_destination_details.yaml' '{ system("python3 ../../python/migration-processor/try.py -j " $1)}'