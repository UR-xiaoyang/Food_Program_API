import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--add-data=e:\\project\\食程计划\\Food_Program_API\\初始化.py;.',
    '--add-data=e:\\project\\食程计划\\Food_Program_API\\用户;用户',
    '--add-data=e:\\project\\食程计划\\Food_Program_API\\计划;计划',
    '--hidden-import=uvicorn.loops.auto',
    '--hidden-import=uvicorn.protocols.http.auto',
    '--hidden-import=uvicorn.protocols.websockets.auto',
    '--name=FoodProgramAPI'
])