# coding: utf-8
from instantft.battle.polt import Polt
opening =Polt()  #开始的对话
opening.set_mapinfo(11, 5) #先设置地图大小

a1=opening.add_agent(137,3,3) #添加人  剑王
a2=opening.add_agent(10046,4,4) #添加人  淘气巨魔
d1=opening.add_agent(10049,8,3) #添加   风骚巨魔 活的
d2=opening.add_agent(10049,9,5) #添加   风骚巨魔 活的
d3=opening.add_agent(10052,7,3) #添加   下流巨魔 活的
d4=opening.add_agent(10052,10,6) #添加   下流巨魔 活的

opening.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2,d3,d4) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_right(a1,a2)  #朝向。都向右。
opening.face_to_left(d1,d2,d3,d4)  #朝向。敌人都向左。

opening.dead(d1,d2,d3,d4)
opening.dialog(a1, "小子，正主来了！")
opening.dialog(a2, "神马？真主？俺们巨魔只信仰神灵姐姐呀。")
d5=opening.birth_agent(10034,7,2) #人妖出生（hero id,x,y）
opening.set_def_group(d5) #把哪些人分为一组  a 攻击组 d防守组
opening.face_to_left(d5)  #朝向。敌人都向左。
opening.new_frame()

opening.idle(a1)
opening.dialog(a2, "什么啊…一个病老头…")
opening.dialog(d5, "哼…脆弱的肉体，溺毙在鲜血中吧！")
opening.new_frame()

d6=opening.birth_agent(10007,8,3) #英雄出生（hero id,x,y）  叫叫
d7=opening.birth_agent(10007,9,5) #英雄出生（hero id,x,y）  叫叫
d8=opening.birth_agent(10007,7,3)  #英雄出生（hero id,x,y）   叫叫
d9=opening.birth_agent(10007,10,6) #英雄出生（hero id,x,y）   叫叫
opening.set_def_group(d6,d7,d8,d9) #把哪些人分为一组  a 攻击组 d防守组
opening.face_to_left(d6,d7,d8,d9)  #朝向。敌人都向左。
opening.dialog(d5, "…就算是你，也无法打扰大人的计划！")
opening.dialog(a1, "自大的蠢货！")
opening.dialog(a2, "神灵姐姐保佑！我是打酱油的，不要砍我啊啊啊……")

takeabow =Polt()   #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小

a1=takeabow.add_agent(137,5,3) #添加人  剑王
a2=takeabow.add_agent(10046,4,4) #添加人  淘气巨魔
d1=takeabow.birth_agent(10034,6,3) #人妖出生（hero id,x,y）

takeabow.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1) #把哪些人分为一组  a 攻击组 d防守组
takeabow.face_to_right(a1,a2)  #朝向。都向右。
takeabow.face_to_left(d1)  #朝向。巨魔都向左。

takeabow.dialog(d1, "剑王，你…会…受到王的惩罚！")
takeabow.dialog(a1, "哼！巫妖王赐予我主宰之剑，现在，我就是王的意志！")
takeabow.idle(a2)