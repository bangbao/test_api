# coding: utf-8
from instantft.battle.polt import Polt
opening = None #开始的对话

takeabow =Polt() #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小

a1=takeabow.add_agent(221,4,3) #添加人  法师杀手
d1=takeabow.add_agent(10049,5,3) #添加   风骚巨魔 活的

takeabow.set_atk_group(a1) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_right(a1)  #朝向。向右。
takeabow.face_to_left(d1)  #朝向。 风骚 巨魔向左。

takeabow.attack1(a1,d1,"melee_effect_01")   #敌法第2种普通攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(d1,"melee_effect_01",1350)  #受击 （self, hero代号, effect_lua ,掉的血量）
takeabow.new_frame()

takeabow.dead(d1)
takeabow.dialog(a1, "还真是没完没了…这次又有什么好东西？")
takeabow.new_frame()

takeabow.dialog(a1,"…又是可口的魔力饲料呢，法力分解！")