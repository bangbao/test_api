# coding: utf-8
from instantft.battle.polt import Polt
opening =Polt()  #开始的对话
opening.set_mapinfo(11, 5) #先设置地图大小

a1=opening.add_agent(137,3,3) #添加人  剑王
a2=opening.add_agent(10046,5,4) #添加人  淘气巨魔
d1=opening.birth_agent(10004,4,3) #英雄出生（hero id,x,y）   叫叫
d2=opening.birth_agent(10007,6,4) #英雄出生（hero id,x,y）   叫叫

opening.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_right(a1,a2)  #朝向。都向右。
opening.face_to_left(d1,d2)  #朝向。敌人都向左。

opening.attack2(a1,d1,"  melee_effect_01")   #斧王怒气攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
opening.hurt(d1,"melee_effect_01",9999)  #受击 （self, hero代号, 填skill_data里的effect_lua ,掉的血量）
opening.attack1(a2,d2,"  melee_effect_01") #淘气普通攻击
opening.hurt(d2," melee_effect_01",13)  #受击 （self, hero代号, 填skill_data里的effect_lua ,掉的血量）
opening.new_frame()

opening.dead(d1)
opening.attack1(d2,a2,"melee_effect_01") #叫叫普通攻击
opening.hurt(d2," melee_effect_01",3)  #受击 （self, hero代号, 填skill_data里的effect_lua ,掉的血量）
opening.idle(a1)
opening.new_frame()

opening.dialog(a2, "哎呀呀呀！我受伤了！！！")
opening.dialog(a1, "……")
d1=opening.birth_agent(10004,8,3) #英雄出生（hero id,x,y）  叫叫
d2=opening.birth_agent(10004,9,5) #英雄出生（hero id,x,y）  叫叫
d3=opening.birth_agent(10004,7,3)  #英雄出生（hero id,x,y）   叫叫
d4=opening.birth_agent(10004,10,6) #英雄出生（hero id,x,y）   叫叫
opening.set_def_group(d1,d2,d3,d4) #把哪些人分为一组  a 攻击组 d防守组
opening.face_to_left(d1,d2,d3,d4)  #朝向。敌人都向左。

takeabow =Polt()   #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小

a1=takeabow.add_agent(137,5,3) #添加人  剑王
d2=takeabow.add_agent(10046,4,4) #添加人  淘气巨魔

takeabow.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_right(a1,a2)  #朝向。都向右。
takeabow.face_to_left(d1)  #朝向。巨魔都向左。

takeabow.dialog(a2, "饿...发生了什么…好痛")
takeabow.dialog(a1, "一个能打的都没有！不能打架就老实打酱油去！")
takeabow.idle(a2)
