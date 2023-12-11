import Loader
import webbrowser

# Загрузка данных в отдельном потоке
Loader.load_all_data()


import Dash_board
print('Если браузер не открылся, то откройте самостоятельно ссылку: http://127.0.0.1:8050/')
webbrowser.open('http://127.0.0.1:8050/')
Dash_board.app.run_server(debug=True)

input("Нажмите Enter для выхода...")
