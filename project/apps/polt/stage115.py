# coding: utf-8
from instantft.battle.polt import Polt
opening = Polt() #开始的对话
opening.set_mapinfo(11, 5) #先设置地图大小

a1=opening.add_agent(10046,9,2) #添加人 淘气巨魔1 活着
a2=opening.add_agent(10046,10,5) #添加人 淘气巨魔2 活着
d1=opening.add_agent(10049,12,2) #添加人 黑暗巨魔1 活的
d2=opening.add_agent(10049,12,5) #添加人 黑暗巨魔2 活的

opening.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_left(a1,a2,d1,d2)  #朝向。巨魔都向左。

opening.move(a1,[(9,2),(3,2)],3)
opening.move(a2,[(10,5),(4,4)],3)  #战场格子
opening.move(d1,[(12,2),(8,2)],3)
opening.move(d2,[(12,2),(9,5)],3)  #战场格子
opening.new_frame()

opening.attack1(d1,a1,"range_xialiu")            #下流巨魔第1种普通攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)     
opening.attack1(d2,a2,"range_xialiu")         #下流巨魔第1种普通攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
opening.hurt(a1," range_xialiu",150)  #受击 （self, hero代号, effect_lua ,掉的血量）
opening.hurt(a1," range_xialiu",134)  #受击 （self, hero代号, effect_lua ,掉的血量）
opening.new_frame()

opening.dead(a1)
opening.dead(a2)
opening.dialog(d1, "死！")
opening.dialog(d2, "死！")
opening.new_frame()

a3=opening.birth_agent(221,1,2) #英雄出生（hero id,x,y）  法师杀手又回来了
a4=opening.birth_agent(137,1,4) #英雄出生（hero id,x,y）  剑王又回来了
opening.set_atk_group(a3,a4) #把哪些人分为一组  a 攻击组 d防守组
opening.face_to_right(a3,a4)  #朝向。剑王、斧圣都向右。

opening.dialog(d1, "！")
opening.dialog(d2, "！")
opening.dialog(a3, "哈，剑王？人生何处不相逢！")
opening.dialog(a4, "哼，也来找不朽的下落？")
opening.new_frame()

d3=opening.birth_agent(137,10,3) #英雄出生（hero id,x,y）  暗牧出场
opening.set_def_group(d3)  #每个代号只用定义一次
opening.face_to_left(d3) 
opening.dialog(d1, "老大!")
opening.dialog(d2, "老大!")
opening.idle(a3)
opening.idle(a4)
opening.new_frame()

opening.idle(a3)
opening.idle(a4)
opening.idle(d1)
opening.idle(d2)
opening.dialog(d3, "呜哈！又来了一群小白鼠，大哥我真是喜闻乐见！崽子们，接客！")
opening.aside("黑色的巨魔？！")

takeabow =Polt() #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小

a1=takeabow.add_agent(221,4,2) #添加本方英雄（hero id,x,y）    法师杀手又回来了   
a2=takeabow.add_agent(137,7,4) #添加本方英雄 剑王
d3=takeabow.add_agent(137,10,3) #添加敌方英雄 暗牧

takeabow.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d3) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_left(d3)  #暗牧向左
takeabow.face_to_right(a1,a2) #法师杀手、剑王向右。

takeabow.dialog(a1,"喂！慢着！")
takeabow.attack3(a2,d1," melee_effect_01")        #剑王怒气攻击（self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(d1," melee_effect_01",9999)  #受击 （self, hero代号,填skill_data里的effect_lua,掉的血量）
takeabow.new_frame()

takeabow.dead(d3)
takeabow.dialog(a1,"……")
takeabow.dialog(a2, "呸，啰嗦！不过是战斗力只有5的渣！")
takeabow.new_frame()

takeabow.dialog(a1,"你猪啊！问都没问就把他挂了！我们怎么知道不朽藏在哪儿！")
takeabow.dialog(a2, "额…─.─||")
takeabow.new_frame()

takeabow.dialog(a1,"不管了，哥先闪人了！")
takeabow.idle(a2)
a3=takeabow.add_agent(10046,1,3) #添加人 淘气巨魔1
takeabow.set_atk_group(a3)
takeabow.face_to_right(a3)
takeabow.new_frame()

takeabow.hide(a1)
takeabow.move(a3,[(1,3),(9,3)],4)  #战场格子
takeabow.dialog(a2,"!")
takeabow.new_frame()

takeabow.dialog(a3,"大…大哥，怎么会酱紫！")
takeabow.dialog(a2,"此事必有蹊跷……")
