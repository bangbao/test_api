# coding: utf-8
from instantft.battle.polt import Polt
opening =Polt()  #开始的对话
opening.set_mapinfo(11, 5) #先设置地图大小

a1=opening.add_agent(137,1,4) #添加人  剑王
a2=opening.add_agent(10046,1,2) #添加人  淘气巨魔
d1=opening.birth_agent(211,9,3) #英雄出生（hero id,x,y）  法师杀手
d2=opening.birth_agent(10028,7,2) #英雄出生（hero id,x,y）   呆呆 
d3=opening.birth_agent(10055,7,4) #英雄出生（hero id,x,y） 槑槑
d4=opening.birth_agent(10055,10,2) #英雄出生（hero id,x,y） 槑槑

opening.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2,d3,d4) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_right(a1,a2)  #朝向。都向右。
opening.face_to_left(d1,d2,d3,d4)  #朝向。敌人都向左。

opening.move(a1,[(1,4),(4,3)],3)
opening.move(a2,[(1,2),(3,2)],3)  #战场格子
opening.idle(d1)
opening.idle(d2)
opening.idle(d3)
opening.idle(d4)

opening.dialog(d1, " 人在塔在。这里是近卫守护整个大陆的最终壁垒，不会放任何外人过去。")
opening.dialog(a1, " 今天俺就推它一推！")
opening.idle(a2)
opening.idle(d2)
opening.idle(d3)
opening.idle(d4)
opening.new_frame()


takeabow=Polt()   #结束的对话
takeabow.set_mapinfo(11,5) #先设置地图大小
a1=takeabow.add_agent(137,4,3) #添加人  剑王
a2=takeabow.add_agent(10046,3,1) #添加人  淘气巨魔
d1=takeabow.birth_agent(211,6,4) #英雄出生（hero id,x,y）  法师杀手
d2=takeabow.birth_agent(10001,7,2) #英雄出生（hero id,x,y）   呆呆 
d3=takeabow.birth_agent(10004,7,4) #英雄出生（hero id,x,y） 槑槑
d4=takeabow.birth_agent(10004,10,2) #英雄出生（hero id,x,y） 槑槑

takeabow.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1,d2,d3,d4) #把哪些人分为一组  a 攻击组 d防守组
takeabow.face_to_right(a1,a2)  #朝向。都向右。
takeabow.face_to_left(d1,d2,d3,d4)  #朝向。巨魔都向左。

takeabow.dialog(d1, "…你们过去吧。前面可是近卫的高地，山岭巨人没有情感，他们绝对不会放水的。")
takeabow.dialog(a2, "神灵姐姐保佑！")
takeabow.dialog(a1, " 一言既出，人马难追！")
takeabow.idle(a2)
takeabow.idle(d2)
takeabow.idle(d3)
takeabow.idle(d4)
takeabow.new_frame()

takeabow.move(d2,[(7,2),(7,1)],1)  #小兵闪开移动
takeabow.move(d3,[(7,4),(7,6)],1)
takeabow.move(d4,[(10,2),(10,1)],1)  
takeabow.move(a1,[(4,3),(12,3)],5)
takeabow.move(a2,[(3,2),(12,2)],5)  #战场格子
takeabow.idle(d2)
takeabow.idle(d3)
takeabow.idle(d4)
takeabow.dialog(a1, "哼！也太小看我的尾行技巧了！")
takeabow.new_frame()

takeabow.hide(a1)
takeabow.hide(a2)
takeabow.idle(d2)
takeabow.idle(d3)
takeabow.idle(d4)
takeabow.hide(d1)
