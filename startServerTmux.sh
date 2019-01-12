SESSION=DRINKLIST-API


tmux has-session -t $SESSION
if [ $? -eq 0 ]; then
    echo "Session $SESSION already exists. Attaching."
    sleep 1
    tmux attach -t $SESSION
    exit 0;
fi

tmux new-session -d -s $SESSION

tmux select-pane -t :.0
tmux send-keys . Space venv/bin/activate Enter
tmux send-keys export Space FLASK_APP=drinklist-api Enter
tmux send-keys export Space FLASK_DEBUG=1 Enter
tmux send-keys export Space FLASK_ENV=debug Enter
tmux send-keys flask Space create_db Enter
tmux send-keys flask Space run Enter

tmux attach -t $SESSION:0

