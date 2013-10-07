# coding: utf-8
from instantft.battle.polt import Polt

opening = Polt() #开始的对话
opening.set_mapinfo(11, 5)
a1 = opening.add_agent(1, 1, 2) #添加人（hero id,位置）   法师杀手 先用冰冰替代
a2 = opening.add_agent(2, 2, 3) #添加人  剑王
d1 = opening.add_agent(3, 3, 4) #添加人 肉山 先用屠夫替代

opening.set_atk_group(a1, a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_left(d1)  #设置朝向
opening.face_to_right(a1, a2) #朝向

opening.dialog(a1, "时机来临了，", "肉山，我要代表月神消灭你！") #逗号后面，意思是点击才能继续
opening.idle(a2)
opening.idle(d1)
opening.new_frame()

d2 = opening.birth_agent(3, 3, 5)
opening.set_def_group(d2)
opening.face_to_left(d2)
opening.idle(a1)
opening.dialog(a2, "我跟你说过你真的完了！", "不朽盾和奶酪统统是我的！")
opening.idle(d1)
opening.new_frame()

opening.idle(a1)  #发愣
opening.idle(a2)
opening.dialog(d1, "愚蠢的凡人！", "在我的真正形态前颤抖吧！")
opening.new_frame()

opening.move(a1, [(1, 2), (5, 0), (6, 3)], 10)
opening.move(a2, [(1, 2)], 10)  #战场格子
opening.move(d1, [(1, 2)], 10)
opening.new_frame()

opening.attack1(a1, d1, 'a')
opening.attack1(a2, d2, 'b')
opening.attack1(d1, a1, 'c')
opening.new_frame()

opening.dead(d1)
opening.dialog(a1, "耶！奶酪属于近卫！")
opening.dialog(a2, "呸，谁动了我的奶酪！")

takeabow = Polt() # 开始的对话
takeabow.aside("为了争夺奶酪，两个人在寒冰之巅开始了终极决斗？英雄，你，要帮助谁呢？")  #结束的对话

if __name__ == "__main__":
    print opening.record()
