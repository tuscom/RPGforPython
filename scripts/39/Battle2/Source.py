from Helper import BattleHelper
import Helper

from ObjectClass4 import ObjectClass
from FieldCharacter5 import FieldCharacter
from FieldEnemy4 import FieldEnemy
from FieldFamily5 import FieldFamily
from IconCharacter3 import IconCharacter
from PieceAnimation4 import PieceAnimation
from OneCmdAnim3 import OneCmdAnim
from AllAnimationController4 import AllAnimationController
from Button1 import Button

#from OneCommandAnim4 import OneCommandAnim

"""
関数の更新状況 - どこからOverride or 継承されているか。バージョン更新ごとに記述する。
注意すべきは継承元が更新されたとき、ちゃんと継承先も合わせられているかが問題。
================= クラス名 ===============
・関数名：Mainバージョン数

================= Main ==================
・__init__
・Start:4
・Update:4 
・ControllerPanelParameter:4
・GetSource:4
・ProgramParameter:4
・SetPanel:4
・SetBackPanel:4
・SetFamilyIcon:4
・SetAttackBtn:4
・PanelController:4
・AttackBtnOnClick:4
・ObjectSetActive:4
・SelectedSwitch:4

============== FieldCharacter ================
・__init__:4
・SetOptions:4
・ProgramParameter:4
・Start:4
・AutoSelectAttackTarget:4
・Update:4
・Attack:4

================ IconCharacter ===============
・__init__:4
・GetSource:4
・SetOptions:4
・SetObjAnimDic:4
・Start:4
・SetBattleMenu:4
・Update:4
・BattleMenuBtnOnClick:4
・OnClick:4
・BattleMenuController:4

=============== ObjectClass ================
・__init__:4
・SetOptions:4
・ProgramParameter:4
・Main:4
・Start:4
・Update:4
・BtnUpdate:4

================= OneCmdAnim ================
・__init__:4
・SetOptions:4
・ProgramParameter:4
・Start:4
・Update:4
・PlayWithFirstUsed:4
・PlayWithAfterUsed:4
・End:4

================ AllAnimationController ===============
・__init__
・ProgramParameter :4
・Start:4
・Update:4
・IsEndContinueAnimation:4

==================== PieceAnimation ==================
・__init__
・AfterUsedStart:4
・Update:4
・MoveBattleMenuUpdate:4
・MoveBattleMenuFirstUsedStart:4
・DecideParameterForMoveBattleMenu:4
・BackBattleMenuFirstUsedStart:4
・ShowBattleMenuFirstUsedStart:4
"""