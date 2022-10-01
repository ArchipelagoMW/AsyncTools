
set /p num_games="Enter number of games to generate: "
set /p num_players="Enter number of worlds to generate: "

for /L %%i in (1, 1, %num_games%) do (
    start ArchipelagoGenerate.exe --spoiler 0 --multi %num_players%
)