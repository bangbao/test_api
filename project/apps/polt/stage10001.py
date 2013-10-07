# coding: utf-8
from instantft.battle.polt import Polt

opening = Polt() #开始的对话
opening.set_mapinfo(12,8,2,80,(3,3),(10,3)) #先设置地图大小 set_mapinfo(x, y, sky, pixel, attack, defend)
a1 = opening.add_agent(221,3,2) #添加人（hero id,x,y）   法师杀手
a2 = opening.add_agent(137,3,4) #添加人  剑王
d1 = opening.add_agent(10119,11,3) #添加人 肉山 先用屠夫替代
opening.set_atk_group(a1, a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1) #把哪些人分为一组  a 攻击组 d防守组
opening.face_to_left(d1)  #设置朝向
opening.face_to_right(a1, a2) #朝向,如果转向，在后面的new_frame里新设

opening.dialog(a1, "是时候终结你了，肉山!我要代表月神消灭你！") #逗号后面，意思是点击才能继续
opening.idle(a2)
opening.idle(d1)
opening.new_frame()

opening.idle(a1)
opening.dialog(a2, "我跟你说过你们都没戏！不朽盾和奶酪统统是我的！")
opening.idle(d1)
opening.new_frame()

opening.dialog(d1,"愚蠢的凡人！在我的真正形态前颤抖吧！")  #能加震屏不？
opening.idle(a1)
opening.idle(a2)
opening.new_frame()

opening.idle(a1)
opening.idle(d1)
opening.dialog(a2, "巫妖王万岁！")
opening.new_frame()

opening.move(a2,[(3,2),(8,4)],4)  #战场格子
opening.move(d1,[(11,3),(9,3)],4)
opening.idle(a1)
for i in xrange(4):
	opening.new_frame()

opening.attack1(a2,d1,"melee_effect_01")   #剑王第1种普通攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
opening.hurt(d1,"melee_effect_01",800)  #受击 （self, hero代号, effect_lua ,掉的血量）
opening.idle(a1)
opening.new_frame()  

opening.attack1(d1,a2,"melee_effect_01")   #肉山的反击 （self，攻击者变量名 ，目标 变量名 ，effect_lua)
opening.hurt(a2,"melee_effect_01",1260)  #受击 （self, hero代号, effect_lua ,掉的血量）  最好换个受击特效
opening.idle(a1)
opening.new_frame()   

opening.dialog(a2, "去死！无敌淘汰斩！ ")
opening.idle(d1)
opening.idle(a1)
opening.new_frame()   

opening.attack3(a2,d1,"melee_effect_01")   #剑王怒气攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
opening.hurt(d1," melee_effect_01",9999)  #受击 （self, hero代号, effect_lua ,掉的血量）
opening.idle(a1)  
opening.new_frame()   

opening.dialog(a2, " 果然是肉山，居然还剩1点血 ")
opening.idle(d1)
opening.idle(a1)  #让目标消失 ( 消失者的变量名)
opening.new_frame()   

opening.idle(a2)
opening.dialog(d1, "同样招数对我是无效的,本魔王已经看穿你的拳了！")
opening.idle(a1) 
opening.new_frame()   

opening.idle(a2)
opening.idle(d1)
opening.hide(a1)  #让目标消失 ( 消失者的变量名)
opening.new_frame()   

opening.idle(d1)
opening.idle(a2)
opening.appear(a1,8,2)    #之前消失过的目标出现 
opening.new_frame()   

opening.attack1(a1,d1,"melee_effect_01")        #敌法师第1种攻击：怒气攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
opening.hurt(d1,"melee_effect_01",1)  #受击 （self, hero代号, effect_lua ,掉的血量）
opening.idle(a2)
opening.new_frame() 

opening.dead(d1)
d2 = opening.birth_agent(50021,10,3) #（英雄id,x,y）  英雄出生
opening.set_def_group(d2) #把哪些人分为一组  a 攻击组 d防守组
opening.new_frame() 

opening.face_to_left(d2)  #设置朝向
opening.dialog(a1, "看哥神补刀！宝物属于近卫！")
opening.idle(a2)
opening.idle(d1)
opening.new_frame() 

opening.idle(a1)
opening.idle(d2)
opening.dialog(a2, "谁敢动我的奶酪！？")
opening.new_frame() 

opening.aside("为了争夺奶酪，二人在寒冰之巅开始终极决斗。英雄，你要帮助谁呢？")  #结束的对话 

takeabow =Polt() #战斗结束后的脚本
takeabow.set_mapinfo(12,8,2,80,(3,3),(10,3)) #先设置地图大小 set_mapinfo(x, y, sky, pixel, attack, defend)
a1 = takeabow.add_agent(221,7,3) #添加人（hero id,x,y）   法师杀手 
d1 = takeabow.add_agent(137,8,4) #添加人  剑王

takeabow.set_atk_group(a1) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_left(d1)  #设置朝向
takeabow.face_to_right(a1) #朝向,如果转向，在后面的new_frame里新设

takeabow.attack1(a1,d1,"melee_effect_01")        #敌法师第1种攻击：怒气攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(d1,"melee_effect_01",800)  #受击 （self, hero代号, effect_lua ,掉的血量）
takeabow.new_frame()

takeabow.attack3(d1,a1,"melee_jianwang02")        #剑王第1种攻击：怒气攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(a1,"melee_effect_01",1300)  #受击 （self, hero代号, effect_lua ,掉的血量）
takeabow.new_frame()

takeabow.attack2(a1,d1,"melee_effect_01")        #敌法师第1种攻击：怒气攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(d1,"melee_effect_01",800)  #受击 （self, hero代号, effect_lua ,掉的血量）
takeabow.new_frame()

takeabow.attack2(d1,a1,"melee_effect_01 ")        #剑王第1种攻击：怒气攻击  （self，攻击者变量名 ，目标 变量名 ，effect_lua)
takeabow.hurt(a1,"melee_effect_01",650)  #受击 （self, hero代号, effect_lua ,掉的血量）
takeabow.new_frame()

takeabow.aside("双方依然僵持不下……")
takeabow.idle(d1)
takeabow.idle(a1)
takeabow.new_frame()

d2 = takeabow.birth_agent(3,4,6) #（英雄id,x,y）  #英雄出生
takeabow.set_def_group(d2) #把哪些人分为一组  a 攻击组 d防守组
takeabow.new_frame()

takeabow.face_to_left(d2)  #设置朝向
takeabow.move(a1,[(7,3),(6,3)],5)
takeabow.move(a2,[(8,3),(9,3)],5)  #战场格子
takeabow.new_frame()

takeabow.dialog(a1, "好贱，果然是剑王。敢在哥的地盘撒野，你摊上大事了。") 
takeabow.idle(d1)
takeabow.idle(d2)
takeabow.new_frame()

takeabow.idle(a1)
takeabow.idle(d2)
takeabow.dialog(d1,"瞎子！咱们走着瞧。")
takeabow.aside("咦？传说中肉山的宝物【不朽盾】，掉在哪儿了？……")
