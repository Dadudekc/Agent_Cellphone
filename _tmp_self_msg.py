import sys
sys.path.insert(0, '.')
from src.agent_cell_phone import AgentCellPhone, MsgTag
acp = AgentCellPhone('Agent-2', layout_mode='2-agent', test=True)
acp.send('Agent-2', 'Self-calibration check: hello from Agent-2', MsgTag.REPLY)
print('OK: self-message invoked in test mode')
