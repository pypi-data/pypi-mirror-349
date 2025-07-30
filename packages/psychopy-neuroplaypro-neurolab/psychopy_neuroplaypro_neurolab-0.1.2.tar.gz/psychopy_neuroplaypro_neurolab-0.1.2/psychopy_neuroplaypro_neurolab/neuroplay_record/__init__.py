# -*- coding: utf-8 -*-
"""
NeuroplayRecordingComponent
Инициализация и управление записью NeuroPlayPro через WebSocket из PsychoPy Builder
"""

__all__ = ['NeuroplayRecordingComponent']

from pathlib import Path
from psychopy.experiment.components import BaseComponent, Param, getInitVals

WS_OBJ = 'ws_neuro'

class NeuroplayRecordingComponent(BaseComponent):
    categories = ['EEG']
    targets = ['PsychoPy']
    iconFile = Path(__file__).parent / 'neuroplay_record.png'
    tooltip = 'Start/Stop EEG recording via NeuroPlayPro'
    plugin = "psychopy-neuroplaypro-neurolab"

    def __init__(self, exp, parentName, name='neuroplay_rec'):
        super().__init__(
            exp, parentName, name=name,
            startType='time (s)', startVal=0,
            stopType='duration (s)', stopVal=1.0,
            startEstim='', durationEstim='',
            saveStartStop=False
        )

        self.type = 'NeuroplayRecording'
        self.exp.requireImport(importName='websocket')
        self.exp.requireImport(importName='json')

        self.params['wsURL'] = Param("ws://localhost:1336", valType='str', inputType='editable',
                                     hint="WebSocket адрес NeuroPlayPro")

    def writeInitCode(self, buff):
        inits = getInitVals(self.params, 'PsychoPy')
        code = (f'{inits["name"]} = visual.BaseVisualStim(' +
                'win=win, name="{}")\n'.format(inits['name']))
        buff.writeIndentedLines(code)

        ws_url = inits['wsURL'].val
        code = f"{WS_OBJ} = websocket.create_connection(\"{ws_url}\")"
        buff.writeIndentedLines(code)

    def writeRoutineStartCode(self, buff):
        inits = getInitVals(self.params, 'PsychoPy')
        buff.writeIndentedLines("# === Start EEG Recording ===")
        buff.writeIndentedLines("try:")
        buff.setIndentLevel(1, relative=True)

        buff.writeIndentedLines('start_record_cmd = json.dumps({"command": "startRecord"})')
        buff.writeIndentedLines(f"{WS_OBJ}.send(start_record_cmd)")
        buff.writeIndentedLines(f"response = {WS_OBJ}.recv()")
        buff.writeIndentedLines("print(f'Response from NeuroPlay: {response}')")

        buff.setIndentLevel(-1, relative=True)
        buff.writeIndentedLines("except Exception as e:")
        buff.setIndentLevel(1, relative=True)
        buff.writeIndentedLines('print(f"Ошибка при старте записи NeuroPlay: {e}")')
        buff.setIndentLevel(-1, relative=True)

    def writeRoutineEndCode(self, buff):
        buff.writeIndentedLines("# === Stop EEG Recording ===")
        buff.writeIndentedLines('print("Stopping NeuroPlay...")')
        buff.writeIndentedLines("try:")
        buff.setIndentLevel(1, relative=True)
        buff.writeIndentedLines('stop_record_cmd = json.dumps({"command": "stopRecord"})')
        buff.writeIndentedLines(f"{WS_OBJ}.send(stop_record_cmd)")
        buff.writeIndentedLines(f"response = {WS_OBJ}.recv()")
        buff.writeIndentedLines("print(f'Response from NeuroPlay: {response}')")
        buff.setIndentLevel(-1, relative=True)
        buff.writeIndentedLines("except Exception as e:")
        buff.setIndentLevel(1, relative=True)
        buff.writeIndentedLines('print(f"Ошибка при остановке записи NeuroPlay: {e}")')
        buff.setIndentLevel(-1, relative=True)

    def writeExperimentEndCode(self, buff):
        buff.writeIndentedLines("# === Close WebSocket connection ===")
        buff.writeIndentedLines("try:")
        buff.setIndentLevel(1, relative=True)
        buff.writeIndentedLines(f"{WS_OBJ}.close()")
        buff.setIndentLevel(-1, relative=True)
        buff.writeIndentedLines("except Exception as e:")
        buff.setIndentLevel(1, relative=True)
        buff.writeIndentedLines("print(f'Ошибка при закрытии WebSocket: {e}')")
        buff.setIndentLevel(-1, relative=True)

    def writeFrameCode(self, buff):
        pass

    def writeFrameCodeJS(self, buff):
        pass

    def writeExperimentEndCodeJS(self, buff):
        pass

    def writeInitCodeJS(self, buff):
        pass