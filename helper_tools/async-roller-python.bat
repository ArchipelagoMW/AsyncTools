set /p venv="directory of your python environment: "
call %venv%\scripts\activate

set /p num_games="Enter number of games to generate: "
set /p num_players="Enter number of worlds to generate: "

for /L %%i in (1, 1, %num_games%) do (
    start py -O Generate.py --spoiler 0 --multi %num_players% --yaml_output %num_players%
)
