pyinstaller --name ChessClient --add-data "client\images;client\images" --onefile --distpath ./bin client\client.py
Remove-Item -Path "./build" -Recurse -Force
Remove-Item "ChessClient.spec"
