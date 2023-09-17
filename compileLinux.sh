pyinstaller --name ChessClient --onefile --noconsole --distpath ./bin ./client/client.py
rm -rf ./build
rm ./main.spec
rm ./GCom.spec
