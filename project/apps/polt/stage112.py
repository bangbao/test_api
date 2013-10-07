# coding: utf-8
from instantft.battle.polt import Polt
opening=None #开始的对话

takeabow=Polt() #结束的对话
takeabow.set_mapinfo(11, 5) #先设置地图大小

a1=takeabow.add_agent(10046,7,2) #添加人 淘气巨魔1 活着
a2=takeabow.add_agent(10046,6,3) #添加人 淘气巨魔2 死的
a3=takeabow.add_agent(211,3,3)   #添加人 法师杀手 
d1=takeabow.add_agent(10022,9,5) #添加人  狗头1 死的

takeabow.set_atk_group(a1,a3) #把哪些人分为一组  a 攻击组 d防守组
takeabow.set_def_group(d1,a2) #把哪些人分为一组  a 攻击组 d防守组

takeabow.face_to_left(a2,d1)  #设置朝向 活巨魔向左，死狗头向左
takeabow.face_to_right(a1,a3) #朝向。死巨魔向右。如果转向在后面的new_frame里新设

takeabow.dead(a2,d1)
takeabow.dialog(a1, "尘归尘…")
takeabow.new_frame()

takeabow.move(a1,[(7,2),(4,3)],2)
takeabow.dialog(a3, "土归土……" )
takeabow.new_frame()

takeabow.face_to_right(a1) 
takeabow.move(a1,[(4,3),(8,4)],2)
takeabow.new_frame()

takeabow.dialog(a1, "英雄，这有件装备。")
takeabow.dialog(a3,"哦？死人也有用途嘛。")
