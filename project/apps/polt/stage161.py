# coding: utf-8
from instantft.battle.polt import Polt
opening =Polt()  #开始的对话
opening.set_mapinfo(11, 5) #先设置地图大小

a1=opening.add_agent(137,4,4) #添加人  剑王
a2=opening.add_agent(10046,2,4) #添加人  淘气巨魔
d1=opening.birth_agent(211,9,3) #英雄出生（hero id,x,y）  法师杀手
d2=opening.birth_agent(10001,7,2) #英雄出生（hero id,x,y）   呆呆 
d3=opening.birth_agent(10004,7,4) #英雄出生（hero id,x,y） 槑槑
d4=opening.birth_agent(10004,10,2) #英雄出生（hero id,x,y） 槑槑

opening.set_atk_group(a1,a2) #把哪些人分为一组  a 攻击组 d防守组
opening.set_def_group(d1,d2,d3,d4) #把哪些人分为一组  a 攻击组 d防守组

opening.face_to_right(a1,a2)  #朝向。都向右。
opening.face_to_left(d1,d2,d3,d4)  #朝向。敌人都向左。

opening.dialog(d1, "准备作战！为死掉的弟兄们复仇！")
opening.dialog(a1, " 哈。法师杀手，看来有人先一步烧了你的后院。")
opening.idle(a2)
opening.idle(d2)
opening.idle(d3)
opening.idle(d4)
opening.new_frame()

opening.dialog(d1, "可恶天灾！这就是你们调虎离山的卑鄙伎俩吗")
opening.dialog(a1, " 等等！")
opening.idle(a2)
opening.idle(d2)
opening.idle(d3)
opening.idle(d4)
opening.new_frame()

takeabow =Polt()   #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小
a1=takeabow.add_agent(137,5,4) #添加人  剑王
a2=takeabow.add_agent(10046,2,4) #添加人  淘气巨魔
d1=takeabow.birth_agent(211,6,4) #英雄出生（hero id,x,y）  法师杀手
d2=takeabow.birth_agent(10001,7,2) #英雄出生（hero id,x,y）   呆呆 
d3=takeabow.birth_agent(10004,7,4) #英雄出生（hero id,x,y） 槑槑
d4=takeabow.birth_agent(10004,10,2) #英雄出生（hero id,x,y） 槑槑

takeabow.set_atk_group(a1,a2,) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1,d2,d3,d4) #把哪些人分为一组  a 攻击组 d防守组
takeabow.face_to_right(a1,a2)  #朝向。都向右。
takeabow.face_to_left(d1,d2,d3,d4)  #朝向。巨魔都向左。

takeabow.dialog(a2, "……")
takeabow.dialog(a1, "瞎子，只有这个小不点可以跟上黑巨魔。难道你不想知道雪域这些异动的真凶吗？")
takeabow.dialog(d1, "好！你们可以从这里过去，但是要通过近卫的关口，你必须证明你有足够的资格！")
takeabow.idle(d2)
takeabow.idle(d3)
takeabow.idle(d4)
takeabow.new_frame()

takeabow.idle(a2)
takeabow.dialog(a1, "切！小菜一碟。")
takeabow.dialog(d1, "我在最后的关口等你！（二货！一点面子也不给…)")
takeabow.idle(d2)
takeabow.idle(d2)
takeabow.idle(d3)
takeabow.idle(d4)